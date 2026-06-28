import argparse
import agent_tool_lab.cases as c
import agent_tool_lab.evaluator as evaluator


# 命令行入口：读取参数、加载文件、执行评测，并把结果打印到终端。
def main():
    # 解析命令行参数；如果用户不传路径，就使用 examples/simple 下的默认样例。
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cases", default="examples/simple/cases.jsonl")
    parser.add_argument("-o", "--outputs", default="examples/simple/model_outputs.jsonl")
    args = parser.parse_args()

    # 读取测试用例和模型输出，然后交给 evaluator 做批量评分。
    cases = c.load_cases(args.cases)
    outputs = c.load_outputs(args.outputs)
    results = evaluator.evaluate_all(cases, outputs)

    # 打印整体汇总指标。
    print("Summary")
    print(f"Total cases: {results['total_cases']}")
    print(f"Tool selection accuracy: {results['tool_accuracy']}")
    print(f"Argument accuracy: {results['arg_accuracy']}")

    # 打印每条 case 的通过情况和失败原因。
    print("Results")
    for result in results["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        failure_reasons = " ".join(result["failure_reasons"])
        if failure_reasons:
            print(f"{result['id']} {status} {failure_reasons}")
        else:
            print(f"{result['id']} {status}")


if __name__ == "__main__":
    main()
