import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import main  # noqa: E402
import setup_db  # noqa: E402


def load_sample_db():
    """In-memory database with the real schema and sample data."""
    conn = sqlite3.connect(":memory:")
    conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((ROOT / "sql" / "sample_data.sql").read_text(encoding="utf-8"))
    return conn


class SampleDataTests(unittest.TestCase):
    def test_sample_data_loads(self):
        conn = load_sample_db()
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("vehiculos", "itv", "facturas")}
        self.assertEqual(counts, {"vehiculos": 5, "itv": 4, "facturas": 6})

    def test_pending_itv_dates_are_always_in_the_future(self):
        conn = load_sample_db()
        past = conn.execute(
            "SELECT COUNT(*) FROM itv WHERE estado = 'pendiente' AND fecha_itv < date('now')"
        ).fetchone()[0]
        self.assertEqual(past, 0)


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.conn = load_sample_db()

    def test_itv_pendientes_lists_only_pending_ordered_by_date(self):
        df = main.query_itv_pendientes(self.conn)
        self.assertEqual(list(df.columns), ["matricula", "marca", "modelo", "estado_vehiculo", "fecha_itv"])
        self.assertEqual(df["matricula"].tolist(), ["7777GHI", "1234ABC", "9999XYZ"])
        self.assertEqual(df["fecha_itv"].tolist(), sorted(df["fecha_itv"].tolist()))

    def test_costes_proveedor_totals_and_order(self):
        df = main.query_costes_proveedor(self.conn).set_index("proveedor")
        self.assertEqual(df["total_euros"].to_dict(), {"ALD": 4100.0, "ARVAL": 2250.0, "Repsol": 2180.0})
        self.assertEqual(df["num_facturas"].to_dict(), {"ALD": 2, "ARVAL": 2, "Repsol": 2})
        self.assertEqual(df["media_euros"].to_dict(), {"ALD": 2050.0, "ARVAL": 1125.0, "Repsol": 1090.0})
        self.assertEqual(df.index.tolist(), ["ALD", "ARVAL", "Repsol"])  # por total descendente

    def test_resumen_flota_counts_by_status(self):
        df = main.query_resumen_flota(self.conn).set_index("estado")
        self.assertEqual(df["total"].to_dict(), {"activo": 3, "taller": 1, "baja": 1})

    def test_queries_sql_stays_in_sync_with_the_python_queries(self):
        # sql/queries.sql repeats the queries of main.py "for reference"; they must not drift apart.
        statements = [s.strip() for s in (ROOT / "sql" / "queries.sql").read_text(encoding="utf-8").split(";") if "SELECT" in s]
        self.assertEqual(len(statements), 3)
        expected = [
            main.query_itv_pendientes(self.conn),
            main.query_costes_proveedor(self.conn),
            main.query_resumen_flota(self.conn),
        ]
        for statement, df in zip(statements, expected):
            pd.testing.assert_frame_equal(pd.read_sql_query(statement, self.conn), df)


class ExportAndSetupTests(unittest.TestCase):
    def test_export_excel_writes_one_sheet_per_dataframe(self):
        frames = {"A": pd.DataFrame({"x": [1, 2]}), "B": pd.DataFrame({"y": ["a"]})}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reports" / "out.xlsx"
            main.export_excel(frames, path)
            with pd.ExcelFile(path) as book:
                self.assertEqual(book.sheet_names, ["A", "B"])
                self.assertEqual(book.parse("A")["x"].tolist(), [1, 2])

    def test_create_database_is_idempotent(self):
        original = setup_db.DB_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                setup_db.DB_PATH = Path(tmp) / "data" / "empresa.db"
                setup_db.create_database()
                setup_db.create_database()  # a second run must not load the sample data twice
                conn = sqlite3.connect(setup_db.DB_PATH)
                try:
                    self.assertEqual(conn.execute("SELECT COUNT(*) FROM vehiculos").fetchone()[0], 5)
                finally:
                    conn.close()
        finally:
            setup_db.DB_PATH = original


if __name__ == "__main__":
    unittest.main()
