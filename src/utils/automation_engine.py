"""
跨平台自动化引擎模块
实现前台/后台点击、图像识别等功能
支持Windows、macOS、Linux
"""

import platform
import cv2
import numpy as np
import pyautogui
import time
import logging
from typing import Optional, Tuple, List, Dict, Any, Union
from PIL import Image, ImageGrab
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener

from .config_manager import config, ClickMode, ImageMode
from .window_utils import CrossPlatformWindowManager, WindowInfo


class CrossPlatformAutomationEngine:
    """跨平台自动化引擎"""

    def __init__(self):
        self.window_manager = CrossPlatformWindowManager()
        self.system = platform.system()
        self.logger = logging.getLogger(__name__)

        # 配置pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        # 鼠标和键盘控制器
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def click(
        self, hwnd: Union[int, str], x: int, y: int, button: str = "left"
    ) -> bool:
        """
        点击指定窗口的坐标

        Args:
            hwnd: 窗口句柄或标识符
            x: X坐标（相对于窗口）
            y: Y坐标（相对于窗口）
            button: 鼠标按钮 ("left", "right", "middle")

        Returns:
            bool: 是否成功
        """
        try:
            print(config.click_mode)
            if config.click_mode == ClickMode.FOREGROUND:
                return self._foreground_click(hwnd, x, y, button)
            else:
                return self._background_click(hwnd, x, y, button)
        except Exception as e:
            self.logger.error(f"Click failed: {e}")
            return False

    def _foreground_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str
    ) -> bool:
        """前台点击"""
        try:
            # 将窗口置于前台
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                self.logger.error("Window not found")
                return False

            print(window_info.rect)
            # 计算屏幕坐标
            screen_x = window_info.rect[0] + x
            screen_y = window_info.rect[1] + y

            # 使用pyautogui进行点击
            mouse_button = self._get_pyautogui_button(button)
            pyautogui.click(screen_x, screen_y, button=mouse_button)

            return True

        except Exception as e:
            self.logger.error(f"Foreground click failed: {e}")
            return False

    def _background_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str
    ) -> bool:
        """后台点击（模拟前台点击，因为跨平台限制）"""
        try:
            # 对于跨平台兼容性，后台点击实际上还是需要前台操作
            # 但我们可以先保存当前鼠标位置，点击后恢复
            current_pos = pyautogui.position()

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                self.logger.error("Window not found")
                return False

            # 计算屏幕坐标
            screen_x = window_info.rect[0] + x
            screen_y = window_info.rect[1] + y

            # 执行点击
            mouse_button = self._get_pyautogui_button(button)
            pyautogui.click(screen_x, screen_y, button=mouse_button)

            # 恢复鼠标位置
            pyautogui.moveTo(current_pos.x, current_pos.y)

            return True

        except Exception as e:
            self.logger.error(f"Background click failed: {e}")
            return False

    def _get_pyautogui_button(self, button: str) -> str:
        """获取pyautogui的按钮名称"""
        button_map = {"left": "left", "right": "right", "middle": "middle"}
        return button_map.get(button.lower(), "left")

    def double_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str = "left"
    ) -> bool:
        """双击"""
        try:
            if config.click_mode == ClickMode.FOREGROUND:
                return self._foreground_double_click(hwnd, x, y, button)
            else:
                return self._background_double_click(hwnd, x, y, button)
        except Exception as e:
            self.logger.error(f"Double click failed: {e}")
            return False

    def _foreground_double_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str
    ) -> bool:
        """前台双击"""
        try:
            # 将窗口置于前台
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                return False

            # 计算屏幕坐标
            screen_x = window_info.rect[0] + x
            screen_y = window_info.rect[1] + y

            # 使用pyautogui进行双击
            mouse_button = self._get_pyautogui_button(button)
            pyautogui.doubleClick(screen_x, screen_y, button=mouse_button)

            return True

        except Exception as e:
            self.logger.error(f"Foreground double click failed: {e}")
            return False

    def _background_double_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str
    ) -> bool:
        """后台双击"""
        try:
            # 执行两次点击
            if self.click(hwnd, x, y, button):
                time.sleep(0.1)
                return self.click(hwnd, x, y, button)
            return False
        except Exception as e:
            self.logger.error(f"Background double click failed: {e}")
            return False

    def drag(
        self, hwnd: Union[int, str], start_x: int, start_y: int, end_x: int, end_y: int
    ) -> bool:
        """拖拽操作"""
        try:
            if config.click_mode == ClickMode.FOREGROUND:
                return self._foreground_drag(hwnd, start_x, start_y, end_x, end_y)
            else:
                return self._background_drag(hwnd, start_x, start_y, end_x, end_y)
        except Exception as e:
            self.logger.error(f"Drag failed: {e}")
            return False

    def _foreground_drag(
        self, hwnd: Union[int, str], start_x: int, start_y: int, end_x: int, end_y: int
    ) -> bool:
        """前台拖拽"""
        try:
            # 将窗口置于前台
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                return False

            # 计算屏幕坐标
            screen_start_x = window_info.rect[0] + start_x
            screen_start_y = window_info.rect[1] + start_y
            screen_end_x = window_info.rect[0] + end_x
            screen_end_y = window_info.rect[1] + end_y

            # 使用pyautogui进行拖拽
            pyautogui.drag(
                screen_end_x - screen_start_x,
                screen_end_y - screen_start_y,
                duration=0.5,
                button="left",
            )

            return True

        except Exception as e:
            self.logger.error(f"Foreground drag failed: {e}")
            return False

    def _background_drag(
        self, hwnd: Union[int, str], start_x: int, start_y: int, end_x: int, end_y: int
    ) -> bool:
        """后台拖拽"""
        try:
            # 保存当前鼠标位置
            current_pos = pyautogui.position()

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                return False

            # 计算屏幕坐标
            screen_start_x = window_info.rect[0] + start_x
            screen_start_y = window_info.rect[1] + start_y
            screen_end_x = window_info.rect[0] + end_x
            screen_end_y = window_info.rect[1] + end_y

            # 执行拖拽
            pyautogui.moveTo(screen_start_x, screen_start_y)
            pyautogui.drag(
                screen_end_x - screen_start_x,
                screen_end_y - screen_start_y,
                duration=0.5,
                button="left",
            )

            # 恢复鼠标位置
            pyautogui.moveTo(current_pos.x, current_pos.y)

            return True

        except Exception as e:
            self.logger.error(f"Background drag failed: {e}")
            return False

    def send_text(self, hwnd: Union[int, str], text: str) -> bool:
        """发送文本"""
        try:
            # 确保窗口是活动的
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            time.sleep(0.1)  # 等待窗口激活

            # 使用pyautogui发送文本
            pyautogui.typewrite(text, interval=0.01)
            return True

        except Exception as e:
            self.logger.error(f"Send text failed: {e}")
            return False

    def send_key(
        self,
        hwnd: Union[int, str],
        key_code: Union[int, str],
        ctrl: bool = False,
        alt: bool = False,
        shift: bool = False,
    ) -> bool:
        """发送按键"""
        try:
            # 确保窗口是活动的
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            time.sleep(0.1)  # 等待窗口激活

            # 构建按键组合
            keys = []
            if ctrl:
                keys.append("ctrl")
            if alt:
                keys.append("alt")
            if shift:
                keys.append("shift")

            # 转换按键代码
            if isinstance(key_code, int):
                # 尝试转换常见的按键代码
                key_name = self._convert_key_code(key_code)
            else:
                key_name = str(key_code)

            keys.append(key_name)

            # 发送按键组合
            if len(keys) > 1:
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(keys[0])

            return True

        except Exception as e:
            self.logger.error(f"Send key failed: {e}")
            return False

    def _convert_key_code(self, key_code: int) -> str:
        """转换按键代码为pyautogui识别的按键名"""
        key_map = {
            13: "enter",
            27: "esc",
            32: "space",
            8: "backspace",
            9: "tab",
            16: "shift",
            17: "ctrl",
            18: "alt",
            37: "left",
            38: "up",
            39: "right",
            40: "down",
            112: "f1",
            113: "f2",
            114: "f3",
            115: "f4",
            116: "f5",
            117: "f6",
            118: "f7",
            119: "f8",
            120: "f9",
            121: "f10",
            122: "f11",
            123: "f12",
        }
        return key_map.get(key_code, str(key_code))

    def capture_window(self, hwnd: Union[int, str]) -> Optional[np.ndarray]:
        """
        截取窗口图像

        Args:
            hwnd: 窗口句柄或标识符

        Returns:
            Optional[np.ndarray]: 图像数组，BGR格式
        """
        try:
            if config.image_mode == ImageMode.FOREGROUND:
                return self._capture_window_foreground(hwnd)
            else:
                return self._capture_window_background(hwnd)
        except Exception as e:
            self.logger.error(f"Capture window failed: {e}")
            return None

    def _capture_window_foreground(self, hwnd: Union[int, str]) -> Optional[np.ndarray]:
        """前台截图"""
        try:
            # 将窗口置于前台
            if not self.window_manager.bring_window_to_front(hwnd):
                self.logger.warning(
                    "Failed to bring window to front, continuing anyway"
                )

            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                return None

            # 获取窗口位置
            left, top, right, bottom = window_info.rect
            width = right - left
            height = bottom - top

            # 截图
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

            # 转换为numpy数组
            img_array = np.array(screenshot)

            # 转换为BGR格式（OpenCV使用BGR）
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            return img_bgr

        except Exception as e:
            self.logger.error(f"Foreground capture failed: {e}")
            return None

    def _capture_window_background(self, hwnd: Union[int, str]) -> Optional[np.ndarray]:
        """后台截图（在跨平台环境下，通常需要前台操作）"""
        try:
            # 在大多数跨平台情况下，后台截图需要特殊处理
            # 这里使用前台截图作为fallback
            return self._capture_window_foreground(hwnd)

        except Exception as e:
            self.logger.error(f"Background capture failed: {e}")
            return None

    def capture_screen(
        self, region: Optional[Tuple[int, int, int, int]] = None
    ) -> Optional[np.ndarray]:
        """截取屏幕"""
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()

            # 转换为numpy数组
            img_array = np.array(screenshot)

            # 转换为BGR格式
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            return img_bgr

        except Exception as e:
            self.logger.error(f"Screen capture failed: {e}")
            return None

    def find_image(
        self, hwnd: Union[int, str], template_path: str, threshold: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """
        在窗口中查找图像

        Args:
            hwnd: 窗口句柄或标识符
            template_path: 模板图像路径
            threshold: 匹配阈值

        Returns:
            Optional[Dict[str, Any]]: 匹配结果，包含位置和置信度
        """
        try:
            # 截取窗口图像
            window_img = self.capture_window(hwnd)
            if window_img is None:
                return None

            # 加载模板图像
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                self.logger.error(f"Failed to load template image: {template_path}")
                return None

            # 模板匹配
            result = cv2.matchTemplate(window_img, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                # 计算中心点坐标
                template_height, template_width = template.shape[:2]
                center_x = max_loc[0] + template_width // 2
                center_y = max_loc[1] + template_height // 2

                return {
                    "found": True,
                    "confidence": max_val,
                    "position": {
                        "x": center_x,
                        "y": center_y,
                        "left": max_loc[0],
                        "top": max_loc[1],
                        "right": max_loc[0] + template_width,
                        "bottom": max_loc[1] + template_height,
                    },
                }
            else:
                return None

        except Exception as e:
            self.logger.error(f"Find image failed: {e}")
            return None

    def find_all_images(
        self, hwnd: Union[int, str], template_path: str, threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        在窗口中查找所有匹配的图像

        Args:
            hwnd: 窗口句柄或标识符
            template_path: 模板图像路径
            threshold: 匹配阈值

        Returns:
            List[Dict[str, Any]]: 所有匹配结果列表
        """
        try:
            # 截取窗口图像
            window_img = self.capture_window(hwnd)
            if window_img is None:
                return []

            # 加载模板图像
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                self.logger.error(f"Failed to load template image: {template_path}")
                return []

            # 模板匹配
            result = cv2.matchTemplate(window_img, template, cv2.TM_CCOEFF_NORMED)

            # 查找所有匹配位置
            locations = np.where(result >= threshold)
            matches = []

            template_height, template_width = template.shape[:2]

            for pt in zip(*locations[::-1]):  # 交换x和y坐标
                center_x = pt[0] + template_width // 2
                center_y = pt[1] + template_height // 2
                confidence = result[pt[1], pt[0]]

                matches.append(
                    {
                        "found": True,
                        "confidence": confidence,
                        "position": {
                            "x": center_x,
                            "y": center_y,
                            "left": pt[0],
                            "top": pt[1],
                            "right": pt[0] + template_width,
                            "bottom": pt[1] + template_height,
                        },
                    }
                )

            # 按置信度排序
            matches.sort(key=lambda x: x["confidence"], reverse=True)

            return matches

        except Exception as e:
            self.logger.error(f"Find all images failed: {e}")
            return []

    def wait_for_image(
        self,
        hwnd: Union[int, str],
        template_path: str,
        timeout: int = 10,
        threshold: float = 0.8,
    ) -> Optional[Dict[str, Any]]:
        """
        等待图像出现

        Args:
            hwnd: 窗口句柄或标识符
            template_path: 模板图像路径
            timeout: 超时时间（秒）
            threshold: 匹配阈值

        Returns:
            Optional[Dict[str, Any]]: 匹配结果
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.find_image(hwnd, template_path, threshold)
            if result:
                return result
            time.sleep(0.5)

        return None

    def click_image(
        self,
        hwnd: Union[int, str],
        template_path: str,
        threshold: float = 0.8,
        button: str = "left",
    ) -> bool:
        """
        点击图像

        Args:
            hwnd: 窗口句柄或标识符
            template_path: 模板图像路径
            threshold: 匹配阈值
            button: 鼠标按钮

        Returns:
            bool: 是否成功
        """
        try:
            result = self.find_image(hwnd, template_path, threshold)
            if result:
                x = result["position"]["x"]
                y = result["position"]["y"]
                return self.click(hwnd, x, y, button)
            return False
        except Exception as e:
            self.logger.error(f"Click image failed: {e}")
            return False

    def scroll(
        self, hwnd: Union[int, str], x: int, y: int, direction: str, clicks: int = 3
    ) -> bool:
        """
        滚动操作

        Args:
            hwnd: 窗口句柄或标识符
            x: X坐标
            y: Y坐标
            direction: 滚动方向 ("up", "down")
            clicks: 滚动次数

        Returns:
            bool: 是否成功
        """
        try:
            # 获取窗口信息
            window_info = self.window_manager.get_window_info(hwnd)
            if not window_info:
                return False

            # 计算屏幕坐标
            screen_x = window_info.rect[0] + x
            screen_y = window_info.rect[1] + y

            # 执行滚动
            if direction.lower() == "up":
                pyautogui.scroll(clicks, x=screen_x, y=screen_y)
            else:
                pyautogui.scroll(-clicks, x=screen_x, y=screen_y)

            return True

        except Exception as e:
            self.logger.error(f"Scroll failed: {e}")
            return False

    def get_window_text(self, hwnd: Union[int, str]) -> str:
        """获取窗口文本"""
        try:
            window_info = self.window_manager.get_window_info(hwnd)
            if window_info:
                return window_info.title
            return ""
        except Exception as e:
            self.logger.error(f"Get window text failed: {e}")
            return ""

    def is_window_visible(self, hwnd: Union[int, str]) -> bool:
        """检查窗口是否可见"""
        try:
            window_info = self.window_manager.get_window_info(hwnd)
            if window_info:
                return window_info.is_visible
            return False
        except Exception as e:
            self.logger.error(f"Check window visibility failed: {e}")
            return False


# 为了向后兼容，创建别名
AutomationEngine = CrossPlatformAutomationEngine
