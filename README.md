# Municipal Energy Knowledge Graph

**Independent research prototype** exploring semantic interoperability for municipal energy data and digital-twin decision support. Motivated by the research themes of energy-data sharing, ontologies, and municipal planning, including TU Delft's FEDERATE PhD vacancy. **This is not an official TU Delft or FEDERATE project.**

## What is implemented

- Two explicitly **synthetic** CSV sources: building registry and annual electricity consumption.
- A Python/RDFLib data pipeline mapping records into RDF triples and normalising MWh to kWh.
- Provenance fields including synthetic source identification, original value, unit, and reporting year.
- A SPARQL aggregation query reporting annual electricity use by neighbourhood.
- SHACL shape constraints checking required fields, numeric types, and nonnegative consumption.
- Four automated tests covering unit conversion, aggregation, valid graph constraints, and detection of missing years.
- A GitHub Actions workflow that installs dependencies, runs tests, builds the graph, queries it and validates it.

## Reproduce the experiment

Python 3.11+ is recommended.

```bash
git clone https://github.com/rohaniyer27/municipal-energy-knowledge-graph.git
cd municipal-energy-knowledge-graph
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python -m src.build_graph
python -m src.query_graph
python -m src.validate_graph
```

The graph builder writes `energy_graph.ttl` to the project root.

**Expected query output** (from hard-coded synthetic records):

```text
North: 7800 kWh (2025)
South: 12500 kWh (2025)
```

The generated Turtle RDF file is derived output, not a source dataset.

## Repository structure

```text
data/synthetic/          Synthetic example records
src/build_graph.py       CSV → RDF mapping and unit normalisation
src/query_graph.py       SPARQL neighbourhood aggregation
src/validate_graph.py    SHACL validation command
ontology/shapes.ttl      RDF shape constraints
tests/test_pipeline.py   Minimal regression tests
.github/workflows/       CI test workflow
```

## Research framing

1. How can heterogeneous building and energy-observation records be mapped into an explicit, shared semantic representation?
2. Can source metadata and schema constraints help detect integration errors?
3. How could trustworthy semantic representations feed energy-policy analysis when information is incomplete, delayed or aggregated?

The current implementation provides an **initial proof of concept for RQ1**, a few checks relevant to RQ2, and **does not yet implement RQ3**.

## Limitations and next steps

This is a small illustrative graph, not a city-scale digital twin. It does not perform asset entity resolution beyond matching supplied identifiers, formal ontology alignment to ESDL, privacy enforcement, real-time ingestion, decision optimisation, or measured performance comparisons. The datasets are synthetic and do not support empirical conclusions about Dutch municipalities.

Future work could include comparisons with a relational baseline, richer provenance and entity resolution, semantic mappings to existing energy data standards, privacy-aware access control, and scenario sensitivity experiments.

## Data ethics

No real household or customer information, OVO Energy data, or confidential operational material is included.

## Licence

See [LICENSE](LICENSE).
