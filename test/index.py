import json
from pywinauto import Application
import sys
import psutil


# 可选：辅助函数计算元素总数
def count_elements(data):
    """递归计算JSON结构中的元素数量"""
    if not isinstance(data, dict):
        return 0

    count = 1  # 当前元素
    if "children" in data:
        for child in data["children"]:
            count += count_elements(child)
    return count


def dump_to_json(element, filename, depth=10):
    """将控件树结构输出为JSON格式"""

    def element_to_dict(elem, current_depth):
        """递归将控件元素转换为字典"""
        if current_depth > depth:
            return None

        try:
            # 获取控件基本属性
            elem_dict = {
                "title": elem.window_text() or "",
                "class_name": elem.class_name(),
                "control_type": elem.element_info.control_type,
                "automation_id": elem.automation_id() or "",
                "handle": elem.handle,
                "rectangle": {
                    "left": elem.rectangle().left,
                    "top": elem.rectangle().top,
                    "right": elem.rectangle().right,
                    "bottom": elem.rectangle().bottom,
                },
                "is_visible": elem.is_visible(),
                "is_enabled": elem.is_enabled(),
                "children": [],
            }

            # 添加更多属性
            elem_dict["runtime_id"] = str(elem.element_info.runtime_id)
            elem_dict["process_id"] = elem.element_info.process_id
            elem_dict["framework_id"] = getattr(elem.element_info, "framework_id", "")

            # 递归处理子控件
            if current_depth < depth:
                try:
                    children = elem.children()
                    for child in children:
                        child_dict = element_to_dict(child, current_depth + 1)
                        if child_dict:
                            elem_dict["children"].append(child_dict)
                except Exception as e:
                    elem_dict["children_error"] = str(e)

            return elem_dict

        except Exception as e:
            return {
                "error": f"无法处理元素: {str(e)}",
                "handle": elem.handle if hasattr(elem, "handle") else 0,
            }

    # 构建根元素字典
    root_dict = element_to_dict(element, 0)

    # 保存到JSON文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(root_dict, f, ensure_ascii=False, indent=2)

    return root_dict


# 使用示例
if __name__ == "__main__":
    # 连接到应用程序
    app = Application(backend="win32").connect(process=20732)
    mainWindow = app.MainWindow
    mainWindow.print_control_identifiers()

    # 使用进程名获取所有相关进程
    process_name = "qq108miniwpfn45.exe"
    target_processes = []

    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"].lower() == process_name.lower():
            target_processes.append(
                {"pid": proc.info["pid"], "name": proc.info["name"]}
            )

    for p in target_processes:
        print(f"PID: {p['pid']}, 进程名: {p['name']}")

    # xxx = mainWindow["Chrome_WidgetWin_0"]
    # xxx.print_control_identifiers()

    # # 输出为JSON
    # json_data = dump_to_json(main_window, "control_tree.json", depth=8)
    # print(f"控件树已保存为JSON，包含 {count_elements(json_data)} 个元素")
