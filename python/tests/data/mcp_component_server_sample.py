# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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

from appbuilder.mcp_server.server import MCPComponentServer

if __name__ == "__main__":
    from appbuilder.core.components.v2 import (
        Translation,
        StyleWriting,
        OralQueryGeneration,
        
    )

    server = MCPComponentServer(name="AB Component Server")

    model = "ERNIE-4.0-8K"
    server.add_component(Translation())  
    server.add_component(StyleWriting(model=model))  
    server.add_component(
        OralQueryGeneration(model=model)
    )

    server.run()
