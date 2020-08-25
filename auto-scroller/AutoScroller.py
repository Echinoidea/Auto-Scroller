# @date 2020-08-25
# @author Gabriel Hooks
# Simulate scroll wheel at x speed controlled by PGUP and PGDN

import time
import threading
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key

mouse = Controller()

key_scroll_up = Key.page_up
key_scroll_down = Key.page_down
key_terminate = Key.end


class Scroller(threading.Thread):

    def __init__(self, button):
        super(Scroller, self).__init__()
        self.button = button
        self.running = False
        self.scroll_direction = 1  # -1 = down; 1 = up
        self.program_running = True

    def start_scrolling(self, direction):
        self.running = True
        self.scroll_direction = direction
        print("Started scrolling")

    def stop_scrolling(self):
        self.running = False
        print("Stopped scrolling")

    def terminate(self):
        self.stop_scrolling()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.scroll(0, 1 * self.scroll_direction)
                time.sleep(0.001)


scroll_thread = Scroller(key_scroll_up)
scroll_thread.start()
print("Press PGUP/PGDN to start/stop auto scrolling. Press 'END' to terminate the program...")


def on_press(key):
    if key == key_scroll_up:
        if scroll_thread.running:
            scroll_thread.stop_scrolling()
        else:
            scroll_thread.start_scrolling(1)
    elif key == key_scroll_down:
        if scroll_thread.running:
            scroll_thread.stop_scrolling()
        else:
            scroll_thread.start_scrolling(-1)
    elif key == key_terminate:
        scroll_thread.terminate()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()

listener.stop()
