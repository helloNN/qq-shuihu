from utils.hwnd import GameHwnd
from pywinauto import Application


def main():
    game1 = GameHwnd()
    hwnd = game1.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")
    print(f"找到的窗口句柄: {hwnd}")

    if hwnd is None:
        return

    app = Application(backend="uia").connect(handle=hwnd)
    mainWindow = app.MainWindow

    qq254 = mainWindow.child_window(
        title="2548918215", auto_id="btnTab", control_type="Button"
    )
    qq24686 = mainWindow.child_window(
        title="醒来，遇见你", auto_id="btnTab", control_type="Button"
    )
    qq3305 = mainWindow.child_window(
        title="nn", auto_id="btnTab", control_type="Button"
    )
    # qq254.print_control_identifiers()
    # qq24686.print_control_identifiers()
    # qq3305.print_control_identifiers()

    sixBar = mainWindow.child_window(auto_id="nav1", control_type="List")
    # sixBar.print_control_identifiers()
    guanfangWeb = sixBar.child_window(title="官方网站", control_type="Hyperlink")
    rect = guanfangWeb.rectangle()
    # print(guanfangWeb.rectangle())

    origin = (rect.left, rect.bottom)
    print(f"游戏原点: {origin}")

    flash_content = app.window(auto_id="flashContent", control_type="Group")
    if flash_content.exists():
        print("找到了 flashContent")
    else:
        print("没有找到 flashContent")

    # gameWindow.drwaw_outline(colour="red", thickness=2)
    # xx = mainWindow.Pane2
    # xx.print_control_identifiers()

    # mainWindow.print_control_identifiers()
    # print(app.windows())
    # game1.set_hwnd(hwnd)

    # game1.click(985, 155, "left")


if __name__ == "__main__":
    main()
