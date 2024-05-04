import random

class Emulator:
    def __init__(self):
        self.choices = [(0, 0), (0, 1), (1, 0), (1, 1)]

    def gen_random_choice(self):
        return random.choice(self.choices)
        
    def gen_realistic_example(self):
        #Meant to provide a simple example of what may be detected
        long_example = []
        for _ in range(30):
            long_example.append(self.gen_random_choice())
        
        return long_example
    
    def emulate(self):
        i = 0
        emulation_values = self.gen_realistic_example()
        while i < len(emulation_values):
            yield emulation_values[i]
            i = i + 1
        
        return 0