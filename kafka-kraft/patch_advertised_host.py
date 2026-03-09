#!/usr/bin/env python3
"""Replace all advertisedHost entries in a Strimzi Kafka manifest."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ADVERTISED_HOST_RE = re.compile(
    r"^(?P<indent>\s*)advertisedHost:\s*(?P<value>.*?)(?P<comment>\s+#.*)?$"
)


def patch_file(path: Path, host: str) -> None:
    text = path.read_text()
    lines = text.splitlines()
    end_nl = text.endswith("\n")

    updated: list[str] = []
    for line in lines:
        match = ADVERTISED_HOST_RE.match(line)
        if match:
            comment = match.group("comment") or ""
            updated.append(f"{match.group('indent')}advertisedHost: {host}{comment}")
            continue
        updated.append(line)

    new_text = "\n".join(updated) + ("\n" if end_nl else "")
    path.write_text(new_text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Path to kafka-cluster.yaml")
    parser.add_argument("--host", required=True, help="Value to set for advertisedHost")
    args = parser.parse_args()

    patch_file(Path(args.file), args.host)
    print(f"Set advertisedHost to {args.host} in {args.file}")


if __name__ == "__main__":
    main()
