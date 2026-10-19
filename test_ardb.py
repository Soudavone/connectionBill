
import getpass
from pathlib import Path

import jaydebeapi
import jpype

# Driver information from DBeaver
DRIVER_CLASS = (
    "com.huawei.ngcbs.dbmanproxydriver.jdbc."
    "ZCloudProxyDriver"
)

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
        cursor.execute("SELECT 1")
        print("Test query result:", cursor.fetchall())

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
