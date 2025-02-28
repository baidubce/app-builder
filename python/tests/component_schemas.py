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
    "enum": ["files"]
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
    "enum": ["urls"]
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
references_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["references"]
}
references_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "type": {
      "type": "string"
    },
    "doc_id": {
      "type": "string"
    },
    "content": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "source": {
      "type": "string"
    },
    "extra": {
      "type": "object"
    }
  },
  "required": ["type", "doc_id", "content", "title", "source"]
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
    },
    "base64": {
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
    "type": {
      "type": "string"
    },
    "data": {
      "type": "string"
    }
  },
  "required": ["type", "data"]
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
    },
    "base64": {
      "type": "string"
    }
  },
  "required": ["filename", "url"]
}

json_schema = copy.deepcopy(base_item_schema)
json_schema["$schema"] = "json_schema"
json_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["json"]
}
json_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "data": {
      "type": "string"
    }
  },
  "required": ["data"]
}

plan_schema = copy.deepcopy(base_item_schema)
plan_schema["$schema"] = "plan_schema"
plan_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["plan"]
}
plan_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "detail": {
      "type": "string"
    },
    "steps": {
      "type": "array",
      "items": {
          "type": "object",
          "properties": {
              "name": {"type": "string"},
              "arguments": {
                "type": "object",
                "additionalProperties": True
              }
          },
          "required": ["name", "arguments"]
      }
    }
  },
  "required": ["detail", "steps"]
}


function_call_schema = copy.deepcopy(base_item_schema)
function_call_schema["$schema"] = "function_call_schema"
function_call_schema["properties"]["type"] = {
    "type": "string",
    "enum": ["function_call"]
}
function_call_schema["properties"]["text"] = {
  "type": "object",
  "properties": {
    "thought": {
      "type": "string"
    },
    "name": {
      "type": "string",
    },
    "arguments": {
      "type": "object",
      "additionalProperties": True
    }
  },
  "required": ["thought", "name", "arguments"],
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
  "audio": audio_schema,
  "json": json_schema,
  "plan": plan_schema,
  "function_call": function_call_schema,
}