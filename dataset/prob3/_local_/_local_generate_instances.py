from __future__ import annotations

import argparse
import math
import pickle
import re
from pathlib import Path


PROB_DIR = Path(__file__).resolve().parents[1]
PY_DIR = PROB_DIR / "params" / "py"
DZN_DIR = PROB_DIR / "params" / "dzn"
PLAIN_DIR = PROB_DIR / "params" / "plain"
PICKLE_DIR = PROB_DIR / "params" / "pickle"
FILE_TEMPLATE = "p3_q{index}.py"
VALUE_PATTERN = re.compile(r"^\s*n\s*=\s*(\d+)\s*$")


def parse_n_value(path: Path) -> int:
    content = path.read_text().strip()
    match = VALUE_PATTERN.fullmatch(content)
    if match is None:
        raise ValueError(f"Expected a single 'n=<int>' assignment in {path.name}, found: {content!r}")
    return int(match.group(1))


def collect_existing_values(seed_count: int) -> list[int]:
    values: list[int] = []
    for index in range(1, seed_count + 1):
        path = PY_DIR / FILE_TEMPLATE.format(index=index)
        if not path.exists():
            break
        values.append(parse_n_value(path))
    if not values:
        raise ValueError("No existing instance files were found.")
    if len(values) != seed_count:
        raise ValueError(
            f"Expected the first {seed_count} seed files to exist, but only found {len(values)}."
        )
    return values


def is_feasible_qg3_order(n: int) -> bool:
    # QG3 quasigroups exist exactly for orders n == 0 or 1 (mod 4), except n = 5.
    return n != 5 and n % 4 in (0, 1)


def make_logspace_tail(start: int, stop: int, new_file_count: int) -> list[int]:
    if new_file_count <= 0:
        return []
    if stop <= start:
        raise ValueError(f"max_value must be greater than the last existing n ({start}).")
    if not is_feasible_qg3_order(stop):
        raise ValueError(
            "For prob3/QG3, --max-value must be feasible: n != 5 and n % 4 in {0, 1}."
        )

    candidates = [n for n in range(start + 1, stop + 1) if is_feasible_qg3_order(n)]
    if len(candidates) < new_file_count:
        raise ValueError(
            f"Cannot create {new_file_count} feasible QG3 orders between {start} and {stop}."
        )

    point_count = new_file_count + 1
    log_start = math.log(start)
    log_stop = math.log(stop)

    values: list[int] = []
    previous_index = -1
    for position in range(1, point_count):
        fraction = position / (point_count - 1)
        target = math.exp(log_start + fraction * (log_stop - log_start))

        remaining_slots = point_count - position - 1
        min_index = previous_index + 1
        max_index = len(candidates) - remaining_slots - 1

        chosen_index = min_index
        while chosen_index < max_index and candidates[chosen_index] < target:
            chosen_index += 1

        chosen_index = min(chosen_index, max_index)
        values.append(candidates[chosen_index])
        previous_index = chosen_index

    return values


def write_instances(start_index: int, values: list[int]) -> None:
    for offset, value in enumerate(values, start=start_index):
        stem = f"p3_q{offset}"
        (PY_DIR / f"{stem}.py").write_text(f"n={value}\n")
        (DZN_DIR / f"{stem}.dzn").write_text(f"n = {value};\n")
        (PLAIN_DIR / f"{stem}.txt").write_text(f"n = {value}\n")
        with (PICKLE_DIR / f"{stem}.pkl").open("wb") as f:
            pickle.dump({"n": value}, f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extend prob3 parameter files with log-spaced n values."
    )
    parser.add_argument("--total-count", type=int, default=60, help="Total number of instance files to have.")
    parser.add_argument("--max-value", type=int, default=300, help="Target n value for the final instance file.")
    parser.add_argument(
        "--seed-count",
        type=int,
        default=5,
        help="Number of existing leading files to keep unchanged before generating the tail.",
    )
    args = parser.parse_args()

    if args.total_count < 1:
        raise ValueError("--total-count must be at least 1.")
    if args.seed_count < 1:
        raise ValueError("--seed-count must be at least 1.")
    if args.seed_count > args.total_count:
        raise ValueError("--seed-count cannot be greater than --total-count.")

    existing_values = collect_existing_values(args.seed_count)
    new_file_count = args.total_count - args.seed_count

    new_values = make_logspace_tail(existing_values[-1], args.max_value, new_file_count)
    write_instances(args.seed_count + 1, new_values)


if __name__ == "__main__":
    main()
