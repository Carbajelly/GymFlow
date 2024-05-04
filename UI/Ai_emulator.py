import itertools
import random
import threading
import time

class BinaryGenerator:
    def __init__(self):
        self.cycle = itertools.cycle([(0, 0), (0, 1), (1, 0), (1, 1)])
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.generate_binary_sequence)
    
    def generate_binary_sequence(self):
        while not self.stop_event.is_set():
            interval = random.uniform(0.1, 1.0)  # Random interval between 0.1 and 1.0 seconds
            time.sleep(interval)
            binary_tuple = next(self.cycle)
            print(binary_tuple)  # Print the generated tuple, you can modify this to return the tuple instead of printing
            # You can add your desired action here, like appending the tuple to a list or calling a function with the tuple as an argument
    
    def start(self):
        self.thread.start()
    
    def stop(self):
        self.stop_event.set()
        self.thread.join()

# Example usage:
if __name__ == "__main__":
    generator = BinaryGenerator()  # Create an instance
    generator.start()  # Start generating binary tuples at random intervals
    # Wait for some time to see the output, or perform other operations
    time.sleep(5)
    generator.stop()  # Stop generating binary tuples


