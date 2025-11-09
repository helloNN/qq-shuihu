from utils import Game, Hwnd
from pywinauto import Application
import os
import multiprocessing  # 导入线程包
import time

# 进程列表
processList = []


def do_task(game: Game):
    app = Application(backend="uia").connect(handle=game.hwnd)
    game.count_position(app)
    # game.Bianqiang.liehun(30)
    # game.Fuben.zhengzhan(20)
    # game.Zhanzheng.juyi()
    # game.Other.xiShuXing(100)
    game.Other.xiShuXing2()

    # game.click_more(("天机秘籍", 670, 380), 100)


def more_task():
    print(f"cpu核心数: {os.cpu_count()}")
    global processList
    games = [
        Game(197810, "2548918215"),
        Game(132338, "2468659059"),
        Game(197888, "3305194332"),
    ]

    for game in games:
        try:
            # 创建进程
            p = multiprocessing.Process(target=do_task, args=(game,))
            processList.append(p)
            # 设置为守护进程，主进程结束，子进程也结束
            p.daemon = True
            # 启动进程
            p.start()
            time.sleep(1)  # 避免同时操作一个号
        except Exception as e:
            print(f"index.py | {game.qq} | 任务错误:", e)


def single_task():
    # 1.查找窗口
    game = Game()
    hwnd = Hwnd.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")
    if hwnd is None:
        game.logger.error("未找到窗口")
        return
    game.logger.info(f"{hwnd} | 找到窗口")
    game.set_hwnd(hwnd)

    # 2.执行操作
    do_task(game)


# 是否还有进程在处理任务
def check_process() -> bool:
    global processList
    """类似js的every方法"""


# 后续思路， 通过 handle 得到多个 app ，然后处理
# handle 手动获取, 目前无法通过代码一次夺取全都符合条件的窗口句柄
# 图像识别
def main(mode="single"):
    if mode == "single":
        single_task()
    else:
        # 多窗口
        more_task()


if __name__ == "__main__":
    try:
        main()
        # main("more")
        while True:
            time.sleep(5)
            check_process()

            # print("暂时没有获取的进程")
            # time.sleep(60)

    except KeyboardInterrupt:
        print("\n程序已手动退出")
    except Exception as e:
        print("index.py | 未知错误:", e)
