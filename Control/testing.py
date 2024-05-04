from Emulator import Emulator
import time
from Controller import Controller
from View import App
import threading


def test_emulator():
    emulator = Emulator()
    for value in emulator.emulate():
        return(value)

def test_controller(source):
    controller_test = Controller(source)
    controller_test.run()

def main():
   #TEST FOR EMULATOR
    #for _ in range(100):
    #    time.sleep(5)
    #    print(test_emulator())
    emulator = Emulator()
    test_controller(emulator)    

if __name__ == "__main__":
    main()