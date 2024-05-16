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

os.environ["APPBUILDER_TOKEN"] = "密钥"


class IdiomSolitaire:
    def __init__(self, real_player, app_id1, app_id2):
        self.player1 = appbuilder.AppBuilderClient(app_id1)
        self.player2 = appbuilder.AppBuilderClient(app_id2)
        self.real_player = real_player

    def run(self):
        conversation_id1 = self.player1.create_conversation()
        conversation_id2 = self.player2.create_conversation()
        if self.real_player:
            print("---------游戏开始，请输入一个成语---------")
            q = str(input("真实玩家: "))
        else:
            q = "龙年大吉"
        i = 1
        while True:
            print("----------第%d轮比拼----------" % (i,))
            msg = self.player1.run(conversation_id1, q)
            answer = msg.content.answer
            print("LLM玩家1: ", answer)
            # answer作为下一个玩家的输入
            q = answer

            msg = self.player2.run(conversation_id2, q)
            answer = msg.content.answer
            print("LLM玩家2: ", msg.content.answer)
            q = answer
            if self.real_player:
                q = str(input("真实玩家: "))
            i += 1


# 无真实玩家
def main1():
    idiom_solitaire = IdiomSolitaire(False, "应用ID",
                                     "应用ID")
    idiom_solitaire.run()


# 真实玩家
def main2():
    idiom_solitaire = IdiomSolitaire(True, "应用ID",
                                     "应用ID")
    idiom_solitaire.run()


if __name__ == "__main__":
    main1()
    # main2()