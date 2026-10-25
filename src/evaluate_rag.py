
import json
import time
from pathlib import Path

from answer_generator import answer_question, FALLBACK


# 1. Locate project files
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "data" / "evaluation_dataset.json"
OUTPUT_PATH = PROJECT_DIR / "data" / "evaluation_results.json"


def evaluate():
    # 2. Load all test cases
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    total = len(test_cases)
    passed = 0
    results = []

    print(f"Running evaluation on {total} test cases...\n")

    # 3. Run each question through the RAG pipeline
    for test in test_cases:
        start_time = time.perf_counter()

        try:
            response = answer_question(test["question"])
            latency = time.perf_counter() - start_time

            # Support either a string or a dictionary response
            if isinstance(response, dict):
                actual_answer = response.get("answer", "")
                context = response.get("context")
            else:
                actual_answer = response
                context = None

            actual_answer = str(actual_answer).strip()

            # 4. Check expected answer/fallback behavior
            is_fallback = actual_answer.lower() == FALLBACK.lower()

            if test["expected_behavior"] == "fallback":
                behavior_correct = is_fallback
            else:
                answer_lower = actual_answer.lower()

                required_phrases = test.get("must_contain", [])
                prohibited_phrases = test.get("must_not_contain", [])

                behavior_correct = (
                    bool(answer_lower)
                    and not is_fallback
                    and all(
                        phrase.lower() in answer_lower
                        for phrase in required_phrases
                    )
                    and not any(
                        phrase.lower() in answer_lower
                        for phrase in prohibited_phrases
                    )
                )

            if behavior_correct:
                passed += 1

            row = {
                "id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "expected_behavior": test["expected_behavior"],
                "expected_rule": test.get("expected_rule"),
                "actual_answer": actual_answer,
                "retrieved_context": context,
                "behavior_correct": behavior_correct,
                "latency_seconds": round(latency, 3)
            }

        except Exception as error:
            latency = time.perf_counter() - start_time

            row = {
                "id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "expected_behavior": test["expected_behavior"],
                "expected_rule": test.get("expected_rule"),
                "actual_answer": None,
                "retrieved_context": None,
                "behavior_correct": False,
                "latency_seconds": round(latency, 3),
                "error": str(error)
            }

        results.append(row)

        status = "PASS" if row["behavior_correct"] else "FAIL"

        print(
            f"[{status}] {test['id']} | "
            f"{test['category']} | "
            f"{row['latency_seconds']:.2f}s"
        )
        print(f"Question: {test['question']}")
        print(f"Answer: {row['actual_answer']}")

        if row.get("error"):
            print(f"Error: {row['error']}")

        print("-" * 50)

    # 5. Calculate summary metrics
    failed = total - passed
    pass_rate = passed / total * 100 if total else 0

    latencies = [row["latency_seconds"] for row in results]
    average_latency = (
        sum(latencies) / len(latencies) if latencies else 0
    )

    # 6. Save detailed results
    report = {
        "total_cases": total,
        "passed": passed,
        "failed": failed,
        "behavior_pass_rate_percent": round(pass_rate, 2),
        "average_latency_seconds": round(average_latency, 3),
        "results": results
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    # 7. Print final summary
    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Behavior pass rate: {pass_rate:.2f}%")
    print(f"Average latency: {average_latency:.3f} seconds")
    print(f"Report saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    evaluate()
