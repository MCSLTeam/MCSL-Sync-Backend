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
    "CatServer",
    "CraftBukkit",
    "Vanilla",
    "Fabric",
    "Forge",
]


def init_pre_database():
    for core_type in available_downloads:
        with sqlite3.connect(f"data/runtime/{core_type}.db"):
            pass


def init_production_database():
    for core_type in available_downloads:
        with sqlite3.connect(f"data/production/{core_type}.db"):
            pass


async def get_core_versions(database_type: str, core_type: str):
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as core:
        cursor = core.cursor()
        cursor.execute("SELECT name FROM sqlite_master where type='table'")
        version_list = [row[0] for row in cursor.fetchall()]
        return version_list


@SyncLogger.catch
def update_database(database_type: str, core_type: str, mcversion: str, builds: list):
    with sqlite3.connect(f"data/{database_type}/{core_type}.db") as database:
        cursor = database.cursor()
        try:
            cursor.execute(
                f"""
                    CREATE TABLE "{mcversion}" (
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
                DELETE FROM "{mcversion}"
                """
            )
        except sqlite3.OperationalError:
            pass
        for core_type in available_downloads:
            for build in builds:
                cursor.execute(
                    f"""
                    INSERT INTO "{mcversion}" (sync_time, download_url, core_type, mc_version, core_version)
                    VALUES (:sync_time, :download_url, :core_type, :mc_version, :core_version)
                    """,
                    build,
                )
        cursor.execute(
            f"""
            DELETE FROM "{mcversion}"
            WHERE ROWID NOT IN (
                SELECT MIN(ROWID)
                FROM "{mcversion}"
                GROUP BY sync_time, download_url, core_type, mc_version, core_version
            )
            """
        )
        cursor.execute(f"SELECT COUNT(*) FROM '{mcversion}'")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(f"DROP TABLE '{mcversion}'")
        database.commit()
