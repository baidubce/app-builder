# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# -*- coding: utf-8 -*-
"""
基于Baidu VDB的retriever
"""
import os
import time
from typing import Dict, Any
from appbuilder.core.component import Message
from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.constants import GATEWAY_URL

DEFAULT_ACCOUNT = "root"
DEFAULT_DATABASE_NAME = "AppBuilderDatabase"
DEFAULT_TABLE_NAME = "AppBuilderTable"
DEFAULT_TIMEOUT_IN_MILLS: int = 30 * 1000

DEFAULT_PARTITION = 1
DEFAULT_REPLICA = 3
DEFAULT_INDEX_TYPE = "HNSW"
DEFAULT_METRIC_TYPE = "L2"

DEFAULT_HNSW_M = 16
DEFAULT_HNSW_EF_CONSTRUCTION = 200
DEFAULT_HNSW_EF = 10

DEFAULT_BATCH_SIZE = 1000

FIELD_ID: str = "id"
FIELD_TEXT: str = "text"
FIELD_VECTOR: str = "vector"
FIELD_METADATA: str = "metadata"
INDEX_VECTOR: str = "vector_idx"

VALUE_NONE_ERROR = "Parameter `{}` can not be None."
NOT_SUPPORT_INDEX_TYPE_ERROR = (
    "Unsupported index type: `{}`, supported index types are {}"
)
NOT_SUPPORT_METRIC_TYPE_ERROR = (
    "Unsupported metric type: `{}`, supported metric types are {}"
)
