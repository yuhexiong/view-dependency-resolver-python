import os
import re
from typing import Dict, Set

import pymysql
from dotenv import load_dotenv

from utils import load_db_config


def get_views(cursor) -> Set[str]:
    """
    取得 view 清單。
    """

    cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW';")
    return {row[0] for row in cursor.fetchall()}


def export_view_definitions(cursor, views: Set[str]) -> Dict[str, str]:
    """
    取得每個 view 的建立語法。
    """

    view_definitions = {}
    for view in views:
        cursor.execute(f"SHOW CREATE VIEW `{view}`;")
        result = cursor.fetchone()
        if result and len(result) >= 2:
            view_definitions[view] = result[1]
    return view_definitions


def extract_view_dependencies(view_definitions: Dict[str, str]) -> Dict[str, Set[str]]:
    """
    使用正則表達式由建立語法取得使用的 view 名稱。
    """

    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")

    pattern = re.compile(
        rf"`internal`\.`default_cluster:{re.escape(DB_NAME)}`\.`([^`]+)`")

    dependency_map = {}
    for view_name, ddl in view_definitions.items():
        matches = pattern.findall(ddl)
        # 過濾非 view 名（使用 view_definitions 中已知名稱來篩選）
        views = {m for m in matches if m in view_definitions}
        dependency_map[view_name] = sorted(views)

    return dependency_map


def fetch_dependencies() -> Dict[str, Set[str]]:
    """
    取得 view 依賴關聯。
    """

    # 連線到資料庫
    db_config = load_db_config()
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        # 取得 view 清單
        views = get_views(cursor)

        # 取得每個 view 的建立語法
        view_defs = export_view_definitions(cursor, views)

        # 使用正則表達式由建立語法取得使用的 view 名稱
        extra_view_deps = extract_view_dependencies(view_defs)

        return extra_view_deps

    finally:
        # 關閉連線
        cursor.close()
        conn.close()
