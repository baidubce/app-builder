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


class Runs():
    def run(self, assistant_id: str, conversation_id: str, assistant_config = None,extra_conversation =None, tool_output = None) -> RunResult:
        pass

    def stream_run(self, assistant_id: str, conversation_id: str, assistant_config = None,extra_conversation =None, tool_output = None) -> StreamrRunResult:
        pass

    def submit_tool_output(self, run_id: str, conversation_id:str, tool_outputs, stream:bool=False) -> RunResult:
        pass

    def cancel(self, run_id: str) -> RunResult:
        pass





