# 快速使用

## 缓存文件

```python
import json

cache_file = f"src/config/cache.json"

# 获取缓存json
with open(cache_file, encoding="utf-8") as f:
   cached_json = json.load(f)
   cached_coordDiff = cached_json.get("coordDiff")

   if cached_coordDiff:
        self.coordDiff = tuple(cached_coordDiff)
        self._mountFuture()
        return

# 更新缓存json
cached_json["coordDiff"] = self.coordDiff
with open(cache_file, "w", encoding="utf-8") as f:
    json.dump(cached_json, f, ensure_ascii=False, indent=2)
    print("coordDiff已写入缓存文件")
```

