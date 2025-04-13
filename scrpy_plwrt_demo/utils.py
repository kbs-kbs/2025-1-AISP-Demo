class DataCollector:
    def __init__(self):
        self.items = []
    
    def collect_item(self, item):
        self.items.append(dict(item))