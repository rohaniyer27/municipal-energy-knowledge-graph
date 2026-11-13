"""Query normalized yearly electricity use from the RDF graph."""
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

QUERY = """
PREFIX ex: <https://example.org/municipal-energy/>
SELECT ?area (SUM(?usage) AS ?totalKWh)
WHERE {
  ?building a ex:Building ;
            ex:locatedIn ?area ;
            ex:hasObservation ?observation .
  ?observation ex:energyKWh ?usage ;
               ex:reportingYear 2025 .
}
GROUP BY ?area
ORDER BY ?area
"""


def totals(graph: Graph) -> dict[str, float]:
    return {
        str(area).split("/")[-1].replace("Neighbourhood_", ""): float(total)
        for area, total in graph.query(QUERY)
    }


def main() -> None:
    graph = Graph()
    graph.parse(str(ROOT / "energy_graph.ttl"), format="turtle")
    for area, value in totals(graph).items():
        print(f"{area}: {value:g} kWh (2025)")


if __name__ == "__main__":
    main()
