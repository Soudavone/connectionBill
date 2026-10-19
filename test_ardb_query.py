import csv
import getpass
from pathlib import Path

import jaydebeapi
import jpype

DRIVER_CLASS = "com.huawei.ngcbs.dbmanproxydriver.jdbc.ZCloudProxyDriver"
JDBC_URL = (
    "jdbc:zcloudproxy@172.28.235.92:21800"
    "?cluster=billdb&vnode=107&mode=native"
)
JAR_DIR = Path(r"D:\javefile")
JAR_FILES = [
    str(JAR_DIR / "dbmanproxydriver.jar"),
    str(JAR_DIR / "com.huawei.gauss.jdbc.ZenithDriver-1.2.1.jar"),
    str(JAR_DIR / "fastjson.jar"),
]
QUERY = "SELECT *\nFROM AR_PAYMENT LIMIT 100"


def export_query_to_csv(cursor, output_path):
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        writer.writerows(rows)

    return rows


def main():
    for jar in JAR_FILES:
        if not Path(jar).is_file():
            raise FileNotFoundError(f"JDBC JAR not found: {jar}")

    username = input("Username: ")
    password = getpass.getpass("Password: ")
    connection = None
    cursor = None

    try:
        print("Connecting to ARDB...")

        if not jpype.isJVMStarted():
            jpype.startJVM(
                jpype.getDefaultJVMPath(),
                "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
                classpath=JAR_FILES,
                convertStrings=True,
            )

        connection = jaydebeapi.connect(
            DRIVER_CLASS,
            JDBC_URL,
            [username, password],
            JAR_FILES,
        )
        print("Connection successful!")

        cursor = connection.cursor()
        cursor.execute(QUERY)
        print("Columns:", [column[0] for column in cursor.description])

        output_path = Path(__file__).with_name("AR_PAYMENT.csv")
        rows = export_query_to_csv(cursor, output_path)
        print(f"Returned {len(rows)} row(s):")
        for row in rows:
            print(row)
        print(f"CSV exported to: {output_path}")

    except Exception as error:
        print("Connection or query failed:")
        print(type(error).__name__, str(error))
        if hasattr(error, "printStackTrace"):
            error.printStackTrace()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
