from utils.hwnd import GameHwnd
from pywinauto import Application


def getPosition(rect):
    return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)


# 后续思路， 通过 handle 得到多个 app ，然后处理
# handle 手动获取, 目前无法通过代码一次夺取全都符合条件的窗口句柄
def main():
    game1 = GameHwnd()
    hwnd = game1.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")
    print(f"找到的窗口句柄: {hwnd}")

    if hwnd is None:
        return

    app = Application(backend="uia").connect(handle=hwnd)
    mainWindow = app.MainWindow
    # mainWindow.print_control_identifiers()

    # 联系官方，下面那块区域
    contactArea = mainWindow.child_window(
        auto_id="windowsFormsHost", control_type="Pane"
    )
    contactAreaRect = contactArea.rectangle()
    print(f"联系官方：下面整块区域: {getPosition(contactAreaRect)}")
    # contactArea.click_input(coords=(528, 366))     可以正常点击

    # 游戏内falsh区域
    flashArea = mainWindow["Custom4"]
    flashAreaRect = flashArea.rectangle()
    print(f"游戏坐标信息: {getPosition(flashAreaRect)}")
    # flashArea.click_input(coords=(546, 328))         也可以点击


if __name__ == "__main__":
    main()
