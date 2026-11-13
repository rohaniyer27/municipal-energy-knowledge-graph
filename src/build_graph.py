"""Build a small RDF graph from two explicitly synthetic energy datasets."""
from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, XSD

ROOT = Path(__file__).resolve().parents[1]
EX = Namespace("https://example.org/municipal-energy/")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def to_kwh(value: str, unit: str) -> Decimal:
    factors = {"kWh": Decimal("1"), "MWh": Decimal("1000")}
    if unit not in factors:
        raise ValueError(f"Unsupported electricity unit: {unit}")
    amount = Decimal(value) * factors[unit]
    if amount < 0:
        raise ValueError("Consumption must be nonnegative")
    return amount


def build_graph(data_dir: Path | None = None) -> Graph:
    data_dir = data_dir or ROOT / "data" / "synthetic"
    buildings = read_csv(data_dir / "buildings.csv")
    observations = read_csv(data_dir / "consumption.csv")
    graph = Graph()
    graph.bind("ex", EX)

    known_ids = set()
    for row in buildings:
        building_id = row["building_id"]
        if not building_id or building_id in known_ids:
            raise ValueError(f"Missing or duplicate building_id: {building_id}")
        known_ids.add(building_id)
        building = EX[building_id]
        area = EX[f"Neighbourhood_{row['neighbourhood']}"]
        graph.add((building, RDF.type, EX.Building))
        graph.add((area, RDF.type, EX.Neighbourhood))
        graph.add((building, EX.locatedIn, area))
        graph.add((building, EX.buildingType, Literal(row["building_type"])))

    seen = set()
    for row in observations:
        building_id = row["property_ref"]
        year = int(row["year"])
        if building_id not in known_ids:
            raise ValueError(f"Unmatched building identifier: {building_id}")
        key = (building_id, year)
        if key in seen:
            raise ValueError(f"Duplicate annual observation: {key}")
        seen.add(key)
        kwh = to_kwh(row["annual_usage"], row["unit"])
        obs = EX[f"Observation_{building_id}_{year}"]
        graph.add((obs, RDF.type, EX.EnergyObservation))
        graph.add((EX[building_id], EX.hasObservation, obs))
        graph.add((obs, EX.energyKWh, Literal(kwh, datatype=XSD.decimal)))
        graph.add((obs, EX.reportingYear, Literal(year, datatype=XSD.integer)))
        graph.add((obs, EX.source, EX.SyntheticConsumptionDataset))
        graph.add((obs, EX.originalValue, Literal(Decimal(row["annual_usage"]), datatype=XSD.decimal)))
        graph.add((obs, EX.originalUnit, Literal(row["unit"])))
    return graph


def main() -> None:
    graph = build_graph()
    output = ROOT / "energy_graph.ttl"
    graph.serialize(destination=str(output), format="turtle")
    print(f"Created {len(graph)} triples in {output.name}")


if __name__ == "__main__":
    main()
