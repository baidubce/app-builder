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


base_schema = {
  "$schema": "base template",
  "type": "object",
  "properties": {
    "role": {
      "enum": ["tool"]
    },
    "content": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          # "key": {
          #   "type": "string"
          # },
          # "event_id": {
          #   "type": "string"
          # },
          # "sequence_id": {
          #   "type": "integer"
          # },
          "type": {
            "enum": ["text", "code", "file", "url", "oral_text", "references", "image", "chart", "audio"]
          },
          "visible_scope": {
            "enum": ["llm", "user", "all"]
          },
          # "raw_data": {
          #   "type": "object"
          # },
          # "usage": {
          #   "type": "object"
          # },
          # "metrics": {
          #   "type": "object"
          # }
        },
        # "required": ["event_id", "sequence_id", "type"]
        "required": ["type"]
      }
    }
  },
  "required": ["content"]
}

text_schema = base_schema.copy()
text_schema["$schema"] = "text_schema"
text_schema["properties"]["content"]["items"]["properties"]["type"] = "text"
text_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "info": {
      "type": "string"
    }
  },
  "required": ["info"]
}

code_schema = base_schema.copy()
code_schema["$schema"] = "code_schema"
code_schema["properties"]["content"]["items"]["properties"]["type"] = "code"
code_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "code": {
      "type": "string"
    }
  },
  "required": ["code"]
}

file_schema = base_schema.copy()
file_schema["$schema"] = "file_schema"
file_schema["properties"]["content"]["items"]["properties"]["type"] = "file"
file_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "filename": {
      "type": "string"
    },
    "url": {
      "type": "string"
    }
  },
  "required": ["filename", "url"]
}

url_schema = base_schema.copy()
url_schema["$schema"] = "url_schema"
url_schema["properties"]["content"]["items"]["properties"]["type"] = "url"
url_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "url": {
      "type": "string"
    }
  },
  "required": ["url"]
}

oral_text_schema = base_schema.copy()
oral_text_schema["$schema"] = "oral_text_schema"
oral_text_schema["properties"]["content"]["items"]["properties"]["type"] = "oral_text"
oral_text_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "info": {
      "type": "string"
    }
  },
  "required": ["info"]
}

references_schema = base_schema.copy()
references_schema["$schema"] = "references_schema"
references_schema["properties"]["content"]["items"]["properties"]["type"] = "references"
references_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "type": {
      "type": "string"
    },
    "resource_type": {
      "type": "string"
    },
    "doc_id": {
      "type": "string"
    },
    "icon": {
      "type": "string",
    },
    "site_name": {
      "type": "string"
    },
    "content": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "mock_id": {
      "type": "string"
    },
    "from": {
      "type": "string"
    },
    "image_url": {
      "type": "string"
    },
    "video_url": {
      "type": "string"
    }
  },
  "required": ["type", "resource_type", "doc_id", "icon", "site_name", "content", "title", "mock_id", "from", "image_url", "video_url"]
}

image_schema = base_schema.copy()
image_schema["$schema"] = "image_schema"
image_schema["properties"]["content"]["items"]["properties"]["type"] = "image"
image_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "filename": {
      "type": "string"
    },
    "url": {
      "type": "string"
    }
  },
  "required": ["filename", "url"]
}

chart_schema = base_schema.copy()
chart_schema["$schema"] = "chart_schema"
chart_schema["properties"]["content"]["items"]["properties"]["type"] = "chart"
chart_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "filename": {
      "type": "string"
    },
    "url": {
      "type": "string"
    }
  },
  "required": ["filename", "url"]
}

audio_schema = base_schema.copy()
audio_schema["$schema"] = "audio_schema"
audio_schema["properties"]["content"]["items"]["properties"]["type"] = "audio"
audio_schema["properties"]["content"]["items"]["properties"]["text"] = {
  "type": "object",
  "properties": {
    "filename": {
      "type": "string"
    },
    "url": {
      "type": "string"
    }
  },
  "required": ["filename", "url"]
}

type_to_json_schemas = {
  "text": text_schema,
  'code': code_schema,
  "files": file_schema, #files or file
  "urls": url_schema, #urls or url
  "oral_text": oral_text_schema,
  "references": references_schema,
  "image": image_schema,
  "chart": chart_schema,
  "audio": audio_schema
}

components_tool_eval_output_type_maps = {
    "AnimalRecognition": [text_schema],
    "TreeMind": [text_schema, url_schema]
}