import tkinter as tk
from tkinter import messagebox
import random
from threading import Thread
import time

class MissingNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Find the Missing Number")
        self.root.geometry("800x600")
        self.root.configure(bg="#f3f4f6")

        self.attempts = 0
        self.missing_number = None
        self.numbers = []
        self.timer_value = 60
        self.game_running = False

        # Start Button
        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 16, "bold"), bg="#007bff", fg="white", command=self.start_loading)
        self.start_button.pack(pady=20)

        # Loading Bar Area
        self.loading_area = tk.Frame(root, bg="#f3f4f6")
        self.loading_bar = tk.Frame(self.loading_area, bg="#007bff", height=20, width=0)
        self.loading_bar.pack(side="left")
        self.loading_text = tk.Label(self.loading_area, text="0%", font=("Arial", 16), bg="#f3f4f6")
        self.loading_text.pack(side="left", padx=10)

        # Game Area
        self.game_area = tk.Frame(root, bg="#f3f4f6")
        self.timer_label = tk.Label(self.game_area, text=f"{self.timer_value}s", font=("Arial", 16, "bold"), fg="#ffcccc", bg="#f3f4f6")
        self.timer_label.pack(anchor="ne", pady=10, padx=10)

        self.instructions = tk.Label(self.game_area, text="Find the missing number from the grid below:", font=("Arial", 14), bg="#f3f4f6")
        self.instructions.pack(pady=10)

        self.grid_frame = tk.Frame(self.game_area, bg="#f3f4f6")
        self.grid_frame.pack(pady=20)

        self.input_guess = tk.Entry(self.game_area, font=("Arial", 14), width=10)
        self.input_guess.pack(pady=10)

        self.submit_button = tk.Button(self.game_area, text="Submit", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(self.game_area, text="", font=("Arial", 16, "bold"), bg="#f3f4f6")
        self.feedback_label.pack(pady=20)

        self.reset_button = tk.Button(self.game_area, text="Play Again", font=("Arial", 14, "bold"), bg="#007bff", fg="white", command=self.reset_game)
        self.reset_button.pack(pady=10)
        self.reset_button.pack_forget()

    def start_loading(self):
        self.start_button.pack_forget()
        self.loading_area.pack(pady=20)

        def loading_animation():
            for i in range(101):
                time.sleep(0.05)
                self.loading_bar.config(width=i * 4)
                self.loading_text.config(text=f"{i}%")
                self.root.update()
            self.loading_area.pack_forget()
            self.start_game()

        Thread(target=loading_animation).start()

    def start_game(self):
        self.game_area.pack(pady=20)
        self.reset_game()
        self.start_timer()

    def generate_numbers(self):
        self.numbers = list(range(1, 101))
        self.missing_number = random.choice(self.numbers)
        self.numbers.remove(self.missing_number)
        random.shuffle(self.numbers)

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for num in self.numbers:
            label = tk.Label(self.grid_frame, text=num, font=("Arial", 12), bg="white", width=3, height=2, relief="solid", borderwidth=1)
            label.pack(side="left", padx=2, pady=2)

    def start_timer(self):
        self.timer_value = 60
        self.game_running = True

        def timer_countdown():
            while self.timer_value > 0 and self.game_running:
                self.timer_value -= 1
                self.timer_label.config(text=f"{self.timer_value}s")
                time.sleep(1)
                self.root.update()
            if self.game_running:
                messagebox.showinfo("Time Up", "Time's up! You failed to find the missing number.")
                self.end_game()

        Thread(target=timer_countdown).start()

    def check_answer(self):
        try:
            guess = int(self.input_guess.get())
            if guess == self.missing_number:
                self.feedback_label.config(text="Correct! You found the missing number!", fg="green")
                self.end_game()
            else:
                self.feedback_label.config(text="Wrong! Try again.", fg="red")
                self.attempts += 1
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.", fg="orange")

    def reset_game(self):
        self.attempts = 0
        self.feedback_label.config(text="")
        self.input_guess.delete(0, tk.END)
        self.generate_numbers()

    def end_game(self):
        self.game_running = False
        self.reset_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MissingNumberGame(root)
    root.mainloop()
