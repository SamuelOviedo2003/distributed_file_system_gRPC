# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: dfs.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'dfs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tdfs.proto\x12\x03\x64\x66s\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"1\n\rLoginResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"7\n\x11\x43reateUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"6\n\x12\x43reateUserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1f\n\x0bListRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"#\n\x0cListResponse\x12\x13\n\x0b\x64irectories\x18\x01 \x03(\t\":\n\x0eMakeDirRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x16\n\x0e\x64irectory_name\x18\x02 \x01(\t\"3\n\x0fMakeDirResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xe8\x01\n\x03\x44\x46S\x12.\n\x05Login\x12\x11.dfs.LoginRequest\x1a\x12.dfs.LoginResponse\x12=\n\nCreateUser\x12\x16.dfs.CreateUserRequest\x1a\x17.dfs.CreateUserResponse\x12\x36\n\x0fListDirectories\x12\x10.dfs.ListRequest\x1a\x11.dfs.ListResponse\x12:\n\rMakeDirectory\x12\x13.dfs.MakeDirRequest\x1a\x14.dfs.MakeDirResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dfs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGINREQUEST']._serialized_start=18
  _globals['_LOGINREQUEST']._serialized_end=68
  _globals['_LOGINRESPONSE']._serialized_start=70
  _globals['_LOGINRESPONSE']._serialized_end=119
  _globals['_CREATEUSERREQUEST']._serialized_start=121
  _globals['_CREATEUSERREQUEST']._serialized_end=176
  _globals['_CREATEUSERRESPONSE']._serialized_start=178
  _globals['_CREATEUSERRESPONSE']._serialized_end=232
  _globals['_LISTREQUEST']._serialized_start=234
  _globals['_LISTREQUEST']._serialized_end=265
  _globals['_LISTRESPONSE']._serialized_start=267
  _globals['_LISTRESPONSE']._serialized_end=302
  _globals['_MAKEDIRREQUEST']._serialized_start=304
  _globals['_MAKEDIRREQUEST']._serialized_end=362
  _globals['_MAKEDIRRESPONSE']._serialized_start=364
  _globals['_MAKEDIRRESPONSE']._serialized_end=415
  _globals['_DFS']._serialized_start=418
  _globals['_DFS']._serialized_end=650
# @@protoc_insertion_point(module_scope)
