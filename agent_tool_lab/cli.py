import argparse
import agent_tool_lab.cases as c
import agent_tool_lab.evaluator as evaluator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cases", default="examples/simple/cases.jsonl")
    parser.add_argument("-o", "--outputs", default="examples/simple/model_outputs.jsonl")
    args = parser.parse_args()
    cases = c.load_cases(args.cases)
    outputs = c.load_outputs(args.outputs)
    results = evaluator.evaluate_all(cases, outputs)

    print("Summary")
    print(f"Total cases: {results['total_cases']}")
    print(f"Tool selection accuracy: {results['tool_accuracy']}")
    print(f"Argument accuracy: {results['arg_accuracy']}")

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
