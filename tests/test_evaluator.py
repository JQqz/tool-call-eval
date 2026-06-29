import agent_tool_lab.evaluator as evaluator


def test_evaluate_case_pass():
    case = {
        "id": "case_001",
        "input": "帮我计算 23 * 7",
        "expected_tool": "calculator",
        "expected_args": {"expression": "23 * 7"},
    }
    output = {
        "id": "case_001",
        "actual_tool": "calculator",
        "actual_args": {"expression": "23 * 7"},
    }

    result = evaluator.evaluate_case(case, output)

    assert result["passed"] is True
    assert result["tool_correct"] is True
    assert result["args_correct"] is True
    assert result["failure_reasons"] == []


def test_evaluate_case_wrong_tool():
    case = {
        "id": "case_002",
        "input": "帮我计算 23 * 7",
        "expected_tool": "calculator",
        "expected_args": {"expression": "23 * 7"},
    }
    output = {
        "id": "case_002",
        "actual_tool": "search_appointments",
        "actual_args": {"expression": "23 * 7"},
    }

    result = evaluator.evaluate_case(case, output)

    assert result["passed"] is False
    assert result["tool_correct"] is False
    assert result["args_correct"] is True
    assert result["failure_reasons"] == ["wrong_tool"]


def test_evaluate_case_missing_arg():
    case = {
        "id": "case_003",
        "input": "帮我查一下王丽，手机号后四位 1234",
        "expected_tool": "search_patients",
        "expected_args": {"name": "王丽", "phone_last4": "1234"},
    }
    output = {
        "id": "case_003",
        "actual_tool": "search_patients",
        "actual_args": {"name": "王丽"},
    }

    result = evaluator.evaluate_case(case, output)

    assert result["passed"] is False
    assert result["tool_correct"] is True
    assert result["args_correct"] is False
    assert result["failure_reasons"] == ["missing_arg"]


def test_evaluate_case_wrong_arg_value():
    case = {
        "id": "case_004",
        "input": "帮我查一下王丽，手机号后四位 1234",
        "expected_tool": "search_patients",
        "expected_args": {"name": "王丽", "phone_last4": "1234"},
    }
    output = {
        "id": "case_004",
        "actual_tool": "search_patients",
        "actual_args": {"name": "王丽", "phone_last4": "9999"},
    }

    result = evaluator.evaluate_case(case, output)

    assert result["passed"] is False
    assert result["tool_correct"] is True
    assert result["args_correct"] is False
    assert result["failure_reasons"] == ["wrong_arg_value"]


def test_evaluate_all_missing_output():
    test_cases = [
        {
            "id": "case_001",
            "input": "帮我计算 23 * 7",
            "expected_tool": "calculator",
            "expected_args": {"expression": "23 * 7"},
        },
        {
            "id": "case_002",
            "input": "帮我查一下王丽，手机号后四位 1234",
            "expected_tool": "search_patients",
            "expected_args": {"name": "王丽", "phone_last4": "1234"},
        },
    ]
    outputs = [
        {
            "id": "case_001",
            "actual_tool": "calculator",
            "actual_args": {"expression": "23 * 7"},
        },
    ]

    result = evaluator.evaluate_all(test_cases, outputs)

    assert result["total_cases"] == 2
    assert result["tool_accuracy"] == 50.0
    assert result["arg_accuracy"] == 50.0

    missing_output_result = result["results"][1]
    assert missing_output_result["actual_tool"] is None
    assert missing_output_result["passed"] is False
    assert missing_output_result["tool_correct"] is False
    assert missing_output_result["args_correct"] is False
    assert missing_output_result["failure_reasons"] == ["missing_output"]
