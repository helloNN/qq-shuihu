from utils import Game, Hwnd
from pywinauto import Application
import os
import multiprocessing  # 导入线程包
import time

# 进程列表
processList = []


class TaskOption:
    def __init__(self, game: Game, order_num: int, lock, setup_time: int = 0):
        self.game = game
        self.order_num = order_num
        self.setup_time = setup_time
        self.global_lock = lock


def do_task(option: TaskOption):
    """
    任务

    :param option:配置参数

    :param option.game: 游戏实例
    :param option.order_num: 进程顺序
    :param option.setup_time: 启动耗时，单位秒
    :param option.global_lock: 全局进程锁
    :return none:
    """
    time_start = time.time()
    app = Application(backend="uia").connect(handle=option.game.hwnd)
    option.game.count_position(app, True, option.global_lock)
    setup_time2 = time.time() - time_start
    game = option.game

    print(
        " | ".join(
            [
                game.qq,
                f"程序初始化耗时: {round(option.setup_time if option.setup_time>0 else setup_time2, 2)}s",
            ]
        )
    )

    # game.Bianqiang.liehun(500)
    # game.Fuben.zhengzhan(21)
    # game.Zhanzheng.juyi(order_num)
    # game.Other.xiShuXing100(150)
    # game.Other.xiShuXing1()
    game.ZuDui.shenKun(option.order_num)

    # 集市只能跑 2个， 启动程序耗时 1.8s,  59s的时候跑！
    # game.Other.jiShi()

    # game.click_more(("天机秘籍", 670, 380), 300)
    # game.click_more(("背包-使用", 285, 218), 200)

    # game.Test.test_write(("请输入道具名称", 596, 120), 1000)
    # game.Test.test_log()

    # game.logger.info(f"{game.qq} | hello world | {id(game.logger)}")
    # game.count_position(123)


def more_task(lock):
    print(f"cpu核心数: {os.cpu_count()}")
    global processList
    games = [
        Game(721384, "2548918215"),
        Game(460704, "2468659059"),
        Game(591408, "3305194332"),
        Game(722338, "3492175458"),
        # Game(460920, "3492175458"),
        # Game(329834, "3118728968"),
    ]

    # 只计算第一个实例的位置，其它实例共用位置
    time_start = time.time()
    app1 = Application(backend="uia").connect(handle=games[0].hwnd)
    games[0].count_position(app1)
    setup_time = time.time() - time_start

    current_index = 0

    for game in games:
        # 使用第一个实例的位置
        if current_index != 0:
            game.coordDiff = games[0].coordDiff

        try:
            # 创建进程
            p = multiprocessing.Process(
                target=do_task,
                args=(TaskOption(game, current_index, lock, setup_time),),
            )
            processList.append(p)
            # 设置为守护进程，主进程结束，子进程也结束
            p.daemon = True
            # 启动进程
            p.start()
        except Exception as e:
            print(f"index.py | {game.qq} | 任务错误:", e)
        current_index += 1


def single_task(lock):
    # 1.查找窗口
    game = Game()
    hwnd = Hwnd.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")
    if hwnd is None:
        print("未找到窗口")
        return
    print(f"{hwnd} | 找到窗口")
    game.set_hwnd(hwnd)

    # 2.执行操作
    do_task(TaskOption(game, 0, lock))


# 是否还有进程在处理任务
def check_process() -> bool:
    global processList
    """类似js的every方法"""


# 后续思路， 通过 handle 得到多个 app ，然后处理
# handle 手动获取, 目前无法通过代码一次夺取全都符合条件的窗口句柄
# 图像识别
def main(mode="single"):
    global_lock = multiprocessing.Lock()

    if mode == "single":
        single_task(global_lock)
    else:
        # 多窗口
        more_task(global_lock)


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
