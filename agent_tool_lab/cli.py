import argparse
import os
import sys
import agent_tool_lab.cases as c
import agent_tool_lab.evaluator as evaluator
import agent_tool_lab.report as report


# 命令行入口：读取参数、加载文件、执行评测，并把结果打印到终端。
def main():
    # 手写帮助信息，避免 argparse 默认输出里的 usage/options 等英文文案。
    if "-h" in sys.argv or "--help" in sys.argv:
        print("用法：python -m agent_tool_lab.cli [参数]")
        print("")
        print("运行工具调用评测：读取测试用例和模型输出，计算工具选择与参数匹配准确率。")
        print("")
        print("参数：")
        print("  -h, --help       显示帮助信息并退出")
        print("  -c, --cases      测试用例 JSONL 文件路径")
        print("                   默认：examples/simple/cases.jsonl")
        print("  -o, --outputs    模型输出 JSONL 文件路径")
        print("                   默认：examples/simple/model_outputs.jsonl")
        print("  -r, --report     Markdown 报告输出路径")
        print("                   不传则只在终端打印结果")
        return

    # 先检查需要文件路径的参数，避免 argparse 输出英文错误提示。
    # 默认值只在完全不传参数时生效。
    path_options = {
        "-c": "测试用例 JSONL 文件路径",
        "--cases": "测试用例 JSONL 文件路径",
        "-o": "模型输出 JSONL 文件路径",
        "--outputs": "模型输出 JSONL 文件路径",
        "-r": "Markdown 报告文件路径",
        "--report": "Markdown 报告文件路径",
    }
    for option, description in path_options.items():
        if option in sys.argv:
            option_index = sys.argv.index(option)
            if option_index == len(sys.argv) - 1 or sys.argv[option_index + 1].startswith("-"):
                print(f"参数 {option} 后面需要跟 {description}。")
                if option in ["-r", "--report"]:
                    print("如果不想生成报告文件，就不要写这个参数。")
                else:
                    print("如果想使用默认路径，就不要写这个参数。")
                print("运行 python -m agent_tool_lab.cli --help 查看用法。")
                raise SystemExit(1)

    # 解析命令行参数；如果用户不传路径，就使用 examples/simple 下的默认样例。
    parser = argparse.ArgumentParser(
        description="运行工具调用评测：读取测试用例和模型输出，计算工具选择与参数匹配准确率。",
        add_help=False,  # 关闭自带的英文 help。
    )
    parser.add_argument(
        "-c",
        "--cases",
        default="examples/simple/cases.jsonl",
    )
    parser.add_argument(
        "-o",
        "--outputs",
        default="examples/simple/model_outputs.jsonl",
    )
    parser.add_argument(
        "-r",
        "--report",
        default=None,
    )
    # parse_known_args 会把认识的参数放进 args，把不认识的参数放进 unknown_args。
    args, unknown_args = parser.parse_known_args()
    if unknown_args:
        print(f"未知参数：{' '.join(unknown_args)}")
        print("运行 python -m agent_tool_lab.cli --help 查看用法。")
        raise SystemExit(1)

    # 读取测试用例和模型输出，然后交给 evaluator 做批量评分。
    cases = c.load_cases(args.cases)
    outputs = c.load_outputs(args.outputs)
    results = evaluator.evaluate_all(cases, outputs)

    # 打印整体汇总指标。
    print("汇总")
    print(f"用例总数：{results['total_cases']}")
    print(f"工具选择准确率：{results['tool_accuracy']:.1f}%")
    print(f"参数匹配准确率：{results['arg_accuracy']:.1f}%")

    # 打印每条 case 的通过情况和失败原因。
    failure_reason_names = {
        "wrong_tool": "工具选择错误",
        "missing_arg": "缺少参数",
        "wrong_arg_value": "参数值错误",
        "missing_output": "缺少模型输出",
    }

    print("结果明细")
    for result in results["results"]:
        status = "通过" if result["passed"] else "失败"
        reason_names = []
        for reason in result["failure_reasons"]:
            reason_names.append(failure_reason_names.get(reason, reason))
        failure_reasons = " ".join(reason_names)
        if failure_reasons:
            print(f"{result['id']} {status} {failure_reasons}")
        else:
            print(f"{result['id']} {status}")

    # 如果用户传了 --report，就把 Markdown 报告写入指定文件。
    if args.report:
        markdown = report.generate_markdown_report(results)
        report_dir = os.path.dirname(args.report)
        # 只允许写入已经存在的目录。
        if report_dir and not os.path.isdir(report_dir):
            print(f"报告目录不存在：{report_dir}")
            print("请先创建目录，或者换一个已经存在的报告输出路径。")
            raise SystemExit(1)
        with open(args.report, "w", encoding="utf-8") as file:
            file.write(markdown)
        print(f"报告已写入：{args.report}")


if __name__ == "__main__":
    main()
