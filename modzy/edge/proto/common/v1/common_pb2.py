# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/modzy/common/v1/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from ...protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#protos/modzy/common/v1/common.proto\x12\tcommon.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc-gen-openapiv2/options/annotations.proto\"\xa4\x01\n\x0fModelIdentifier\x12\x34\n\nidentifier\x18\x01 \x01(\tB\x14\xe0\x41\x02\x92\x41\x0eJ\x0c\"ed542963de\"R\nidentifier\x12)\n\x07version\x18\x02 \x01(\tB\x0f\xe0\x41\x02\x92\x41\tJ\x07\"1.0.1\"R\x07version\x12\x30\n\x04name\x18\x03 \x01(\tB\x1c\xe0\x41\x03\x92\x41\x16J\x14\"Sentiment Analysis\"R\x04name\"\xac\x01\n\x0cModelLibrary\x12\x1e\n\nidentifier\x18\x05 \x01(\tR\nidentifier\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12%\n\x0e\x63\x61_certificate\x18\x03 \x01(\tR\rcaCertificate\x12/\n\x08registry\x18\x04 \x01(\x0b\x32\x13.common.v1.RegistryR\x08registry\"\xa8\x01\n\x16ModelAutoscalingConfig\x12\x30\n\x05model\x18\x01 \x01(\x0b\x32\x1a.common.v1.ModelIdentifierR\x05model\x12\x18\n\x07minimum\x18\x02 \x01(\rR\x07minimum\x12\x18\n\x07maximum\x18\x03 \x01(\rR\x07maximum\x12(\n\x10model_library_id\x18\x04 \x01(\tR\x0emodelLibraryId\"|\n\x08Registry\x12\x12\n\x04host\x18\x01 \x01(\tR\x04host\x12\x12\n\x04port\x18\x02 \x01(\rR\x04port\x12 \n\x0b\x63redentials\x18\x03 \x01(\tR\x0b\x63redentials\x12&\n\x0fskip_tls_verify\x18\x05 \x01(\x08R\rskipTlsVerify\"\xa2\x02\n\x0bListOptions\x12=\n\x07\x66ilters\x18\x01 \x03(\x0b\x32#.common.v1.ListOptions.FiltersEntryR\x07\x66ilters\x12\x34\n\x04sort\x18\x02 \x03(\x0b\x32 .common.v1.ListOptions.SortEntryR\x04sort\x12)\n\x04page\x18\x03 \x01(\x0b\x32\x15.common.v1.PaginationR\x04page\x1a:\n\x0c\x46iltersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a\x37\n\tSortEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"8\n\nPagination\x12\x16\n\x06number\x18\x01 \x01(\rR\x06number\x12\x12\n\x04size\x18\x02 \x01(\rR\x04size\"\x82\x01\n\x04Page\x12\x16\n\x06number\x18\x01 \x01(\rR\x06number\x12\x12\n\x04size\x18\x02 \x01(\rR\x04size\x12\"\n\npage_count\x18\x03 \x01(\rB\x03\xe0\x41\x03R\tpageCount\x12*\n\x0etotal_elements\x18\x04 \x01(\rB\x03\xe0\x41\x03R\rtotalElementsBa\n#com.modzy.platform.protos.common.v1P\x01Z8github.modzy.engineering/platform/protos/modzy/common/v1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.modzy.common.v1.common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#com.modzy.platform.protos.common.v1P\001Z8github.modzy.engineering/platform/protos/modzy/common/v1'
  _MODELIDENTIFIER.fields_by_name['identifier']._options = None
  _MODELIDENTIFIER.fields_by_name['identifier']._serialized_options = b'\340A\002\222A\016J\014\"ed542963de\"'
  _MODELIDENTIFIER.fields_by_name['version']._options = None
  _MODELIDENTIFIER.fields_by_name['version']._serialized_options = b'\340A\002\222A\tJ\007\"1.0.1\"'
  _MODELIDENTIFIER.fields_by_name['name']._options = None
  _MODELIDENTIFIER.fields_by_name['name']._serialized_options = b'\340A\003\222A\026J\024\"Sentiment Analysis\"'
  _LISTOPTIONS_FILTERSENTRY._options = None
  _LISTOPTIONS_FILTERSENTRY._serialized_options = b'8\001'
  _LISTOPTIONS_SORTENTRY._options = None
  _LISTOPTIONS_SORTENTRY._serialized_options = b'8\001'
  _PAGE.fields_by_name['page_count']._options = None
  _PAGE.fields_by_name['page_count']._serialized_options = b'\340A\003'
  _PAGE.fields_by_name['total_elements']._options = None
  _PAGE.fields_by_name['total_elements']._serialized_options = b'\340A\003'
  _MODELIDENTIFIER._serialized_start=132
  _MODELIDENTIFIER._serialized_end=296
  _MODELLIBRARY._serialized_start=299
  _MODELLIBRARY._serialized_end=471
  _MODELAUTOSCALINGCONFIG._serialized_start=474
  _MODELAUTOSCALINGCONFIG._serialized_end=642
  _REGISTRY._serialized_start=644
  _REGISTRY._serialized_end=768
  _LISTOPTIONS._serialized_start=771
  _LISTOPTIONS._serialized_end=1061
  _LISTOPTIONS_FILTERSENTRY._serialized_start=946
  _LISTOPTIONS_FILTERSENTRY._serialized_end=1004
  _LISTOPTIONS_SORTENTRY._serialized_start=1006
  _LISTOPTIONS_SORTENTRY._serialized_end=1061
  _PAGINATION._serialized_start=1063
  _PAGINATION._serialized_end=1119
  _PAGE._serialized_start=1122
  _PAGE._serialized_end=1252
# @@protoc_insertion_point(module_scope)
