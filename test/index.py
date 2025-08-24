import time

# 使用示例
if __name__ == "__main__":
    times = (x for x in range(10))
    realTime = 0
    print(f"猎魂开始, 预计次数: {10}")

    for i in times:
        time.sleep(0.3)
        realTime += 1

        print(f"当前已猎魂: {realTime} 次", end="\r")

    print(f"猎魂结束, 实际次数: {realTime}")
