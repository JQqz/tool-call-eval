import agent_tool_lab.report as report


def test_generate_markdown_report_contains_title_and_summary():
    evaluation = {
        "total_cases": 1,
        "tool_accuracy": 100.0,
        "arg_accuracy": 100.0,
        "results": [
            {
                "id": "case_001",
                "input": "帮我算一下 23 * 7",
                "expected_tool": "calculator",
                "actual_tool": "calculator",
                "tool_correct": True,
                "args_correct": True,
                "passed": True,
                "failure_reasons": [],
            }
        ],
    }

    markdown = report.generate_markdown_report(evaluation)

    assert "# 工具调用评测报告" in markdown
    assert "| 用例总数 | 1 |" in markdown
    assert "| 工具选择准确率 | 100.0% |" in markdown
    assert "| 参数匹配准确率 | 100.0% |" in markdown


def test_generate_markdown_report_contains_failed_cases():
    evaluation = {
        "total_cases": 1,
        "tool_accuracy": 0.0,
        "arg_accuracy": 100.0,
        "results": [
            {
                "id": "case_002",
                "input": "今天有哪些预约？",
                "expected_tool": "list_appointments",
                "actual_tool": "search_patients",
                "tool_correct": False,
                "args_correct": True,
                "passed": False,
                "failure_reasons": ["wrong_tool"],
            }
        ],
    }

    markdown = report.generate_markdown_report(evaluation)

    assert "## 失败用例" in markdown
    assert "case_002" in markdown
    assert "今天有哪些预约？" in markdown
    assert "工具选择错误" in markdown


def test_generate_markdown_report_handles_no_failures():
    evaluation = {
        "total_cases": 1,
        "tool_accuracy": 100.0,
        "arg_accuracy": 100.0,
        "results": [
            {
                "id": "case_001",
                "input": "帮我算一下 23 * 7",
                "expected_tool": "calculator",
                "actual_tool": "calculator",
                "tool_correct": True,
                "args_correct": True,
                "passed": True,
                "failure_reasons": [],
            }
        ],
    }

    markdown = report.generate_markdown_report(evaluation)

    assert "没有失败用例。" in markdown
    assert "| 无 | 0 |" in markdown
