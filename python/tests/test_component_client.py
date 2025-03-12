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
import unittest
import appbuilder
import os


#unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestComponentCLient(unittest.TestCase):
    def test_component_client(self):
        appbuilder.logger.setLoglevel("DEBUG")
        client = appbuilder.ComponentClient()

        res = client.run(component_id="44205c67-3980-41f7-aad4-37357b577fd0",
                         version="latest", sys_origin_query="北京景点推荐")
        print(res.content)

    def test_component_client_stream(self):
        appbuilder.logger.setLoglevel("DEBUG")
        client = appbuilder.ComponentClient()

        res = client.run(component_id="44205c67-3980-41f7-aad4-37357b577fd0",
                         version="latest", sys_origin_query="北京景点推荐", stream=True)
        for data in res.content:
            print(data)


if __name__ == "__main__":
    unittest.main()
