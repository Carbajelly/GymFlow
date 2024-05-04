import random
import time
from View import App
#Acts as the camera_detection
from Emulator import Emulator 
import threading

from src.camera_detection import *


class Controller():
    def __init__(self, source=None):
        #source can either be the model or the emulator
        if source != None:
            self.source = source 
        self.App = App(self)

        self.buffer_timer = None
        self.last_input = None        

    def test_detect_input(self): 
        for input_value in self.source.emulate():
            print(input_value)
            self.change_color(input_value)
            self.sleep_random_time(0.5,20)

    def model_input(self):
        thread = threading.Thread(target=run_visual_model)
        thread.daemon = True
        thread.start()
        while True:
            input_value = get_bench_status()
            if input_value == self.last_input:
                self.reset_buffer_timer(input_value)
            else:
                self.start_buffer_timer(input_value)

            self.change_color(input_value)
    
    def start_buffer_timer(self, input_value):
        if self.buffer_timer is not None and self.buffer_timer.is_alive():
        
            self.buffer_timer.cancel()
        
        self.buffer_timer = threading.Timer(3, self.control_bench_timer(input_value))  # 5 seconds buffer time

    def reset_buffer_timer(self, input_value):
        if self.buffer_timer is not None and self.buffer_timer.is_alive():
            # Reset the timer if it's already running
            self.buffer_timer.cancel()
            self.buffer_timer = threading.Timer(3, self.control_bench_timer(input_value))  # 5 seconds buffer time
            self.buffer_timer.start()

    def change_color(self, input_value):
        ben1, ben2 = input_value
        if ben1 == 1 and ben2 == 0:
            self.App.change_bench_color("ben1", "red")
            self.App.change_bench_color("ben2", "green")
        elif ben1==0 and ben2==1:
            self.App.change_bench_color("ben1", "green")
            self.App.change_bench_color("ben2", "red")
        elif ben1==1 and ben2==1:
            self.App.change_bench_color("ben1", "red")
            self.App.change_bench_color("ben2", "red")
        else:
            self.App.change_bench_color("ben1", "green")
            self.App.change_bench_color("ben2", "green")
    
    def control_bench_timer(self, input_value):
        ben1, ben2 = input_value
        if ben1 == 1 and ben2 == 0:
            self.App.start_bench_timer("ben1")
            self.App.stop_bench_timer("ben2")       
        elif ben1==0 and ben2==1:
            self.App.start_bench_timer("ben2")
            self.App.stop_bench_timer("ben1")       
        elif ben1==1 and ben2==1:
            self.App.start_bench_timer("ben1")
            self.App.start_bench_timer("ben2")
        else:
            self.App.stop_bench_timer("ben1")
            self.App.stop_bench_timer("ben2")




    def sleep_random_time(self, min_seconds, max_seconds):
        sleep_time = random.uniform(min_seconds,max_seconds)
        time.sleep(sleep_time)   
    
    def start_input_source(self):
        if isinstance(self.source, Emulator):
            thread = threading.Thread(target=self.test_detect_input)
        else:
            thread = threading.Thread(target=self.model_input)
        thread.daemon = True
        thread.start()


    def run(self):
        self.start_input_source()
        self.App.mainloop()
