#!/usr/bin/env python3
"""Replace all advertisedHost entries in a Strimzi Kafka manifest."""

from __future__ import annotations

import argparse
from pathlib import Path


def patch_file(path: Path, host: str) -> None:
    text = path.read_text()
    lines = text.splitlines()
    end_nl = text.endswith("\n")

    updated: list[str] = []
    for line in lines:
        if "advertisedHost:" in line:
            prefix = line.split("advertisedHost:")[0]
            updated.append(f"{prefix}advertisedHost: {host}")
        else:
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
