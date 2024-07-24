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
import argparse
import time
from typing import Optional


parser = argparse.ArgumentParser()
parser.add_argument("--host",  type=str, default="127.0.0.1", help="phoenix服务的url地址")
parser.add_argument("--port", type=int, default=8080, help="phoenix服务的端口号")
parser.add_argument("--timeout", type=float, default=None, help="phoenix服务的运行时间，不填写则为常驻服务，单位为秒")


def launch_phoenix(host: Optional[str] = "127.0.0.1", port: Optional[int] = 8080, **kwargs):
    """
    启动Phoenix
    Launch Phoenix
    """
    try:
        import phoenix
    except ModuleNotFoundError:
        raise ImportError(
            "尚未安装phoenix组件，尝试使用 python3 -m pip install arize-phoenix==4.5.0 -i https://pypi.tuna.tsinghua.edu.cn/simple 安装该组件")
    session = phoenix.launch_app(**kwargs)
    return session

def stop_phoenix(delete_data:bool=False):
    """
    停止Phoenix
    Stop Phoenix
    """
    try:
        import phoenix
    except ModuleNotFoundError:
        raise ImportError(
            "尚未安装phoenix组件，尝试使用 python3 -m pip install arize-phoenix==4.5.0 -i https://pypi.tuna.tsinghua.edu.cn/simple 安装该组件")
    phoenix.stop_app(delete_data)

def runtime_main():
    """
    运行主程序
    Run main program
    """ 
    args = parser.parse_args()
    os.environ['PHOENIX_PORT'] = str(args.port)
    os.environ['PHOENIX_HOST'] = args.host
    timeout = args.timeout
    print(" Launching AppBuilder Tracer Server By Phoenix... ")
    print(" Arguments: ", args)
    session = launch_phoenix()
    while True:
        if timeout is not None:
            time.sleep(timeout)
            break
        time.sleep(1)
    stop_phoenix()


if __name__ == "__main__":
    runtime_main()
