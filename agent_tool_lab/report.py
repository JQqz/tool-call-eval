# 根据 evaluate_all 返回的评测结果，生成一份 Markdown 格式的评测报告。
def generate_markdown_report(evaluation):
    results = evaluation["results"]
    lines = []

    # 先生成报告标题和整体汇总表。
    lines.append("# 工具调用评测报告")
    lines.append("")

    lines.append("## 汇总")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|---|---:|")
    lines.append(f"| 用例总数 | {evaluation['total_cases']} |")
    lines.append(f"| 工具选择准确率 | {evaluation['tool_accuracy']:.1f}% |")
    lines.append(f"| 参数匹配准确率 | {evaluation['arg_accuracy']:.1f}% |")
    lines.append("")

    # 按 expected_tool 分组，统计每个工具对应的 case 数和准确率。
    by_tool = {}
    for result in results:
        expected_tool = result["expected_tool"]

        if expected_tool not in by_tool:
            by_tool[expected_tool] = {
                "cases": 0,
                "tool_correct": 0,
                "args_correct": 0,
            }

        by_tool[expected_tool]["cases"] += 1

        if result["tool_correct"]:
            by_tool[expected_tool]["tool_correct"] += 1

        if result["args_correct"]:
            by_tool[expected_tool]["args_correct"] += 1

    lines.append("## 按工具统计")
    lines.append("")
    lines.append("| 期望工具 | 用例数 | 工具选择准确率 | 参数匹配准确率 |")
    lines.append("|---|---:|---:|---:|")

    for expected_tool in sorted(by_tool):
        stats = by_tool[expected_tool]
        case_count = stats["cases"]
        tool_accuracy = stats["tool_correct"] / case_count * 100
        arg_accuracy = stats["args_correct"] / case_count * 100
        lines.append(
            f"| {expected_tool} | {case_count} | "
            f"{tool_accuracy:.1f}% | {arg_accuracy:.1f}% |"
        )
    lines.append("")

    # 统计所有失败原因，方便看主要问题是哪一种。
    failure_counts = {}
    for result in results:
        for reason in result["failure_reasons"]:
            failure_counts[reason] = failure_counts.get(reason, 0) + 1

    lines.append("## 失败原因统计")
    lines.append("")
    lines.append("| 失败原因 | 次数 |")
    lines.append("|---|---:|")

    failure_reason_names = {
        "wrong_tool": "工具选择错误",
        "missing_arg": "缺少参数",
        "wrong_arg_value": "参数值错误",
        "missing_output": "缺少模型输出",
    }

    if failure_counts:
        for reason in sorted(failure_counts):
            reason_name = failure_reason_names.get(reason, reason)
            lines.append(f"| {reason_name} | {failure_counts[reason]} |")
    else:
        lines.append("| 无 | 0 |")
    lines.append("")

    # 工具调用对照表：行是期望调用的工具，列是实际调用的工具，格子里的数字是出现次数。
    expected_tools = sorted({result["expected_tool"] for result in results})
    actual_tools = set()
    confusion_counts = {}

    for result in results:
        expected_tool = result["expected_tool"]
        actual_tool = result["actual_tool"]

        if actual_tool is None:
            actual_tool = "缺失"

        actual_tools.add(actual_tool)
        key = (expected_tool, actual_tool)
        confusion_counts[key] = confusion_counts.get(key, 0) + 1

    matrix_tools = sorted(set(expected_tools) | actual_tools)

    lines.append("## 工具调用对照表")
    lines.append("")

    header_cells = ["期望调用 \\ 实际调用"] + matrix_tools
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|---" + "|---:" * len(matrix_tools) + "|")

    for expected_tool in expected_tools:
        row = [expected_tool]
        for actual_tool in matrix_tools:
            row.append(str(confusion_counts.get((expected_tool, actual_tool), 0)))
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # 最后列出失败 case，方便下一轮修改 prompt 或工具定义。
    lines.append("## 失败用例")
    lines.append("")

    has_failed_case = False
    for result in results:
        if not result["passed"]:
            has_failed_case = True

    if has_failed_case:
        lines.append("| 用例 ID | 用户输入 | 期望工具 | 实际工具 | 失败原因 |")
        lines.append("|---|---|---|---|---|")

        for result in results:
            if result["passed"]:
                continue

            actual_tool = result["actual_tool"]
            if actual_tool is None:
                actual_tool = "缺失"

            reason_names = []
            for reason in result["failure_reasons"]:
                reason_names.append(failure_reason_names.get(reason, reason))
            failure_reasons = ", ".join(reason_names)
            lines.append(
                f"| {result['id']} | {result['input']} | "
                f"{result['expected_tool']} | {actual_tool} | {failure_reasons} |"
            )
    else:
        lines.append("没有失败用例。")

    return "\n".join(lines) + "\n"
