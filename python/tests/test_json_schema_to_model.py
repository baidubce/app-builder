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
import unittest

from appbuilder.utils.json_schema_to_model import _to_camel_case as to_camel_case

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestJsonSchemaToModel(unittest.TestCase):
    def test_to_camel_case(self):
        model_name = to_camel_case("image_to_3d_vast")
        print(model_name)
        assert model_name == "ImageTo3dVast"

if __name__ == '__main__':
    unittest.main()
