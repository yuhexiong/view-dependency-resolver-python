import os
import re
import pymysql
from typing import Dict, Set
from utils import load_db_config
from dotenv import load_dotenv


def get_views(cursor) -> Set[str]:
    cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW';")
    return {row[0] for row in cursor.fetchall()}


def export_view_definitions(cursor, views: Set[str]) -> Dict[str, str]:
    view_definitions = {}
    for view in views:
        cursor.execute(f"SHOW CREATE VIEW `{view}`;")
        result = cursor.fetchone()
        if result and len(result) >= 2:
            view_definitions[view] = result[1]
    return view_definitions


def extract_view_dependencies(view_definitions: Dict[str, str]) -> Dict[str, Set[str]]:
    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")

    pattern = re.compile(rf"`internal`\.`default_cluster:{re.escape(DB_NAME)}`\.`([^`]+)`")

    dependency_map = {}
    for view_name, ddl in view_definitions.items():
        matches = pattern.findall(ddl)
        # 過濾非 view 名（這裡假設用 view_definitions 中已知名稱來篩選）
        views = {m for m in matches if m in view_definitions}
        dependency_map[view_name] = sorted(views)
    return dependency_map


def fetch_dependencies() -> Dict[str, Set[str]]:
    db_config = load_db_config()
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    try:
        views = get_views(cursor)
        view_defs = export_view_definitions(cursor, views)
        return extract_view_dependencies(view_defs)
    finally:
        cursor.close()
        conn.close()
