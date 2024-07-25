import sqlite3
from .logger import SyncLogger

available_downloads = [
    "Arclight",
    "Lightfall",
    "LightfallClient",
    "Banner",
    "Mohist",
    "Spigot",
    "BungeeCord",
    "Leaves",
    "Pufferfish",
    "Pufferfish+",
    "Pufferfish+Purpur",
    "SpongeForge",
    "SpongeVanilla",
    "Paper",
    "Folia",
    "Travertine",
    "Velocity",
    "Waterfall",
    "Purpur",
    "Purformance",
    "CatServer",
    "Craftbukkit",
    "Vanilla",
    "Fabric",
    "Forge",
    "Akarin",
    "NukkitX",
    "Thermos",
    "Contigo",
    "Luminol",
    "LightingLuminol",
    "Geyser",
    "Floodgate",
]


def init_database() -> None:
    for core_type in available_downloads:
        with sqlite3.connect(f"data/runtime/{core_type}.db"):
            pass


async def get_mc_versions(database_type: str, core_type: str) -> list[str]:
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as core:
        cursor = core.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        version_list = sorted([row[0] for row in cursor.fetchall()], reverse=True)
        return version_list


async def get_core_versions(
    database_type: str, core_type: str, mc_version: str
) -> list[str]:
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as core:
        cursor = core.cursor()
        cursor.execute(f"SELECT core_version FROM '{mc_version}' ORDER BY core_version")
        version_list = sorted([row[0] for row in cursor.fetchall()], reverse=True)
        return version_list


async def get_specified_core_data(
    database_type: str, core_type: str, mc_version: str, core_version: str
) -> dict[str, str]:
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as core:
        cursor = core.cursor()
        cursor.execute(
            f"SELECT * FROM '{mc_version}' WHERE core_version='{core_version}'"
        )
        columns = [column[0] for column in cursor.description]
        core_data = [dict(zip(columns, row)) for row in cursor.fetchall()][0]
        return core_data


@SyncLogger.catch
def update_database(
    database_type: str, core_type: str, mc_version: str, builds: list
) -> None:
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as database:
        cursor = database.cursor()
        try:
            cursor.execute(
                f"""
                    CREATE TABLE "{mc_version}" (
                        sync_time TEXT,
                        download_url TEXT,
                        core_type TEXT,
                        mc_version TEXT,
                        core_version TEXT
                    )
                    """
            )
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute(
                f"""
                DELETE FROM "{mc_version}"
                """
            )
        except sqlite3.OperationalError:
            pass
        for core_type in available_downloads:
            for build in builds:
                cursor.execute(
                    f"""
                    INSERT INTO "{mc_version}" (sync_time, download_url, core_type, mc_version, core_version)
                    VALUES (:sync_time, :download_url, :core_type, :mc_version, :core_version)
                    """,
                    build,
                )
        cursor.execute(
            f"""
            DELETE FROM "{mc_version}"
            WHERE ROWID NOT IN (
                SELECT MIN(ROWID)
                FROM "{mc_version}"
                GROUP BY sync_time, download_url, core_type, mc_version, core_version
            )
            """
        )
        cursor.execute(f"SELECT COUNT(*) FROM '{mc_version}'")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(f"DROP TABLE '{mc_version}'")
        database.commit()


async def optimize_core_data(database_type: str = "runtime") -> None:
    for core_type in available_downloads:
        with sqlite3.connect(f"data/{database_type}/{core_type}.db") as core:
            cursor = core.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_list = [row[0] for row in cursor.fetchall()]
            for table_name in table_list:
                cursor.execute(
                    f"SELECT * FROM '{table_name}' ORDER BY ROWID DESC LIMIT 35"
                )
                rows = cursor.fetchall()
                cursor.execute(f"DELETE FROM '{table_name}'")
                cursor.executemany(
                    f"INSERT INTO '{table_name}' VALUES (?, ?, ?, ?, ?)", rows
                )
                cursor.execute(f"SELECT COUNT(*) FROM '{table_name}'")
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.execute(f"DROP TABLE '{table_name}'")
            core.commit()
