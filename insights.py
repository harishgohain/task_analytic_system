from typing import List
import numpy as np
from datetime import datetime
from .visualization import plot_trend

class TaskInsights:
    @staticmethod
    def calculate_eisenhower_matrix(tasks: List[Task]) -> dict:
        """Categorize tasks into Eisenhower Matrix quadrants"""
        matrix = {
            "urgent_important": [],
            "not_urgent_important": [],
            "urgent_not_important": [],
            "not_urgent_not_important": []
        }
        
        for task in tasks:
            urgency = 1 if task.deadline and (datetime.strptime(task.deadline, '%Y-%m-%d') - datetime.now()).days < 3 else 0
            if urgency and task.priority >= 7:
                matrix["urgent_important"].append(task)
            elif not urgency and task.priority >= 7:
                matrix["not_urgent_important"].append(task)
            elif urgency and task.priority < 7:
                matrix["urgent_not_important"].append(task)
            else:
                matrix["not_urgent_not_important"].append(task)
        return matrix

    @staticmethod
    def predict_completion(tasks: List[Task], hours_per_day: float = 8) -> dict:
        """Forecast completion timeline"""
        pending = [t for t in tasks if t.status != 'completed']
        total_hours = sum(t.estimated_hours - t.time_spent for t in pending)
        work_days = total_hours / hours_per_day
        
        return {
            "total_pending": len(pending),
            "estimated_days": np.ceil(work_days),
            "critical_path": sorted(
                [t for t in pending if t.priority >= 8],
                key=lambda x: x.deadline if x.deadline else '9999-12-31'
            )
        }

    @staticmethod
    def analyze_productivity(tasks: List[Task]) -> dict:
        """Calculate productivity metrics"""
        completed = [t for t in tasks if t.status == 'completed']
        if not completed:
            return {}
            
        avg_accuracy = np.mean(
            [t.time_spent / t.estimated_hours for t in completed 
             if t.estimated_hours > 0]
        )
        
        return {
            "tasks_completed": len(completed),
            "time_vs_estimate": avg_accuracy,
            "priority_efficiency": np.mean(
                [t.priority for t in completed]
            ) / 10,
            "trend_data": plot_trend(tasks)
        }