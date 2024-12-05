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
    "TreeMind"
] # NOQA