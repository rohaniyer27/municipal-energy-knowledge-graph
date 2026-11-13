"""Validate graph data quality with SHACL."""
from pathlib import Path

from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    conforms, _, report = validate(
        data_graph=str(ROOT / "energy_graph.ttl"),
        shacl_graph=str(ROOT / "ontology" / "shapes.ttl"),
        data_graph_format="turtle",
        shacl_graph_format="turtle",
    )
    print("SHACL conforms:", conforms)
    if not conforms:
        print(report)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
