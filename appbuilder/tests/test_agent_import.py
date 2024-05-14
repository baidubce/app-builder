import os
import sys
import unittest
import subprocess
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime,
)


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        pass

    def test_chainlit_agent_import_failed(self):
        """测试import chainlit失败"""
        component = Component()
        agent = AgentRuntime()
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y", "chainlit"]
        )
        with self.assertRaises(ImportError):
            agent.chainlit_agent()
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chainlit"])


if __name__ == "__main__":
    unittest.main()
