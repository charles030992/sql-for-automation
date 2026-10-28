# sql-for-automation
[![CI](https://github.com/charles030992/sql-for-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/charles030992/sql-for-automation/actions/workflows/ci.yml)

Business automation pipeline using SQL + Python + pandas to generate operational reports from enterprise fleet data.

## What this project demonstrates

A practical data automation pipeline that:

- Connects to a relational database (SQLite)
- Runs structured SQL queries against operational business data
- Transforms results into pandas DataFrames
- Exports multi-sheet Excel reports automatically

This replaces a manual process that many companies still do with copy-paste and Excel formulas.

## Business context

The domain is fleet management: vehicles, ITV inspections, providers and invoices. **All the data in this repository is fictitious** (placeholder plates, invented amounts). The same pipeline structure applies to any business domain with tabular data.

## What it does

```
SQLite database (fleet data)
  → SQL queries (JOINs, GROUP BY, filters)
    → pandas DataFrames
      → Excel report (multi-sheet)
        → reporte_operativo.xlsx
```

**Sheets generated:**

| Sheet | Content |
|---|---|
| ITV_Pendientes | Vehicles with upcoming ITV inspection, ordered by date |
| Costes_Proveedor | Total spend, invoice count and average per provider |
| Resumen_Flota | Vehicle count grouped by operational status |

## SQL concepts used

- `SELECT`, `WHERE`, `ORDER BY`
- `INNER JOIN` across related tables
- `GROUP BY` with aggregations (`SUM`, `COUNT`, `AVG`)
- `ROUND` for formatting

## Project structure

```
sql-for-automation/
├── data/
│   └── empresa.db          (auto-generated on first run)
├── sql/
│   ├── schema.sql           table definitions
│   ├── sample_data.sql      sample fleet data (fictitious; pending ITV dates are relative to today)
│   └── queries.sql          standalone SQL for reference
├── reports/
│   └── reporte_operativo.xlsx  (auto-generated)
├── src/
│   ├── setup_db.py          creates and populates the database
│   └── main.py              runs the full pipeline
├── tests/
│   └── test_pipeline.py     queries, export and setup tests (in-memory SQLite)
├── requirements.txt
└── README.md
```

## How to run

```bash
# 1. Clone the repository
git clone https://github.com/charles030992/sql-for-automation.git
cd sql-for-automation

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
python src/main.py
```

The database is created automatically on first run. The Excel report is saved to `reports/reporte_operativo.xlsx`.

## Tests

```bash
python -m unittest discover -s tests
```

They run the real schema and sample data in an in-memory SQLite database and check each query, the Excel export and that `sql/queries.sql` stays in sync with the queries in `src/main.py`.

## Stack

- Python 3.11+
- SQLite (via `sqlite3` standard library)
- pandas
- openpyxl

## Extending this project

The pipeline is intentionally simple. Natural extensions:

- Replace SQLite with PostgreSQL or MySQL for a production database
- Add a scheduling layer (cron, Task Scheduler) for automatic daily reports
- Connect to SharePoint or email to distribute the report automatically
- Add LLM layer to generate a natural language summary of the report
- Integrate with Power Automate for enterprise workflow triggers

## Limitations

- The "pending ITV" report lists every inspection marked as pending, including vehicles with status `baja`.
- Sample data only: there is no import from a real system.

## About this project

Built as part of a structured learning path focused on enterprise automation with Python, SQL and AI. The goal is to apply concepts directly to business scenarios — not academic exercises.

## Keywords

`Python` `SQL` `SQLite` `pandas` `openpyxl` `data automation` `reporting automation`
`business process automation` `fleet management` `enterprise automation` `Excel automation`
`ETL` `workflow automation` `automatización empresarial`

## License

MIT — see [LICENSE](./LICENSE).
