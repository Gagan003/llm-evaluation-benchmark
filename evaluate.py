"""Prepare blinded review sheets and summarize completed reviews."""
import argparse
from collections import Counter
import csv
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent
DIMENSIONS = ("correctness", "instructions", "completeness")
SIDES = ("a", "b")
SCORES = [f"{side}_{dimension}" for side in SIDES for dimension in DIMENSIONS]
LABELS = ("model_1", "model_2")
FAILURES = {
    "policy_error", "unsupported_promise", "privacy_error",
    "missed_step", "instruction_error",
}


def read_index(path, required):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"id", *required}.issubset(reader.fieldnames or []):
            raise ValueError(f"{path} is missing required columns")
        indexed = {}
        for row in reader:
            identifier = row["id"]
            if not identifier or identifier in indexed:
                raise ValueError(f"{path} contains an empty or duplicate ID")
            if any(row[key] is None for key in required):
                raise ValueError(f"{path} has an incomplete row for {identifier}")
            indexed[identifier] = row
        return indexed


def write_csv(path, fields, rows):
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def check_ids(prompts, table, label):
    if prompts.keys() != table.keys():
        missing = sorted(prompts.keys() - table.keys())
        extra = sorted(table.keys() - prompts.keys())
        raise ValueError(f"{label}: missing IDs {missing}, extra IDs {extra}")


def prepare(args, prompts):
    first = read_index(args.model_1, ["response"])
    second = read_index(args.model_2, ["response"])
    for label, table in zip(LABELS, (first, second)):
        check_ids(prompts, table, label)
        if any(not row["response"].strip() for row in table.values()):
            raise ValueError(f"{label} has blank responses")

    rng = random.Random(args.seed)
    order = list(prompts)
    rng.shuffle(order)
    reviews = []
    keys = []
    for identifier in order:
        pair = [(LABELS[0], first[identifier]), (LABELS[1], second[identifier])]
        rng.shuffle(pair)
        (label_a, row_a), (label_b, row_b) = pair
        reviews.append({
            "id": identifier,
            **{field: prompts[identifier][field] for field in (
                "prompt", "policy_refs", "required_checks", "reference_answer"
            )},
            "response_a": row_a["response"],
            "response_b": row_b["response"],
        })
        keys.append({"id": identifier, "a": label_a, "b": label_b})

    args.directory.mkdir(parents=True, exist_ok=True)
    review_path = args.directory / "review.csv"
    key_path = args.directory / "key.csv"
    if review_path.exists() or key_path.exists():
        raise ValueError("Choose an output directory without review.csv or key.csv")
    write_csv(review_path, [
        *reviews[0], *SCORES, "a_failure", "b_failure", "winner", "justification"
    ], reviews)
    write_csv(key_path, ["id", "a", "b"], keys)
    print(f"Prepared {len(reviews)} blind comparisons in {review_path}")


def report(args, prompts):
    reviews = read_index(args.directory / "review.csv", [
        *SCORES, "a_failure", "b_failure", "winner", "justification"
    ])
    keys = read_index(args.directory / "key.csv", SIDES)
    check_ids(prompts, reviews, "review")
    check_ids(prompts, keys, "key")

    winners = Counter()
    scores = {label: Counter() for label in LABELS}
    failures = {label: Counter() for label in LABELS}
    for identifier, row in reviews.items():
        key = keys[identifier]
        if {key[side] for side in SIDES} != set(LABELS):
            raise ValueError(f"{identifier}: invalid model mapping")
        winner = row["winner"].strip().lower()
        if winner not in (*SIDES, "tie") or not row["justification"].strip():
            raise ValueError(f"{identifier}: enter a, b, or tie and a justification")
        winners["tie" if winner == "tie" else key[winner]] += 1
        for side in SIDES:
            label = key[side]
            values = [row[f"{side}_{dimension}"].strip() for dimension in DIMENSIONS]
            if any(value not in ("0", "1", "2") for value in values):
                raise ValueError(f"{identifier}: enter 0, 1, or 2 for each score")
            for dimension, value in zip(DIMENSIONS, values):
                scores[label][dimension] += int(value)
            failure = row[f"{side}_failure"].strip().lower()
            if failure == "none" and "0" not in values and "1" not in values:
                continue
            if failure not in FAILURES or values == ["2", "2", "2"]:
                raise ValueError(f"{identifier}: failure tag must match the scores for {side}")
            failures[label][failure] += 1

    count = len(reviews)
    print(f"Reviewed {count} prompts and {2 * count} responses\n")
    for label in LABELS:
        print(f"{label} — {winners[label]} wins")
        for dimension in DIMENSIONS:
            print(f"  {dimension}: {scores[label][dimension] / count:.2f}/2")
        tagged = sum(failures[label].values())
        print(f"  Responses with a tagged failure: {tagged}/{count} ({tagged / count:.0%})")
        for failure, frequency in sorted(failures[label].items()):
            print(f"    {failure}: {frequency}")
    print(f"Ties: {winners['tie']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("model_1", type=Path)
    prepare_parser.add_argument("model_2", type=Path)
    prepare_parser.add_argument("directory", type=Path)
    prepare_parser.add_argument("--seed", type=int, default=42)
    report_parser = commands.add_parser("report")
    report_parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    try:
        prompts = read_index(ROOT / "data" / "prompts.csv", [
            "prompt", "policy_refs", "required_checks", "reference_answer"
        ])
        if not prompts:
            raise ValueError("The prompt dataset is empty")
        if args.command == "prepare":
            prepare(args, prompts)
        else:
            report(args, prompts)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
