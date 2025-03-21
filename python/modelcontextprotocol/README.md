### Baidu AISearch MCP Server

An MCP server implementation that integrates the Baidu AI search API, providing  web search capabilities and summary of LLM. The Baidu AI Search Component combines Baidu Search capabilities with large model technology, providing intelligent response functions with real-time information from the entire network, and supporting a variety of industry scenarios.

### Features

* **Integration of Search and Large Model Technology**: The component seamlessly merges Baidu’s powerful search engine with advanced large model technology, enabling intelligent and contextually aware responses.
* **Real-time Information Access**: It provides users with up-to-date information from across the internet, ensuring relevant and timely replies.
* **Versatile Applications**: The component caters to a wide range of industries and scenarios, offering flexible solutions for various use cases.
* **Standardized and Customizable Features**: Users can customize personas, choose from different models, rewrite questions for enhanced search results, configure search scopes, and specify the number of reference links, among other options.
* **Enhanced Performance and Availability**: The API delivers high performance and reliability, ensuring smooth and uninterrupted service.
* **Comprehensive Content Safety**: With rigorous content safety reviews, the component ensures all responses and information remain compliant and within acceptable standards.

### Tools

* AIsearch
  * Execute web searches with pagination and filtering
  * Inputs:
    - query (str): The search request.
    - stream (bool, optional): Whether to receive response data in streaming format. Defaults to False.
    - instruction (Instruction, optional): Instruction information object. Defaults to None.
    - temperature (float, optional): Temperature parameter to control the randomness of generated text. Defaults to 1e-10.
    - top_p (float, optional): Cumulative probability threshold for controlling the diversity of generated text. Defaults to 1e-10.
    - search_top_k (int, optional): The number of search candidate results. Defaults to 4.
    - hide_corner_markers (bool, optional): Whether to hide the boundary markers in the response. Defaults to True.

### Configuration

#### Getting an API Key

You can refer to this webpage https://cloud.baidu.com/doc/AppBuilder/s/klv2eywua to obtain the api_key

#### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

##### python

```json
{
  "mcpServers": {
    "AB Component Server": {
      "command": "/path/to/your/python3.12",
      "args": [
        "/path/to/your/ai_search_server.py"
      ],
      "envs": {
        "APPBUILDER_TOKEN": "your token"
      }
    }
  }
}
```

#### Usage with Cursor

```json
{
    "mcpServers": {
        "AISearch": {
            "url": "http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key={your token}"
        }
    }
}
```

### License

Copyright (c) 2024 Baidu, Inc. All Rights Reserved.  Licensed under the Apache License, Version 2.0 (the "License");  you may not use this file except in compliance with the License.  You may obtain a copy of the License at      http://www.apache.org/licenses/LICENSE-2.0  Unless required by applicable law or agreed to in writing, software  distributed under the License is distributed on an "AS IS" BASIS,  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the specific language governing permissions and  limitations under the License.