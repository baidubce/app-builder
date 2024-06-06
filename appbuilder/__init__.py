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


__version__ = '0.8.0'

import sys
import copy
import pydantic


class PythonVersionChecker:
    def __init__(self):
        self.min_version = (3, 9)
        self.current_version = sys.version_info
        self.check_version()

    def check_version(self):
        if self.current_version < self.min_version:
            raise EnvironmentError(
                f"Mismatched Python version. Expected Python version >= {self.min_version[0]}.{self.min_version[1]}, "
                f"Got Python version {self.current_version[0]}.{self.current_version[1]}.")


# Creating an instance to test the function
checker = PythonVersionChecker()
checker.current_version


class SDKReportConfig(pydantic.BaseModel):
    appbuilder_sdk_version: str = __version__
    appbuilder_sdk_language: str = "python"


# report information
default_header = {
    "X-Appbuilder-Sdk-Config": SDKReportConfig().model_dump_json(),
    "X-Appbuilder-Origin": 'appbuilder_sdk'
}


def get_default_header():
    return copy.deepcopy(default_header)


from .core import *
from .core.components.rag_with_baidu_search_pro import RagWithBaiduSearchPro
from .core.components.rag_with_baidu_search import RAGWithBaiduSearch
from .core import console
from .core.components.excel2figure import Excel2Figure
from .core.components.llms.mrc import MRC
from .core.components.llms.oral_query_generation import OralQueryGeneration
from .core.components.llms.qa_pair_mining import QAPairMining
from .core.components.llms.similar_question import SimilarQuestion
from .core.components.llms.style_writing import StyleWriting
from .core.components.llms.style_rewrite import StyleRewrite
from .core.components.llms.tag_extraction import TagExtraction
from .core.components.llms.nl2pandas import Nl2pandasComponent
from .core.components.llms.query_rewrite import QueryRewrite
from .core.components.llms.dialog_summary import DialogSummary
from .core.components.llms.is_complex_query import IsComplexQuery
from .core.components.llms.query_decomposition import QueryDecomposition
from .core.components.llms.hallucination_detection import HallucinationDetection
from .core.components.llms.playground import Playground

from .core.components.asr.component import ASR
from .core.components.general_ocr.component import GeneralOCR
from .core.components.object_recognize.component import ObjectRecognition
from .core.components.text_to_image.component import Text2Image
from .core.components.landmark_recognize.component import LandmarkRecognition
from .core.components.tts.component import TTS
from .core.components.extract_table.component import ExtractTableFromDoc
from .core.components.doc_parser.doc_parser import DocParser, ParserConfig
from .core.components.doc_splitter.doc_splitter import DocSplitter
from .core.components.retriever.bes.bes_retriever import BESRetriever
from .core.components.retriever.bes.bes_retriever import BESVectorStoreIndex
from .core.components.retriever.baidu_vdb.baiduvdb_retriever import BaiduVDBVectorStoreIndex
from .core.components.retriever.baidu_vdb.baiduvdb_retriever import BaiduVDBRetriever
from .core.components.retriever.baidu_vdb.baiduvdb_retriever import TableParams

from .core.components.dish_recognize.component import DishRecognition
from .core.components.translate.component import Translation
from .core.components.animal_recognize.component import AnimalRecognition
from .core.components.doc_crop_enhance.component import DocCropEnhance
from .core.components.qrcode_ocr.component import QRcodeOCR
from .core.components.table_ocr.component import TableOCR
from .core.components.doc_format_converter.component import DocFormatConverter

from .core.components.embeddings import Embedding
from .core.components.matching import Matching

from .core.components.gbi.nl2sql.component import NL2Sql
from .core.components.gbi.select_table.component import SelectTable

from .core.components.plant_recognize.component import PlantRecognition
from .core.components.handwrite_ocr.component import HandwriteOCR
from .core.components.image_understand.component import ImageUnderstand
from .core.components.mix_card_ocr.component import MixCardOCR

from appbuilder.core.message import Message
from appbuilder.core.agent import AgentRuntime
from appbuilder.core.user_session import UserSession

from appbuilder.utils.logger_util import logger

from appbuilder.core.utils import get_model_list

from appbuilder.core.console.appbuilder_client.appbuilder_client import AppBuilderClient
from appbuilder.core.console.appbuilder_client.appbuilder_client import AgentBuilder

from .core._exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    PreconditionFailedException,
    InternalServerErrorException,
    HTTPConnectionException,
    AppBuilderServerException,
)

from appbuilder.core.assistant.base import assistant
from appbuilder.core.assistant.threads.runs import StreamRunContext
from appbuilder.core.assistant.threads.runs import AssistantEventHandler
from appbuilder.core.assistant.threads.runs import AssistantStreamManager

__all__ = [
    'logger',

    'BadRequestException',
    'ForbiddenException',
    'NotFoundException',
    'PreconditionFailedException',
    'InternalServerErrorException',
    'HTTPConnectionException',
    'AppBuilderServerException',

    'StyleWriting',
    'MRC',
    'Playground',
    'OralQueryGeneration',
    'QAPairMining',
    'SimilarQuestion',
    'IsComplexQuery',
    'QueryDecomposition',
    'TagExtraction',
    'StyleRewrite',
    'QueryRewrite',
    'DialogSummary',
    'ASR',
    'GeneralOCR',
    'ObjectRecognition',
    'Text2Image',
    'LandmarkRecognition',
    'TTS',
    "ExtractTableFromDoc",
    "DocParser",
    "ParserConfig",
    "DocSplitter",
    "BESRetriever",
    "BESVectorStoreIndex",
    "BaiduVDBVectorStoreIndex",
    "BaiduVDBRetriever",
    "TableParams",
    "HallucinationDetection",

    'DishRecognition',
    'Translation',
    'Message',
    'AnimalRecognition',
    'DocCropEnhance',
    'QRcodeOCR',
    'TableOCR',

    'Embedding',

    'Matching',

    "PlantRecognition",
    "HandwriteOCR",
    "ImageUnderstand",
    "MixCardOCR",
    "AppBuilderClient",
    "AgentBuilder",

    "assistant",
    "StreamRunContext",
    "AssistantEventHandler",
    "AssistantStreamManager"
]
