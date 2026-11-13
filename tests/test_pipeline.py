from decimal import Decimal

import pytest
from rdflib import RDF
from pyshacl import validate

from src.build_graph import EX, ROOT, build_graph, to_kwh
from src.query_graph import totals


def test_unit_conversion():
    assert to_kwh("4.2", "MWh") == Decimal("4200")
    assert to_kwh("3600", "kWh") == Decimal("3600")
    with pytest.raises(ValueError):
        to_kwh("1", "unknown")


def test_neighbourhood_totals():
    graph = build_graph()
    assert totals(graph) == {"North": 7800.0, "South": 12500.0}


def test_shacl_valid():
    graph = build_graph()
    conforms, _, _ = validate(
        data_graph=graph,
        shacl_graph=str(ROOT / "ontology" / "shapes.ttl"),
        shacl_graph_format="turtle",
    )
    assert conforms


def test_shacl_rejects_missing_year():
    graph = build_graph()
    graph.remove((EX.Observation_B001_2025, EX.reportingYear, None))
    conforms, _, _ = validate(
        data_graph=graph,
        shacl_graph=str(ROOT / "ontology" / "shapes.ttl"),
        shacl_graph_format="turtle",
    )
    assert not conforms
