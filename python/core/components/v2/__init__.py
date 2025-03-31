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

from .animal_recognize.component import AnimalRecognition
from .image_understand.component import  ImageUnderstand
from .translate.component import Translation
from .general_ocr.component import GeneralOCR
from .llms.style_rewrite.component import StyleRewrite
from .llms.hallucination_detection.component import HallucinationDetection
from .qrcode_ocr.component import QRcodeOCR
from .handwrite_ocr.component import HandwriteOCR
from .mix_card_ocr.component import MixCardOCR
from .table_ocr.component import TableOCR
from .text_to_image.component import Text2Image
from .llms.style_writing.component import StyleWriting
from .tree_mind.component import TreeMind
from .asr.component import ASR
from .object_recognize.component import ObjectRecognition
from .llms.similar_question.component import SimilarQuestion
from .llms.oral_query_generation.component import OralQueryGeneration
from .plant_recognize.component import PlantRecognition
from .llms.query_rewrite.component import QueryRewrite
from .llms.nl2pandas.component import Nl2pandasComponent
from .llms.dialog_summary.component import DialogSummary
from .llms.mrc.component import MRC
from .llms.is_complex_query.component import IsComplexQuery
from .llms.qa_pair_mining.component import QAPairMining
from .llms.query_decomposition.component import QueryDecomposition
from .llms.tag_extraction.component import TagExtraction

__V2_COMPONENTS__ = [
    "AnimalRecognition",
    "ImageUnderstand",
    "Translation",
    "GeneralOCR",
    "StyleRewrite",
    "HallucinationDetection",
    "QRcodeOCR",
    "HandwriteOCR",
    "MixCardOCR",
    "TableOCR",
    "Text2Image",
    "StyleWriting",
    "TreeMind",
    "ASR",
    "ObjectRecognition",
    "SimilarQuestion",
    "OralQueryGeneration",
    "PlantRecognition",
    "QueryRewrite",
    "Nl2pandasComponent",
    "DialogSummary",
    "MRC",
    "IsComplexQuery",
    "QAPairMining",
    "QueryDecomposition",
    "TagExtraction"
] # NOQA