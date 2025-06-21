from models.task_manager import TaskManager
from analytics.visualization import generate_productivity_report
import sqlite3

def main():
    """Entry point for the task analytics system"""
    print("Initializing Task Analytics System...")
    
    
    conn = sqlite3.connect('tasks.db')
    task_manager = TaskManager(conn)
    
    
    task_manager.add_task("Complete Shipd project", priority=8, estimated_hours=20)
    task_manager.add_task("Write documentation", priority=5, estimated_hours=5)
    
    
    generate_productivity_report(task_manager.get_all_tasks())

if __name__ == "__main__":
    main()
