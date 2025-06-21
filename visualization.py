import matplotlib.pyplot as plt
import pandas as pd

def generate_productivity_report(tasks):
    """Generate visual productivity report"""
    df = pd.DataFrame(tasks)
    df.plot(kind='bar', x='name', y='time_spent')
    plt.title('Task Time Allocation')
    plt.savefig('reports/time_allocation.png')