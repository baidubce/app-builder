# Baidu AI Search

Baidu AI Search component combines Baidu's search capabilities with large language model technology to provide intelligent responses with real-time web information references, supporting various industry application scenarios. It offers rich standardized capabilities such as:

- Custom persona settings
- Model selection 
- Query rewriting (including time-sensitive and multi-turn approaches to enhance search results)
- Search scope configuration (choice of modalities, site ranges and publication dates)
- Customizable number of reference links

## Quick Start

1. Get your AppBuilder API Key from the console
2. Format your authorization token as: `Bearer+<AppBuilder API Key>` (keep the "+" in between)
3. Config with

  {
    "mcpServers": {
      "baidu_ai_search": {
        "url": "http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key=Bearer+bce-v3/ALTAK..."
      }
    }
  }


For more details, please refer to: https://cloud.baidu.com/doc/AppBuilder/s/zm8pn5cju