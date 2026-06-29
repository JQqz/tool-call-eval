import agent_tool_lab.cases as cases


def test_load_cases_reads_jsonl(tmp_path):
    cases_file = tmp_path / "cases.jsonl"
    cases_file.write_text(
        '{"id": "case_001", "expected_tool": "calculator"}\n'
        '{"id": "case_002", "expected_tool": "search_appointments"}\n',
        encoding="utf-8",
    )

    result = cases.load_cases(cases_file)

    assert result == [
        {"id": "case_001", "expected_tool": "calculator"},
        {"id": "case_002", "expected_tool": "search_appointments"},
    ]


def test_load_outputs_reads_jsonl(tmp_path):
    outputs_file = tmp_path / "model_outputs.jsonl"
    outputs_file.write_text(
        '{"id": "case_001", "actual_tool": "calculator"}\n'
        '{"id": "case_002", "actual_tool": "search_appointments"}\n',
        encoding="utf-8",
    )

    result = cases.load_outputs(outputs_file)

    assert result == [
        {"id": "case_001", "actual_tool": "calculator"},
        {"id": "case_002", "actual_tool": "search_appointments"},
    ]


def test_load_cases_skips_empty_lines(tmp_path):
    cases_file = tmp_path / "cases.jsonl"
    cases_file.write_text(
        '\n'
        '{"id": "case_001", "expected_tool": "calculator"}\n'
        '\n',
        encoding="utf-8",
    )

    result = cases.load_cases(cases_file)

    assert result == [
        {"id": "case_001", "expected_tool": "calculator"},
    ]


def test_load_cases_invalid_json_reports_line(tmp_path, capsys):
    cases_file = tmp_path / "cases.jsonl"
    cases_file.write_text(
        '{"id": "case_001", "expected_tool": "calculator"}\n'
        '{"id": "case_002", "expected_tool": }\n',
        encoding="utf-8",
    )

    try:
        cases.load_cases(cases_file)
    except SystemExit as error:
        assert error.code == 1
    else:
        assert False, "load_cases should exit when JSON is invalid"

    captured = capsys.readouterr()
    assert "Invalid JSON" in captured.out
    assert "line 2" in captured.out
