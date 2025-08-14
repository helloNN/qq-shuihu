from utils.hwnd import GameHwnd


def main():
    game1 = GameHwnd(66708)
    # res = game1.find_childHwnds(66708, include_hidden=True, max_depth=20)
    # for window in res:
    #     print(
    #         f"窗口标题: {window.title}, 句柄: {window.hwnd}, 可见: {window.is_visible}, 最小化: {window.is_minimized}"
    #     )

    # print(res)

    game1.hello()
    game1.click(653, 430, "left")


if __name__ == "__main__":
    main()
