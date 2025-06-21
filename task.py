class Task:
    def __init__(self, name, priority, estimated_hours):
        self.name = name
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.time_spent = 0
        
    def __repr__(self):
        return f"Task({self.name}, priority={self.priority})"