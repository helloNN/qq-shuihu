from utils import Game, Hwnd
from pywinauto import Application


def do_task(game):
    game.beibao.liehun()


def more_task():
    games = [
        Game(918842, "2548918215"),
        Game(525474, "2468659059"),
        Game(263250, "3305194332"),
    ]

    for game in games:
        app = Application(backend="uia").connect(handle=game.hwnd)
        game.count_position(app)


def single_task():
    # 1.查找窗口
    game = Game()
    hwnd = Hwnd.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")
    if hwnd is None:
        game.logger.error("未找到窗口")
        return
    game.logger.info(f"{hwnd} | 找到窗口")
    game.set_hwnd(hwnd)

    # 2.连接窗口 && 计算位置
    app = Application(backend="uia").connect(handle=hwnd)
    game.count_position(app)

    # 3.执行操作
    do_task(game)


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
        main("more")
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(e)
