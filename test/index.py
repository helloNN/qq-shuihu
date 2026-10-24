import threading
import time

cond = threading.Condition()
data = None


# A发数据
def thread_a():
    global data
    time.sleep(1)

    with cond:
        data = "A 用 Condition 发给 B"
        cond.notify()  # 通知B
    print("A 已通知")


# B等通知 + 收数据
def thread_b():
    global data
    print("B 等待通知...")

    with cond:
        cond.wait()  # 阻塞等A

        print(f"B 收到：{data}")


if __name__ == "__main__":
    t1 = threading.Thread(target=thread_a)
    t2 = threading.Thread(target=thread_b)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
