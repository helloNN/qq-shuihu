from utils import Game, Hwnd
from pywinauto import Application
import os
import multiprocessing  # 导入线程包
import time

# 进程列表
processList = []

time_start = time.time()


def do_task(game: Game, order_num: int):
    app = Application(backend="uia").connect(handle=game.hwnd)
    game.count_position(app)

    print(
        " | ".join([game.qq, f"程序初始化耗时: {round(time.time() - time_start, 2)}s"])
    )

    # game.Bianqiang.liehun(30)
    # game.Fuben.zhengzhan(21)
    # game.Zhanzheng.juyi(order_num)
    # game.Other.xiShuXing(100)
    # game.Other.xiShuXing2()

    # 集市只能跑 2个， 启动程序耗时 2.5s - 3s,  59s的时候跑！
    game.Other.jiShi()

    # game.click_more(("天机秘籍", 670, 380), 100)


def more_task():
    print(f"cpu核心数: {os.cpu_count()}")
    global processList
    games = [
        Game(526078, "2548918215"),
        Game(460238, "2468659059"),
        Game(919254, "3305194332"),
    ]

    # 只计算第一个实例的位置，其它实例共用位置
    app1 = Application(backend="uia").connect(handle=games[0].hwnd)
    games[0].count_position(app1)

    current_index = 0

    for game in games:
        # 使用第一个实例的位置
        if current_index != 0:
            game.coordDiff = games[0].coordDiff

        try:
            # 创建进程
            p = multiprocessing.Process(target=do_task, args=(game, current_index))
            processList.append(p)
            # 设置为守护进程，主进程结束，子进程也结束
            p.daemon = True
            # 启动进程
            p.start()
        except Exception as e:
            print(f"index.py | {game.qq} | 任务错误:", e)
        current_index += 1


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
    do_task(game, 0)


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
        # main()
        main("more")
        while True:
            time.sleep(5)
            check_process()

            # print("暂时没有获取的进程")
            # time.sleep(60)

    except KeyboardInterrupt:
        print("\n程序已手动退出")
    except Exception as e:
        print("index.py | 未知错误:", e)
