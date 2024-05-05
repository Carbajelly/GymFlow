import threading

class BenchTracker:
    def __init__(self):
        self.bench_count = 0
        self.last_input = None
        self.lock = threading.Lock()

    def update_input(self, input_value):
        with self.lock:
            if input_value != self.last_input:
                self.input_count += 1
                self.last_input = input_value
    
    def get_usage_count(self):
        with self.lock:
            return self.input_count
    
    def reset_usage_count(self):
        with self.lock:
            self.input_count = 0
    
    def get_last_input(self):
        with self.lock:
            return self.last_input
    