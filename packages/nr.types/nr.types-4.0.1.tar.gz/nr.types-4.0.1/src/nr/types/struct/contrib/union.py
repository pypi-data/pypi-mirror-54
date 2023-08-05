# -*- coding: utf8 -*-
# Copyright (c) 2019 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

""" This module provides a configurable [[UnionType]] for struct fields. """

import typing

from nr.types import abc
from nr.types.interface import Interface, implements
from nr.types.utils import classdef
from nr.types.utils.typing import is_generic, get_generic_args

from ..core.adapters import DefaultTypeMapper
from ..core.errors import ExtractTypeError, ExtractValueError, InvalidTypeDefinitionError
from ..core.interfaces import IConverter, IDataType, ITypeDefAdapter
from ..core.json import JsonObjectMapper
from ..struct import Struct, StructType


class UnknownUnionTypeError(Exception):
  pass


class IUnionTypeMember(Interface):
  """ Represents a member of a [[UnionType]] as returned by a
  [[IUnionTypeResolver]] when given a type name. This interface provides all
  the information about this union member. """

  def get_name(self):  # type: () -> str
    pass

  def get_type_name(self):  # type: () -> str
    pass

  def get_struct(self):  # type: () -> Type[Struct]
    """ Return the [[Struct]] subclass for this union type member. """
    pass

  def create_instance(self, deserialized_struct):   # type: (Struct) -> Any
    """ Create an instance of this union type member. A usualy implementation
    would be to just return the *deserialized_struct*, but in some use cases
    you may want to wrap it in another type. """
    pass

  def isinstance_check(self, value):  # type: (Any) -> bool
    """ Check if *value* is an instance of the type returned by
    [[create_instance()]]. """
    pass


class IUnionTypeResolver(Interface):
  """ An interface for resolving union types by a name. """

  classdef.comparable([])

  def resolve(self, type_name):  # type: (str) -> IUnionTypeResolver
    """ Resolve the *type_name* to a [[IUnionTypeMember]] instance. If the
    *type_name* is unknown, an [[UnknownUnionTypeError]] must be raised. """
    pass

  def reverse(self, value):  # type: (Any) -> IUnionTypeResolver
    """ Return the [[IUnionTypeResolver]] for the specified *value*, which is
    whatever [[IUnionTypeMember.create_instance()]] returns. Raises
    [[UnknownUnionTypeError]] if the value cannot be reversed. """
    pass

  def members(self):  # type: () -> Iterable[IUnionTypeResolver]
    """ List up all the members of this resolver. If listing members is not
    supported, a [[NotImplementedError]] must be raised to indicate that. """
    pass


@implements(IUnionTypeResolver)
class StandardTypeResolver(object):
  """ This implementation of the [[IUnionTypeResolver]] uses a static mapping
  of type names to [[Struct]] subclasses. It can be initialized from a list
  of [[Struct]] objects or a dictionary. If a list is specified, the type name
  is derived from the `__union_type_name__` attribute or the class name, in
  that order. """

  @implements(IUnionTypeMember)
  class _Member(object):
    def __init__(self, name, cls):
      self._name = name
      self._cls = cls
    def get_name(self):
      return self._name
    def get_type_name(self):
      return self._cls.__name__
    def get_struct(self):
      return self._cls
    def create_instance(self, deserialized_struct):
      return deserialized_struct
    def isinstance_check(self, value):
      return isinstance(value, self._cls)

  def __init__(self, types):
    if isinstance(types, abc.Mapping):
      self.types = types
    elif isinstance(types, (list, tuple)):
      self.types = {}
      for item in types:
        struct_cls = self._unpack_struct_item(item)
        name = getattr(struct_cls, '__union_type_name__', struct_cls.__class__)
        self.types[name] = struct_cls
    else:
      raise TypeError('expected list/tuple/dict, got {}'
                      .format(type(types).__name__))

  classdef.comparable(['types'])

  @staticmethod
  def _unpack_struct_item(item):
    if isinstance(item, StructType):
      return item.struct_cls
    elif isinstance(item, type) and issubclass(item, Struct):
      return item
    else:
      raise TypeError('expected StructType instance or Struct class, '
        'got {}'.format(type(item).__name__))

  def resolve(self, type_name):
    try:
      return self._Member(type_name, self.types[type_name])
    except KeyError:
      raise UnknownUnionTypeError(type_name)

  def reverse(self, value):
    results = ((k, v) for k, v in self.types.items() if v == type(value))
    try:
      type_name, struct_type = next(results)
    except StopIteration:
      raise UnknownUnionTypeError(type(value))
    return self._Member(type_name, struct_type)

  def members(self):
    try:
      items = self.types.items()
    except NotImplementedError:
      raise NotImplementedError('wrapped "types" mapping does not support iteration')
    return (self._Member(k, v) for k, v in items)


@implements(IUnionTypeResolver)
class EntrypointTypeResolver(StandardTypeResolver):
  """ Collects all entries from an entrypoints group. Checks if the class
  loaded via an entrypoint is either a subclass of the specified *base_type*
  or implements it's interface (if *base_type* is a subclass of [[Interface]]).
  """

  class _EntrypointMember(StandardTypeResolver._Member):
    def __init__(self, resolver, name, cls):
      super(EntrypointTypeResolver._EntrypointMember, self).__init__(name, cls)
      self.resolver = resolver
    # TODO (@NiklasRosenstein): Allow customatization of create_instance() ?
    def get_struct(self):
      return self._cls.load()

  def __init__(self, entrypoint_group, base_type=None):
    import pkg_resources
    types = {}
    for ep in pkg_resources.iter_entry_points(entrypoint_group):
      types[ep.name] = ep
    super(EntrypointTypeResolver, self).__init__(types)
    self.base_type = base_type

  classdef.comparable(['types', 'base_type'])

  def _Member(self, name, cls):
    return self._EntrypointMember(self, name, cls)


