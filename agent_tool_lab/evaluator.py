# 评测单条 case 和它对应的 output，返回这条用例的评分结果。
def evaluate_case(case, output):
    eva_result = {}
    failure_reasons = []
    eva_result["id"] = case["id"]
    eva_result["input"] = case["input"]
    eva_result["expected_tool"] = case["expected_tool"]

    # 没有对应输出时，这条 case 直接判失败。
    if output is None:
        eva_result["passed"] = False
        failure_reasons.append("missing_output")
        eva_result["tool_correct"] = False
        eva_result["args_correct"] = False
        eva_result["failure_reasons"] = failure_reasons
        eva_result["actual_tool"] = None
        return eva_result

    eva_result["actual_tool"] = output["actual_tool"]
    tool_correct = case["expected_tool"] == output["actual_tool"]
    if not tool_correct:
        failure_reasons.append("wrong_tool")

    # 只要求 expected_args 里的键和值都出现在 actual_args 里。
    # actual_args 多出来的字段不扣分。
    expected_args = case.get("expected_args", {})
    actual_args = output.get("actual_args", {})

    args_correct = True
    for arg_name, expected_value in expected_args.items():
        # 先检查参数名是否存在，避免直接取值时报 KeyError。
        if arg_name not in actual_args:
            args_correct = False
            if "missing_arg" not in failure_reasons:
                failure_reasons.append("missing_arg")
            continue

        # 参数名存在后，再比较实际值和期望值是否完全相等。
        actual_value = actual_args[arg_name]
        if actual_value != expected_value:
            args_correct = False
            if "wrong_arg_value" not in failure_reasons:
                failure_reasons.append("wrong_arg_value")

    eva_result["tool_correct"] = tool_correct
    eva_result["args_correct"] = args_correct
    eva_result["passed"] = tool_correct and args_correct
    eva_result["failure_reasons"] = failure_reasons
    return eva_result

# 批量评测所有 cases，按 id 匹配 outputs 后逐条调用 evaluate_case。
def evaluate_all(cases, outputs):
    # 把 outputs 列表转成按 id 查询的字典，后面可以用 case id 快速找输出。
    results = []
    evaluation = {}
    outputs_by_id = {}
    tool_accuracy_count = 0
    arg_accuracy_count = 0
    if not cases :
        raise ValueError("cases不能为空")
    for output in outputs:
        outputs_by_id[output["id"]] = output

    for case in cases:
        case_id = case["id"]
        # get 找不到时会返回 None，正好交给 evaluate_case 判成 missing_output。
        output = outputs_by_id.get(case_id)
        result = evaluate_case(case, output)
        results.append(result)

    total_cases = len(cases)
    for result in results:
        if result["tool_correct"]:
            tool_accuracy_count += 1
        if result["args_correct"]:
            arg_accuracy_count += 1

    tool_accuracy = round(tool_accuracy_count / total_cases * 100 , 1)
    arg_accuracy = round(arg_accuracy_count / total_cases * 100 , 1)

    evaluation["total_cases"] = total_cases
    evaluation["tool_accuracy"] = tool_accuracy
    evaluation["arg_accuracy"] = arg_accuracy
    evaluation["results"] = results
    return evaluation


