from pywinauto import Application

# 连接到顶层窗口
app = Application(backend="uia").connect(title="MainWindow")
main_window = app.window(title="MainWindow")

# 打印所有子控件（递归遍历）
main_window.print_control_identifiers()
