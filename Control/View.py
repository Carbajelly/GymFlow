import tkinter as tk
import customtkinter
import os
from PIL import Image
from Emulator import *

class App(customtkinter.CTk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        self.title("GymFlow")
        self.geometry("1024x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  GymFlow!", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=100, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=100, border_spacing=10, text="Admin View",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")


        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        #2x2 frame for each bench; should expand as more benches are included
        self.home_frame.grid(row=3, column=3, sticky="ew")
        self.home_frame.rowconfigure(1, weight=1)
        self.home_frame.rowconfigure(0, weight=1)
        self.home_frame.columnconfigure(1, weight= 1)
        self.home_frame.columnconfigure(2, weight= 1)

        self.bench_1Label = customtkinter.CTkLabel(self.home_frame, text="Bench 1", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.bench_1Label.grid(row=0, column=1)
        self.bench_1 = CustomRectangle(self.home_frame, width=200, height=400, color="green")
        self.bench_1.grid(row=1, column=1)

        self.bench1_timer = Timer(self.home_frame)
        self.bench1_timer.grid(row=2, column=1)
        self.bench1_timer.start_timer()


        self.bench_2Label = customtkinter.CTkLabel(self.home_frame, text="Bench 2", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.bench_2Label.grid(row=0, column=2)
        self.bench_2 = CustomRectangle(self.home_frame, width=200, height=400, color="green")
        self.bench_2.grid(row=1, column=2, pady=10)


        self.bench2_timer = Timer(self.home_frame)
        self.bench2_timer.grid(row=2, column=2, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")


        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def change_bench_color(self, bench, color):
        if bench == "ben1":
            self.bench_1.change_color(color)
        elif bench == "ben2":
            self.bench_2.change_color(color)

    def start_bench_timer(self, bench):
        if bench == "ben1":
            self.bench1_timer.start_timer()
        elif bench == "ben2":
            self.bench2_timer.start_timer()

    def stop_bench_timer(self, bench):
        if bench == "ben1":
            self.bench1_timer.stop_timer()
        elif bench == "ben2":
            self.bench2_timer.stop_timer()


class CustomRectangle (tk.Canvas):
    def __init__(self, master, width, height, color, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.rectangle = self.create_rectangle(0, 0, width, height, fill=color)
        
    def change_color(self, new_color):
        self.itemconfig(self.rectangle, fill=new_color)
        self.color = new_color

class Timer(tk.Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        

        self.timer_label = customtkinter.CTkLabel(self, text="00:00", font=("Arial", 24))
        self.timer_label.grid(row=0, column=0, columnspan=3, pady=5)


        self.timer_running = False
        self.seconds = 0
        self.timer_id = None

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
            self.timer_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
    
    def reset_timer(self):
        self.stop_timer()
        self.seconds = 0
        self.update_timer()

    def update_timer(self):
        self.seconds += 1
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.timer_id = self.after(1000, self.update_timer)


if __name__ == "__main__":
    app = App()
    app.mainloop()
