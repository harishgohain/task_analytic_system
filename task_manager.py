import sqlite3
from typing import List
from .task import Task

class TaskManager:
    def __init__(self, connection):
        self.conn = connection
        self._create_tables()
    
    def _create_tables(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                priority INTEGER,
                estimated_hours REAL,
                time_spent REAL
            )
        ''')
        self.conn.commit()
    
    def add_task(self, name: str, priority: int, estimated_hours: float):
        """Add a new task to the system"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (name, priority, estimated_hours, time_spent) VALUES (?, ?, ?, 0)",
            (name, priority, estimated_hours)
        )
        self.conn.commit()
    
    def get_all_tasks(self) -> List[dict]:
        """Retrieve all tasks as dictionaries"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return [dict(row) for row in cursor.fetchall()]
    def update_time(self, task_id: int, hours: float) -> bool:
        """Log time spent on task"""
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE tasks 
        SET time_spent = time_spent + ?, 
            status = CASE 
                WHEN time_spent + ? >= estimated_hours THEN 'completed' 
                ELSE status 
            END
        WHERE id = ?
        """, (hours, hours, task_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks past deadline"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM tasks 
        WHERE deadline < datetime('now') 
        AND status != 'completed'
        """)
        return [Task(**dict(row)) for row in cursor.fetchall()]

    def generate_report(self) -> Dict:
        """Generate summary statistics"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(time_spent) as total_hours,
            AVG(priority) as avg_priority,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count
        FROM tasks
        """)
        return dict(cursor.fetchone())
