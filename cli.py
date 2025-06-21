import click
from models.task_manager import TaskManager
from analytics.insights import TaskInsights

@click.group()
def cli():
    """Task Analytics System CLI"""

@cli.command()
@click.option('--name', prompt=True, help='Task name')
@click.option('--priority', type=int, default=5, help='Priority (1-10)')
@click.option('--hours', type=float, prompt=True, help='Estimated hours')
def add(name, priority, hours):
    """Add a new task"""
    manager = TaskManager()
    task = manager.add_task(name, priority=priority, estimated_hours=hours)
    click.echo(f"Added task #{task.id}: {task.name}")

@cli.command()
@click.argument('task_id', type=int)
@click.argument('hours', type=float)
def log(task_id, hours):
    """Log time to task"""
    manager = TaskManager()
    if manager.update_time(task_id, hours):
        click.echo(f"Logged {hours}h to task #{task_id}")
    else:
        click.echo("Task not found!")

@cli.command()
def report():
    """Generate analytics report"""
    manager = TaskManager()
    tasks = manager.get_all_tasks()
    
    insights = TaskInsights()
    click.echo("\n📊 Eisenhower Matrix:")
    matrix = insights.calculate_eisenhower_matrix(tasks)
    for quadrant, items in matrix.items():
        click.echo(f"{quadrant.replace('_', ' ').title()}: {len(items)} tasks")
    
    forecast = insights.predict_completion(tasks)
    click.echo(f"\n⏳ Completion Forecast: {forecast['estimated_days']} work days")
    
if __name__ == '__main__':
    cli()