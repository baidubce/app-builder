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
import copy
base_item_schema = {
  "$schema": "base iter template",
  "type": "object",
  "properties": {
    "type": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "text": {
      "type": "object"
    },
    "visible_scope": {
      "enum": ["llm", "user", "all"]
    },
    "raw_data": {
      "type": "object"
    },
    "usage": {
      "type": "object",
      "properties": {
          "prompt_tokens": {
              "type": "integer"
          },
          "completion_tokens": {
              "type": "integer"
          },
          "total_tokens": {
              "type": "integer"
          },
          "name": {
              "type": "string"
          }
      },
    },
    "metrics": {
      "type": "object",
      "properties": {
        "first_token_time(s)": {
          "type": "number"
        },
        "total_time(s)": {
          "type": "number"
        },
        "memory_used(MB)": {
          "type": "number"
        }
      }
    }
  },
  "required": ["type", "text"]
}

text_schema = copy.deepcopy(base_item_schema)
text_schema["$schema"] = "text_schema"
text_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["text"]
}
text_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
      "info": {
          "type": "string"
      }
  },
  "required": ["info"]
}

code_schema = copy.deepcopy(base_item_schema)
code_schema["$schema"] = "code_schema"
code_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["code"]
}
code_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "code": {
      "type": "string"
    }
  },
  "required": ["code"]
}

file_schema = copy.deepcopy(base_item_schema)
file_schema["$schema"] = "file_schema"
file_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["file"]
}
file_schema["properties"]["text"] = {
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

url_schema = copy.deepcopy(base_item_schema)
url_schema["$schema"] = "url_schema"
url_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["url"]
}
url_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "url": {
      "type": "string"
    }
  },
  "required": ["url"]
}

oral_text_schema = copy.deepcopy(base_item_schema)
oral_text_schema["$schema"] = "oral_text_schema"
oral_text_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["oral_text"]
}
oral_text_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "info": {
      "type": "string"
    }
  },
  "required": ["info"]
}

references_schema = copy.deepcopy(base_item_schema)
references_schema["$schema"] = "references_schema"
references_schema["properties"]["type"] = "references"
references_schema["properties"]["text"] = {
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

image_schema = copy.deepcopy(base_item_schema)
image_schema["$schema"] = "image_schema"
image_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["image"]
}
image_schema["properties"]["text"] = {
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

chart_schema = copy.deepcopy(base_item_schema)
chart_schema["$schema"] = "chart_schema"
chart_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["chart"]
}
chart_schema["properties"]["text"] = {
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

audio_schema = copy.deepcopy(base_item_schema)
audio_schema["$schema"] = "audio_schema"
audio_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["audio"]
}
audio_schema["properties"]["text"] = {
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
  "files": file_schema,
  "urls": url_schema,
  "oral_text": oral_text_schema,
  "references": references_schema,
  "image": image_schema,
  "chart": chart_schema,
  "audio": audio_schema
}

components_tool_eval_output_json_maps = {
    "AnimalRecognition": [text_schema],
    "ASR": [text_schema],
    "TreeMind": [text_schema, url_schema],
    "ImageUnderstand": [text_schema]
}