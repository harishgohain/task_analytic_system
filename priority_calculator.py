def calculate_priority_score(urgency, importance, deadline_proximity):
    """
    Advanced priority scoring algorithm
    Returns weighted priority score (0-10)
    """
    return min(10, (urgency * 0.4) + (importance * 0.5) + (deadline_proximity * 0.3))