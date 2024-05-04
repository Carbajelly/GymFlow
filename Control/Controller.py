import random
import time
from View import App
import asyncio
import sys
import os
#Acts as the camera_detection
from Emulator import Emulator 
import threading

from src.camera_detection import *


class Controller():
    def __init__(self, source=None):
        #source can either be the model or the emulator
        if not source:
            self.source = source 
        self.App = App(self)
        self.loop = asyncio.get_event_loop()

    def test_detect_input(self): 
        for input_value in self.source.emulate():
            print(input_value)
            self.change_color(input_value)
            self.sleep_random_time(0.5,20)

    def model_input(self):
        thread = threading.Thread(target=run_visual_model)
        thread.daemon = True
        thread.start
        while True:
            input_value = get_bench_status() 
            self.change_color(input_value)
    
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
