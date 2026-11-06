# Municipal Energy Knowledge Graph

An independent research prototype exploring semantic interoperability for municipal energy data and digital-twin decision support.

## Motivation

Municipal energy planning requires integrating information about buildings, neighbourhoods, energy assets, and demand from different sources. This project investigates how RDF knowledge graphs, explicit semantic mappings, and validation can make the integration process inspectable and reproducible.

This work is independently developed and is **not** an official TU Delft or FEDERATE project.

## Research questions

1. How can heterogeneous building and energy observations be mapped into a common semantic representation?
2. How can provenance, units and quality constraints be preserved and checked?
3. How do missing or aggregated observations affect the answers to municipal planning queries?

## Technical scope

**Planned:** Python, RDFLib, RDF/Turtle, SPARQL, SHACL, synthetic data, automated tests, and a comparison against a relational-data baseline.

**Current status:** Initial repository setup. The technical experiments and validation results have not yet been published.

## First milestone

- Construct a small synthetic building and energy-observation graph.
- Query consumption by building and neighbourhood.
- Check expected values and document limitations.
- Add semantic validation and tests.

## Reproducibility

Once the prototype scripts are added, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No real household customer data or confidential business data will be used.

## Licence

See [LICENSE](LICENSE).
