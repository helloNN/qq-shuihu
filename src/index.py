from utils.hwnd import GameHwnd


def main():
    game1 = GameHwnd(328922)
    # res = game1.find_childHwnds(66708, include_hidden=True, max_depth=20)
    # for window in res:
    #     print(
    #         f"窗口标题: {window.title}, 句柄: {window.hwnd}, 可见: {window.is_visible}, 最小化: {window.is_minimized}"
    #     )

    # print(res)
    hwnd = game1.find_hwndByTitle_p_child("MainWindow", "Chrome Legacy Window")

    game1.hello()
    print(f"获取到的窗口句柄: {hwnd}")
    # game1.click(653, 430, "left")


if __name__ == "__main__":
    main()
