import json
from typing import Any
from pydantic import BaseModel, ValidationError


# cases.jsonl 中每一行测试用例必须符合的结构。
class Case(BaseModel):
    id: str
    input: str
    expected_tool: str
    expected_args: dict[str, Any]


# model_outputs.jsonl 中每一行模型输出必须符合的结构。
class ModelOutput(BaseModel):
    id: str
    actual_tool: str
    actual_args: dict[str, Any]


# 读取 JSONL 文件，逐行解析 JSON，并用传入的校验函数检查每条数据。
def load_jsonl(path, validate_item):
    items = []
    try:
        file = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"文件不存在：{path}")
        raise SystemExit(1)

    with file:
        line_number = 0
        for line in file:
            line_number += 1
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.decoder.JSONDecodeError:
                print(f"JSON 格式错误：文件 {path} 第 {line_number} 行")
                raise SystemExit(1)
            try:
                item = validate_item(item)
            except ValidationError as error:
                # Pydantic 的错误里带有字段位置，这里提取出来放进第一行摘要。
                fields = [err["loc"][0] for err in error.errors()]
                print(f"数据结构错误：文件 {path} 第 {line_number} 行，字段 {fields}")
                raise SystemExit(1)
            items.append(item)
    return items


# 读取测试用例文件，并按 Case schema 校验每一行。
def load_cases(path):
    return load_jsonl(path, validate_case)


# 读取模型输出文件，并按 ModelOutput schema 校验每一行。
def load_outputs(path):
    return load_jsonl(path, validate_output)


# 校验单条测试用例，返回普通 dict，方便后续 evaluator 继续用字典方式读取。
def validate_case(item):
    return Case.model_validate(item).model_dump()


# 校验单条模型输出，返回普通 dict，方便后续 evaluator 继续用字典方式读取。
def validate_output(item):
    return ModelOutput.model_validate(item).model_dump()