@implements(IDataType)
class UnionType(object):
  """ The UnionType represents multiple types. A value represented by this
  datatype can be of any of the types that are encapsulated by the union
  type. UnionType only supports the encapsulation of [[StructType]]s.

  The UnionType can operate in two modes for the serialization and
  deserialization. In either mode, the object from which the UnionType is
  deserialized must contain a "type" key (configurable with the `type_key`
  parameter).

  In the default mode, the fields for the type are read from the same level.

  ```yaml
  type: onePossibleUnionType
  someField: value
  ```

  With the `nested` option enabled, the values are instead read from an object
  nested with the same name as the type.

  ```yaml
  type: onePossibleUnionType
  onePossibleUnionType:
    someField: value
  ```

  The name of types wrapped by the UnionType can be specified in multiple
  ways. The most common way is to specify a mapping as a parameter to the
  UnionType constructor.

  ```py
  UnionType({
    "onePossibleUnionType": StructOne,
    "another": StructTwo
  })
  ```

  Alternatively, a list of [[Struct]] implementations may be passed, in which
  case the name of the type in the union is derived first from the class-level
  `__union_type_name__` attribute or the class name.

  ```py
  UnionType([StructOne, StructTwo])
  ```

  The [[UnionAdapter]] provides support for declaring unions using typing
  annotations. Note that the same rules for deriving the type name apply as
  for the option where a list is passed to the UnionType constructor.

  ```py
  Union[StructOne, StructTwo]
  ```

  > Note: If the *types* parameter is a mapping, it is used as-is. This allows
  > for very dynamic union type resolving.
  """

  classdef.comparable(['type_resolver', 'type_key', 'nested'])

  def __init__(self, type_resolver, type_key='type', nested=False):
    # type: (IUnionTypeResolver, str, bool)

    if isinstance(type_resolver, (dict, list, tuple)):
      type_resolver = StandardTypeResolver(type_resolver)

    self.type_resolver = type_resolver
    self.type_key = type_key
    self.nested = nested

  def check_value(self, py_value):
    try:
      members = list(self.type_resolver.members())
    except NotImplementedError:
      # TODO (@NiklasRosenstein): We use check_value() to type check when
      #   initializing a Struct instance's field, and we don't want that to
      #   fail just because the type resolver doesn't support member listing.
      #   Maybe make this behavior configurable?
      return py_value
    if not any(x.isinstance_check(py_value) for x in members):
      raise TypeError('expected {{{}}}, got {}'.format(
        '|'.join(sorted(x.get_name() for x in members)),
        type(py_value).__name__))
    return py_value


@DefaultTypeMapper.register()
@implements(ITypeDefAdapter)
class UnionAdapter(object):

  def adapt(self, mapper, py_type_def):
    if is_generic(py_type_def, typing.Union):
      union_types = get_generic_args(py_type_def)
      if all(issubclass(x, Struct) for x in union_types):
        return UnionType(union_types)
    raise InvalidTypeDefinitionError(py_type_def)


@JsonObjectMapper.register()
@implements(IConverter)
class UnionConverter(object):

  def accept(self, datatype):
    return type(datatype) == UnionType

  def deserialize(self, mapper, location):
    if not isinstance(location.value, abc.Mapping):
      raise ExtractTypeError(location)

    datatype = location.datatype  # type: UnionType
    type_key = datatype.type_key
    if type_key not in location.value:
      raise ExtractValueError(location,
        'required key "{}" not found'.format(type_key))

    type_name = location.value[type_key]
    try:
      member = datatype.type_resolver.resolve(type_name)
    except UnknownUnionTypeError:
      raise ExtractValueError(location,
        'unknown union type: "{}"'.format(type_name))

    if datatype.nested:
      struct_type = StructType(member.get_struct())
      location = location.sub(type_key, location.value[type_key], struct_type)
    else:
      struct_type = StructType(member.get_struct(), ignore_keys=[type_key])
      location = location.replace(datatype=struct_type)

    return mapper.deserialize(location)

  def serialize(self, mapper, location):
    datatype = location.datatype
    value = location.value
    try:
      member = datatype.type_resolver.reverse(value)
    except UnknownUnionTypeError as exc:
      try:
        members = datatype.type_resolver.members()
      except NotImplementedError:
        message = str(exc)
      else:
        message = 'expected {{{}}}, got {}'.format(
          '|'.join(sorted(x.get_type_name() for x in members)),
          type(value).__name__)
      raise ExtractTypeError(location, message)

    if datatype.nested:
      struct_type = StructType(member.get_struct())
      location = location.sub(type_key, location.value, struct_type)
    else:
      struct_type = StructType(member.get_struct(), ignore_keys=[datatype.type_key])
      location = location.replace(datatype=struct_type)

    result = {datatype.type_key: member.get_name()}
    result.update(mapper.serialize(location))
    return result


__all__ = [
  'IUnionTypeMember',
  'IUnionTypeResolver',
  'UnionType',
]
