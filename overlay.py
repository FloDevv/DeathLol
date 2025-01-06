import tkinter as tk
import logging
import json

class DeathOverlay:
    def __init__(self):
        # Load config
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        self.root = tk.Tk()
        self.root.title("Death Overlay")

        window_width = 800
        window_height = 200

        # Position window in center of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.attributes('-alpha', 0.8)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', 'black')
        self.root.configure(bg='black')

        self.label = tk.Label(
            self.root,
            text=self.config['overlay_text'],
            font=(self.config['font_family'], self.config['font_size'], "bold"),
            fg=self.config['text_color'],
            bg="black",
            wraplength=window_width
        )
        self.label.pack(expand=True, fill="both")
        self.hide_overlay()

    def show_overlay(self):
        self.root.deiconify()
        logging.info("Showing death overlay")

    def hide_overlay(self):
        self.root.withdraw()
        logging.info("Hiding death overlay")

    def update(self):
        self.root.update()
