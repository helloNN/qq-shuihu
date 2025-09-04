import os

# 使用示例
if __name__ == "__main__":
    cou_count = os.cpu_count()
    print(f"CPU 核心数: {cou_count}")

    delay = range(5, 0, -1)
    print(list(delay))
