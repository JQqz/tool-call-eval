import json

# 读取 JSONL 文件，返回由每一行 JSON 对象组成的列表。
def load_jsonl(path):
    # JSONL 文件是一行一个 JSON 对象，所以这里逐行读取并解析。
    items = []
    with open(path, "r", encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.decoder.JSONDecodeError:
                print(f"Invalid JSON in {path} at line {line_number}")
                raise SystemExit(1)
            items.append(item)
    return items

# 读取测试用例文件，返回 cases 列表。
def load_cases(path):
    # cases 和 outputs 当前都是 JSONL 格式，先复用同一个底层读取函数。
    return load_jsonl(path)

# 读取模型输出文件，返回 outputs 列表。
def load_outputs(path):
    # 保留这个函数名，是为了让调用方看得出这里读取的是模型输出。
    return load_jsonl(path)
