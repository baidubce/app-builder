# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import os
import appbuilder

# SKIP名单中的组件无需检查，直接跳过
SKIP_COMPONENTS = [
]

# 白名单中的组件因历史原因，检查失败，但可以正常使用，因此加入白名单
COMPONENT_WHITE_LIST = [
    "RagWithBaiduSearchPro",
    "RAGWithBaiduSearch",
    "Excel2Figure",
    "MRC",
    "OralQueryGeneration",
    "QAPairMining",
    "SimilarQuestion",
    "StyleWriting",
    "StyleRewrite",
    "TagExtraction",
    "Nl2pandasComponent",
    "QueryRewrite",
    "DialogSummary",
    "HallucinationDetection",
    "Playground",
    "ASR",
    "GeneralOCR",
    "ObjectRecognition",
    "Text2Image",
    "LandmarkRecognition",
    "TTS",
    "ExtractTableFromDoc",
    "DocParser",
    "DocSplitter",
    "BESRetriever",
    "BESVectorStoreIndex",
    "BaiduVDBVectorStoreIndex",
    "BaiduVDBRetriever",
    "TableParams",
    "Reranker",
    "PPTGenerationFromInstruction",
    "PPTGenerationFromPaper",
    "PPTGenerationFromFile",
    "DishRecognition",
    "Translation",
    "AnimalRecognition",
    "DocCropEnhance",
    "QRcodeOCR",
    "TableOCR",
    "DocFormatConverter",
    "Embedding",
    "Matching",
    "NL2Sql",
    "SelectTable",
    "PlantRecognition",
    "HandwriteOCR",
    "ImageUnderstand",
    "MixCardOCR", 
]


def get_component_white_list():
    return COMPONENT_WHITE_LIST

def get_all_components():
    from appbuilder import __COMPONENTS__

    components = {}
    for component in __COMPONENTS__:
        if component in SKIP_COMPONENTS:
            continue

        try:
            component_obj = eval("appbuilder."+component)
            components[component]= {
                "obj": component_obj,
                "import_error": ""
            }
        except Exception as e:
            print("Component: {} import with error: {}".format(component, str(e)))
            components[component]= {
                "obj": None,
                "import_error": str(e)
            }

    return components

if __name__ == '__main__':
    all_components = get_all_components()
    print(all_components)