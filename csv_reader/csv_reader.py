import csv
from typing import Iterable
import tabulate


def find_avg(items):
    return sum(items) / len(items)


aggregators = {
    "min": min,
    "max": max,
    "avg": find_avg
}


def aggregate(data: Iterable, condition_str: str) -> dict[str, float]:
    item, aggregator = condition_str.split('=')
    items = []
    for row in data:
        try:
            items.append(float(row[item]))
        except (ValueError, KeyError):
            continue
    if not items:
        return {}
    res = aggregators[aggregator](items) if aggregator in aggregators else None
    return {f"{aggregator}": round(res, 2)}


def filter_file(data: Iterable, condition_str: str) -> list:
    operators = [">", "<", "="]
    for op in operators:
        if op in condition_str:
            item, condition = condition_str.split(op)
            operator = "==" if op == "=" else op
            try:
                float(condition)
                condition_code = float(condition)
            except ValueError:
                condition_code = f"'{condition}'"
            if isinstance(condition_code, str):
                return list(filter(
                    lambda row: eval(
                        f"'{row[item]}' {operator} {condition_code}"
                    ),
                    data
                ))
            else:
                return list(filter(
                    lambda row: eval(
                        f"{row[item]} {operator} {condition_code}"
                    ),
                    data
                ))

    raise ValueError("Invalid condition")


def csv_parser(file, filter: str = "", aggregator: str = "") -> str:
    with open(file, newline='', encoding='utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))

    if filter and aggregator:
        filtered_data = filter_file(data, filter)
        result = aggregate(filtered_data, aggregator)
        tabulated = tabulate.tabulate(
            [result], headers="keys", tablefmt="grid"
        )
        return tabulated

    elif filter:
        filtered_data = filter_file(data, filter)
        tabulated = tabulate.tabulate(
            filtered_data, headers="keys", tablefmt="grid"
        )
        return tabulated

    elif aggregator:
        result = aggregate(data, aggregator)
        tabulated = tabulate.tabulate(
            [result], headers="keys", tablefmt="grid"
        )
        return tabulated

    else:
        tabulated = tabulate.tabulate(data, headers="keys", tablefmt="grid")
        return tabulated

    raise ValueError
