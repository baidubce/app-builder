import time
import phoenix
import threading

def start_app_in_thread():
    phoenix.launch_app()

def launch_tracer(on_time=3600):
    # 启动一个线程来运行应用
    app_thread = threading.Thread(target=start_app_in_thread)
    app_thread.start()
    
    # 主线程等待指定的时间（如果需要的话）
    time.sleep(on_time)




