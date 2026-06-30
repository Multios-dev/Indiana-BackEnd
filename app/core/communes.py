import csv
from pathlib import Path

_CSV_PATH = Path(__file__).parent.parent.parent / "data" / "REFNIS_2025.csv"


def _load_be_communes() -> frozenset[str]:
    names: set[str] = set()
    with open(_CSV_PATH, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="|")
        next(reader)
        for row in reader:
            if len(row) < 6:
                continue
            if not row[2].strip():
                continue
            fr_name = row[1].strip()
            nl_name = row[4].strip()
            if fr_name:
                names.add(fr_name.lower())
            if nl_name:
                names.add(nl_name.lower())
    return frozenset(names)


BE_COMMUNES: frozenset[str] = _load_be_communes()
