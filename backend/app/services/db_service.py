import aiosqlite
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path

class DatabaseService:
    def __init__(self, db_path: str = "backend/data/comparisons.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS comparisons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    similarity_score INTEGER,
                    form_data TEXT,
                    extracted_data TEXT,
                    field_scores TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
    
    async def save_comparison(self, score: int, form_data: dict, extracted_data: dict, field_scores: dict) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                '''INSERT INTO comparisons (similarity_score, form_data, extracted_data, field_scores)
                   VALUES (?, ?, ?, ?)''',
                (score, json.dumps(form_data), json.dumps(extracted_data), json.dumps(field_scores))
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_history(self, limit: int = 10) -> List[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT * FROM comparisons ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_comparison(self, comparison_id: int) -> Optional[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT * FROM comparisons WHERE id = ?',
                (comparison_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

