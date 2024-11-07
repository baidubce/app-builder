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
import time

import appbuilder

os.environ["APPBUILDER_TOKEN"] = "密钥"
app_id = "应用ID"

if __name__ == "__main__":
    builder = appbuilder.AppBuilderClient(app_id)
    stream = True  # 控制是否执行流式输出
    not_stream = True  # 控制是否执行非流式输出

    if not_stream:
        conversation_id = builder.create_conversation()
        start = time.time()
        msg = builder.run(conversation_id, "如何运用胯下变向进行突破？", )
        answer = msg.content.answer.replace("\n", "")
        print("----------------非流式输出篮球教练回答内容----------------")
        i = 0
        step = 30
        while i + step < len(answer):
            print(answer[i: i + step])
            i += step
        print(answer[i:len(answer)])
        end = time.time()
        print("-----------------非流式输出耗时------------------")
        print("%.2f秒" % (end - start))

    print("\n")

    if stream:
        conversation_id = builder.create_conversation()

        start = time.time()
        msg = builder.run(conversation_id, "如何运用胯下变向进行突破？", stream=True)
        costs = []
        print("----------------流式输出篮球教练回答内容----------------")
        i = 0
        step = 30
        answer = ""
        for c in msg.content:
            costs.append("%.2f秒" % (time.time() - start))
            answer += c.answer.replace("\n", "")
            if len(answer) - i > step:
                print(answer[i: i + step])
                i += step
        while i + step < len(answer):
            print(answer[i: i + step])
            i += step
        print(answer[i:len(answer)])
        print("------------流式输出耗时序列------------")
        print(costs)
