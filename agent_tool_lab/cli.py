import json


def main():
    cases = load_json("examples/simple/cases.jsonl")
    outputs = load_json("examples/simple/model_outputs.jsonl")
    cases_num = len(cases)
    outputs_num = len(outputs)

    print(f"拥有case数据 {cases_num} 条")
    print(f"拥有output数据 {outputs_num} 条")
    print("Cases:")
    for case in cases:
        print(f"- {case['id']} | {case['input']} | expected_tool = {case['expected_tool']}")
    print("Outputs:")
    for output in outputs:
        print(f"- {output['id']} | actual_tool = {output['actual_tool']}")

def load_json(path):
    items = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                item = json.loads(line)
            except json.decoder.JSONDecodeError:
                print(f"Invalid JSON in {path}")
                raise SystemExit(1)
            items.append(item)
    return items


if __name__ == "__main__":
    main()
