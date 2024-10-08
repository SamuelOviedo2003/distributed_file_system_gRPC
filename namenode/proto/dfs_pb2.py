# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proto/dfs.proto
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
    'proto/dfs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fproto/dfs.proto\x12\x03\x64\x66s\"4\n\x17RegisterDataNodeRequest\x12\x19\n\x11\x64\x61ta_node_address\x18\x01 \x01(\t\"+\n\x18RegisterDataNodeResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"+\n\x13GetDataNodesRequest\x12\x14\n\x0ctotal_blocks\x18\x01 \x01(\x05\"Y\n\x14GetDataNodesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\ndata_nodes\x18\x02 \x03(\t\x12\x1c\n\x14replication_metadata\x18\x03 \x03(\t\"L\n\x12GetFileInfoRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tdirectory\x18\x02 \x01(\t\x12\x11\n\tfile_name\x18\x03 \x01(\t\"m\n\x13GetFileInfoResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x14\n\x0ctotal_blocks\x18\x02 \x01(\x05\x12\x1e\n\x06\x62locks\x18\x03 \x03(\x0b\x32\x0e.dfs.BlockInfo\x12\x0f\n\x07message\x18\x04 \x01(\t\"\'\n\tBlockInfo\x12\x0c\n\x04node\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"K\n\x11RemoveFileRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tdirectory\x18\x02 \x01(\t\x12\x11\n\tfile_name\x18\x03 \x01(\t\"6\n\x12RemoveFileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x9f\x01\n\x1bRegisterFileMetadataRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tdirectory\x18\x02 \x01(\t\x12\x11\n\tfile_name\x18\x03 \x01(\t\x12\x14\n\x0ctotal_blocks\x18\x04 \x01(\x05\x12\x12\n\ndata_nodes\x18\x05 \x03(\t\x12\x1e\n\x16replication_data_nodes\x18\x06 \x03(\t\"@\n\x1cRegisterFileMetadataResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"&\n\x10ReadBlockRequest\x12\x12\n\nblock_path\x18\x01 \x01(\t\"C\n\x11ReadBlockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x0f\n\x07message\x18\x03 \x01(\t\"\x85\x01\n\x11StoreBlockRequest\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x11\n\tfile_name\x18\x04 \x01(\t\x12\x19\n\x11replication_addrs\x18\x05 \x01(\t\x12\x10\n\x08\x63hecksum\x18\x06 \x01(\r\"6\n\x12StoreBlockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\">\n\x10\x43hangeDirRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x18\n\x10target_directory\x18\x02 \x01(\t\"L\n\x11\x43hangeDirResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rnew_directory\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"<\n\x10RemoveDirRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x16\n\x0e\x64irectory_name\x18\x02 \x01(\t\"5\n\x11RemoveDirResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"1\n\rLoginResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"7\n\x11\x43reateUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"6\n\x12\x43reateUserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\":\n\x0bListRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x19\n\x11\x63urrent_directory\x18\x02 \x01(\t\"#\n\x0cListResponse\x12\x13\n\x0b\x64irectories\x18\x01 \x03(\t\":\n\x0eMakeDirRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x16\n\x0e\x64irectory_name\x18\x02 \x01(\t\"3\n\x0fMakeDirResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"-\n\x10HeartbeatRequest\x12\x19\n\x11\x64\x61ta_node_address\x18\x01 \x01(\t\"$\n\x11HeartbeatResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xa3\x06\n\x03\x44\x46S\x12.\n\x05Login\x12\x11.dfs.LoginRequest\x1a\x12.dfs.LoginResponse\x12=\n\nCreateUser\x12\x16.dfs.CreateUserRequest\x1a\x17.dfs.CreateUserResponse\x12\x36\n\x0fListDirectories\x12\x10.dfs.ListRequest\x1a\x11.dfs.ListResponse\x12:\n\rMakeDirectory\x12\x13.dfs.MakeDirRequest\x1a\x14.dfs.MakeDirResponse\x12@\n\x0f\x43hangeDirectory\x12\x15.dfs.ChangeDirRequest\x1a\x16.dfs.ChangeDirResponse\x12@\n\x0fRemoveDirectory\x12\x15.dfs.RemoveDirRequest\x1a\x16.dfs.RemoveDirResponse\x12=\n\nRemoveFile\x12\x16.dfs.RemoveFileRequest\x1a\x17.dfs.RemoveFileResponse\x12@\n\x0bGetFileInfo\x12\x17.dfs.GetFileInfoRequest\x1a\x18.dfs.GetFileInfoResponse\x12J\n\x13GetDataNodesForFile\x12\x18.dfs.GetDataNodesRequest\x1a\x19.dfs.GetDataNodesResponse\x12[\n\x14RegisterFileMetadata\x12 .dfs.RegisterFileMetadataRequest\x1a!.dfs.RegisterFileMetadataResponse\x12:\n\tHeartbeat\x12\x15.dfs.HeartbeatRequest\x1a\x16.dfs.HeartbeatResponse\x12O\n\x10RegisterDataNode\x12\x1c.dfs.RegisterDataNodeRequest\x1a\x1d.dfs.RegisterDataNodeResponse2\x85\x01\n\x08\x44\x61taNode\x12=\n\nStoreBlock\x12\x16.dfs.StoreBlockRequest\x1a\x17.dfs.StoreBlockResponse\x12:\n\tReadBlock\x12\x15.dfs.ReadBlockRequest\x1a\x16.dfs.ReadBlockResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.dfs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERDATANODEREQUEST']._serialized_start=24
  _globals['_REGISTERDATANODEREQUEST']._serialized_end=76
  _globals['_REGISTERDATANODERESPONSE']._serialized_start=78
  _globals['_REGISTERDATANODERESPONSE']._serialized_end=121
  _globals['_GETDATANODESREQUEST']._serialized_start=123
  _globals['_GETDATANODESREQUEST']._serialized_end=166
  _globals['_GETDATANODESRESPONSE']._serialized_start=168
  _globals['_GETDATANODESRESPONSE']._serialized_end=257
  _globals['_GETFILEINFOREQUEST']._serialized_start=259
  _globals['_GETFILEINFOREQUEST']._serialized_end=335
  _globals['_GETFILEINFORESPONSE']._serialized_start=337
  _globals['_GETFILEINFORESPONSE']._serialized_end=446
  _globals['_BLOCKINFO']._serialized_start=448
  _globals['_BLOCKINFO']._serialized_end=487
  _globals['_REMOVEFILEREQUEST']._serialized_start=489
  _globals['_REMOVEFILEREQUEST']._serialized_end=564
  _globals['_REMOVEFILERESPONSE']._serialized_start=566
  _globals['_REMOVEFILERESPONSE']._serialized_end=620
  _globals['_REGISTERFILEMETADATAREQUEST']._serialized_start=623
  _globals['_REGISTERFILEMETADATAREQUEST']._serialized_end=782
  _globals['_REGISTERFILEMETADATARESPONSE']._serialized_start=784
  _globals['_REGISTERFILEMETADATARESPONSE']._serialized_end=848
  _globals['_READBLOCKREQUEST']._serialized_start=850
  _globals['_READBLOCKREQUEST']._serialized_end=888
  _globals['_READBLOCKRESPONSE']._serialized_start=890
  _globals['_READBLOCKRESPONSE']._serialized_end=957
  _globals['_STOREBLOCKREQUEST']._serialized_start=960
  _globals['_STOREBLOCKREQUEST']._serialized_end=1093
  _globals['_STOREBLOCKRESPONSE']._serialized_start=1095
  _globals['_STOREBLOCKRESPONSE']._serialized_end=1149
  _globals['_CHANGEDIRREQUEST']._serialized_start=1151
  _globals['_CHANGEDIRREQUEST']._serialized_end=1213
  _globals['_CHANGEDIRRESPONSE']._serialized_start=1215
  _globals['_CHANGEDIRRESPONSE']._serialized_end=1291
  _globals['_REMOVEDIRREQUEST']._serialized_start=1293
  _globals['_REMOVEDIRREQUEST']._serialized_end=1353
  _globals['_REMOVEDIRRESPONSE']._serialized_start=1355
  _globals['_REMOVEDIRRESPONSE']._serialized_end=1408
  _globals['_LOGINREQUEST']._serialized_start=1410
  _globals['_LOGINREQUEST']._serialized_end=1460
  _globals['_LOGINRESPONSE']._serialized_start=1462
  _globals['_LOGINRESPONSE']._serialized_end=1511
  _globals['_CREATEUSERREQUEST']._serialized_start=1513
  _globals['_CREATEUSERREQUEST']._serialized_end=1568
  _globals['_CREATEUSERRESPONSE']._serialized_start=1570
  _globals['_CREATEUSERRESPONSE']._serialized_end=1624
  _globals['_LISTREQUEST']._serialized_start=1626
  _globals['_LISTREQUEST']._serialized_end=1684
  _globals['_LISTRESPONSE']._serialized_start=1686
  _globals['_LISTRESPONSE']._serialized_end=1721
  _globals['_MAKEDIRREQUEST']._serialized_start=1723
  _globals['_MAKEDIRREQUEST']._serialized_end=1781
  _globals['_MAKEDIRRESPONSE']._serialized_start=1783
  _globals['_MAKEDIRRESPONSE']._serialized_end=1834
  _globals['_HEARTBEATREQUEST']._serialized_start=1836
  _globals['_HEARTBEATREQUEST']._serialized_end=1881
  _globals['_HEARTBEATRESPONSE']._serialized_start=1883
  _globals['_HEARTBEATRESPONSE']._serialized_end=1919
  _globals['_DFS']._serialized_start=1922
  _globals['_DFS']._serialized_end=2725
  _globals['_DATANODE']._serialized_start=2728
  _globals['_DATANODE']._serialized_end=2861
# @@protoc_insertion_point(module_scope)
