from utils import Game, Hwnd
from pywinauto import Application


def do_task(game):
    game.beibao.liehun()


# 后续思路， 通过 handle 得到多个 app ，然后处理
# handle 手动获取, 目前无法通过代码一次夺取全都符合条件的窗口句柄
def main():
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


if __name__ == "__main__":
    main()
