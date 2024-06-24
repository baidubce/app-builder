import time 
from typing import Optional

def tracer_launch(worktime:Optional[int] = None):
    try:
        import phoenix
    except ImportError:
        raise("\n请使用phoenix.sh脚本安装phoenix\nPlease use the phoenix.sh script to install Phoenix.")
    if worktime:
        phoenix.launch_app()
        time.sleep(worktime)
    if not worktime:
        phoenix.launch_app()
        try:
            # 使用无限循环阻塞
            while True:
                pass
        except KeyboardInterrupt:
            # 捕获键盘中断，以便可以通过Ctrl+C退出
            print("Interrupted by user")



