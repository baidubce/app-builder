# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

import appbuilder
from appbuilder.core.message import Message


class TestLandmarkRecognition(unittest.TestCase):

    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.landmark_recognition = appbuilder.LandmarkRecognition()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行但测

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        filex = os.path.join(current_dir, 'landmark_recognize_test.png')

        with open(filex, 'rb') as img_file:
            raw_image = img_file.read()

        # Create message with raw_image
        message = Message(content={"raw_image": raw_image})

        # Recognize landmark
        output = self.landmark_recognition.run(message)

        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_no_image(self):
        """
        Testing run method with no image. This should raise a ValueError.

        Args:
            None

        Returns:
            None

        """
        # create empty message
        message = Message(content={})

        # Assert ValueError is raised
        with self.assertRaises(ValueError):
            self.landmark_recognition.run(message)

    def test_run_with_timeout_and_retry(self):
        """
        Testing run method with timeout and retry parameters.

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        filex = os.path.join(current_dir, 'landmark_recognize_test.png')

        with open(filex, 'rb') as img_file:
            raw_image = img_file.read()

        # Create message with raw_image
        message = Message(content={"raw_image": raw_image})

        # Recognize landmark with timeout and retry parameters
        output = self.landmark_recognition.run(message, timeout=5.0, retry=3)

        # Assert output is not None
        self.assertIsNotNone(output)


if __name__ == '__main__':
    unittest.main()

