import time
import threading
import pystray
import tkinter as tk
from tkinter import messagebox, font
from playsound import playsound
import webbrowser

import utils
from icon_generator import create_image, get_image

# Define global variables
timer_thread = None
remaining_time = 0
running = False
window_shown = False

# Colors
light_blue = "#0076b3"
dark_blue = "#17426a"


def on_click(icon):
    global remaining_time
    formatted_time = utils.format_time(remaining_time)
    if running:
        icon.notify('Time Remaining: {}'.format(formatted_time))
    else:
        show_buttons_window()


def show_buttons_window():
    global window_shown
    if window_shown:
        return None

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    window_shown = True

    def start_timer(seconds):
        root.destroy()
        start_countdown(seconds)

    top = tk.Toplevel(root)
    top.title("Duration")

    # Remove the default window decorations and only show the close button
    top.overrideredirect(True)
    window_width = 300
    window_height = 60
    window_geometry = utils.get_window_geometry(window_width, window_height)
    top.geometry(window_geometry)
    top.attributes('-topmost', True)
    top.attributes('-alpha', 0.9)

    # Frame
    frame = tk.Frame(top, bg=light_blue, bd=2, border=2, relief='solid')
    frame.place(relx=0.5, rely=0.5, anchor='center', width=window_width, height=window_height)

    custom_font = font.Font(size=14, weight="bold", family="Calibri")

    # Close button
    close_button = tk.Button(frame, text="X", command=top.destroy, bd=1, bg="#FF0000", fg="#FAFAFA", justify='center', font=custom_font, relief='ridge')
    close_button.place(x=265, y=17, height=24)

    # Three buttons
    icon_five = tk.PhotoImage(file="assets/5min.png")
    icon_ten = tk.PhotoImage(file="assets/10min.png")
    icon_fifteen = tk.PhotoImage(file="assets/15min.png")

    button1 = tk.Button(
            frame, image=icon_five, command=lambda: start_timer(5*60), bg=light_blue, borderwidth="0")
    button2 = tk.Button(
            frame, image=icon_ten, command=lambda: start_timer(10*60), bg=light_blue, border="0")
    button3 = tk.Button(
            frame, image=icon_fifteen, command=lambda: start_timer(15*60), bg=light_blue, border="0")

    # Place buttons in a row with even distribution
    button1.place(relx=0.2, rely=0.5, anchor='center')
    button2.place(relx=0.45, rely=0.5, anchor='center')
    button3.place(relx=0.7, rely=0.5, anchor='center')

    root.mainloop()


def start_countdown(seconds):
    global timer_thread, remaining_time, running
    if running:
        return  # Prevent starting another timer if one is running
    remaining_time = seconds
    running = True
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()


def countdown():
    global remaining_time, running
    while remaining_time > 0:
        time.sleep(1)
        remaining_time -= 1
    playsound("assets/alert.mp3")
    flash_icon(tray_icon)
    running = False


def flash_icon(icon):
    for _ in range(10):
        icon.icon = create_image()
        time.sleep(0.5)
    tray_icon.icon = get_image()
    time.sleep(0.5)


def on_right_click(icon, item):
    if item == "About":
        return webbrowser.open('https://somethingreally.fun/about/')
    elif item == "Settings":
        return messagebox.showinfo("Settings", "This feature is still in development.", icon="INFO")
    elif item == "Quit":
        return icon.stop()


def create_menu(icon):
    # ToDo: turn it into a radio button
    return pystray.Menu(
            pystray.MenuItem('Start Timer', lambda: on_click(icon), default=True),
            pystray.MenuItem('About', lambda: on_right_click(icon, 'About')),
            pystray.MenuItem('Settings', lambda: on_right_click(icon, 'Settings')),
            pystray.MenuItem('Quit', lambda: on_right_click(icon, 'Quit')),
    )


tray_icon = pystray.Icon("test_icon")
tray_icon.icon = get_image()
tray_icon.title = "Pymodoro"
tray_icon.menu = create_menu(tray_icon)

tray_icon.run()
