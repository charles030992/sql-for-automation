import sqlite3
import pandas as pd
from pathlib import Path

# Allow running from repo root or from src/
import sys
sys.path.insert(0, str(Path(__file__).parent))
from setup_db import create_database, DB_PATH

REPORTS_DIR = Path(__file__).parent.parent / "reports"


def query_itv_pendientes(conn: sqlite3.Connection) -> pd.DataFrame:
    sql = """
        SELECT
            v.matricula,
            v.marca,
            v.modelo,
            v.estado        AS estado_vehiculo,
            i.fecha_itv
        FROM vehiculos v
        INNER JOIN itv i ON v.id = i.vehiculo_id
        WHERE i.estado = 'pendiente'
        ORDER BY i.fecha_itv ASC
    """
    return pd.read_sql_query(sql, conn)


def query_costes_proveedor(conn: sqlite3.Connection) -> pd.DataFrame:
    sql = """
        SELECT
            proveedor,
            COUNT(*)               AS num_facturas,
            SUM(importe)           AS total_euros,
            ROUND(AVG(importe), 2) AS media_euros
        FROM facturas
        GROUP BY proveedor
        ORDER BY total_euros DESC
    """
    return pd.read_sql_query(sql, conn)


def query_resumen_flota(conn: sqlite3.Connection) -> pd.DataFrame:
    sql = """
        SELECT
            estado,
            COUNT(*) AS total
        FROM vehiculos
        GROUP BY estado
    """
    return pd.read_sql_query(sql, conn)


def export_excel(dataframes: dict, output_path: Path) -> None:
    output_path.parent.mkdir(exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def run():
    create_database()

    conn = sqlite3.connect(DB_PATH)

    df_itv = query_itv_pendientes(conn)
    df_facturas = query_costes_proveedor(conn)
    df_flota = query_resumen_flota(conn)

    conn.close()

    output_path = REPORTS_DIR / "reporte_operativo.xlsx"
    export_excel(
        {
            "ITV_Pendientes":   df_itv,
            "Costes_Proveedor": df_facturas,
            "Resumen_Flota":    df_flota,
        },
        output_path,
    )

    print(f"Report generated: {output_path}")
    print(f"\nITV pendientes ({len(df_itv)} vehicles):")
    print(df_itv.to_string(index=False))
    print(f"\nCostes por proveedor:")
    print(df_facturas.to_string(index=False))


if __name__ == "__main__":
    run()
