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

# 返回类型为text的非流式schema定义
text_non_stream_schema = {
    "type": "object",
    "properties": {
        "role": {"type": "string"},
        "content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["text"]
                    },
                    "text": {"type": "string"},
                    "visible_scope": {
                        "type": "string",
                        "enum": ["llm", "user", "all"]
                    }
                },
                "required": ["type", "text", "visible_scope"]
            }
        }
    },
    "required": ["role", "content"]
}

# 返回类型为text的流式的schema
text_stream_schema = {
    "allOf": [
        text_not_stream_schema,
        {
            "properties": {
                "event_status": {
                    "type": "string",
                    "enum": ["interrupt", "preparing", "running"]
                }
            },
            "required": ["event_status"]
        }
    ]
}

components_tool_eval_output_type_maps = {
    "AnimalRecognition": [text_non_stream_schema, text_stream_schema]
}