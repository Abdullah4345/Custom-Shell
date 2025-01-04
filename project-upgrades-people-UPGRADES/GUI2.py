import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os
import signal

CLI_PROGRAM = "CLI.py"

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shell")
        self.root.geometry("1200x650")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Header label
        self.header_label = tk.Label(
            self.root, text="𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝔹𝕒𝕤𝕚𝕔 𝕊𝕙𝕖𝕝𝕝", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="#00ff00"
        )
        self.header_label.pack(pady=10)

        # Terminal output widget
        self.output_widget = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Courier", 12), bg="#282c34", fg="#61afef", insertbackground="white", relief=tk.SUNKEN, borderwidth=2
        )
        self.output_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_widget.insert(tk.END, "𝕗𝕠𝕣 𝕞𝕠𝕣𝕖 𝕚𝕟𝕗𝕠 𝕥𝕪𝕡𝕖 𝕙𝕖𝕝𝕡....\n")
        self.output_widget.configure(state="disabled")

        # Command input widget
        self.command_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.command_frame.pack(fill=tk.X, padx=10, pady=5)

        self.command_label = tk.Label(
            self.command_frame, text="Command:", font=("Courier", 12), bg="#1e1e1e", fg="#00ff00"
        )
        self.command_label.pack(side=tk.LEFT, padx=5)

        self.command_input = tk.Entry(
            self.command_frame, font=("Courier", 12), bg="#282c34", fg="#ffffff", insertbackground="white"
        )
        self.command_input.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)
        self.command_input.bind("<Return>", self.send_command)

        # Subprocess handler
        self.process = None
        self.start_cli()

        # Handle close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set up SIGINT handling
        signal.signal(signal.SIGINT, self.handle_sigint)

    def start_cli(self):
        """Start the CLI program in a subprocess."""
        try:
            self.process = subprocess.Popen(
                ["python3", CLI_PROGRAM],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            threading.Thread(target=self.read_output, daemon=True).start()
        except Exception as e:
            self.write_output(f"Error starting CLI program: {e}\n")

    def read_output(self):
        """Continuously read output from the subprocess and display it."""
        if self.process and self.process.stdout:
            for line in iter(self.process.stdout.readline, ""):
                self.handle_output(line)

    def write_output(self, text):
        """Write text to the output widget."""
        self.output_widget.configure(state="normal")
        self.output_widget.insert(tk.END, text)
        self.output_widget.see(tk.END)
        self.output_widget.configure(state="disabled")

    def clear_output(self):
        """Clear the output widget."""
        self.output_widget.configure(state="normal")
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.configure(state="disabled")

    def handle_output(self, line):
        """Handle output from the subprocess, including clearing the screen."""
        if line.strip().lower() in ("clear", "cls"):
            self.clear_output()
        else:
            self.write_output(line)

    def send_command(self, event=None):
        """Send a command to the subprocess."""
        command = self.command_input.get().strip()
        if command:
            self.write_output(f"Command> {command}\n")
            if self.process and self.process.stdin:
                try:
                    self.process.stdin.write(command + "\n")
                    self.process.stdin.flush()
                except Exception as e:
                    self.write_output(f"Error sending command: {e}\n")
            if command.lower() in ("clear", "cls"):
                self.clear_output()
            self.command_input.delete(0, tk.END)

    def on_close(self):
        """Handle closing of the application."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.root.destroy()

    def handle_sigint(self, signal_number, frame):
        """Handle SIGINT (Ctrl+C) by sending SIGINT to the subprocess."""
        if self.process:
            self.write_output("\nCtrl+C pressed! Terminating the process...\n")
            self.process.send_signal(signal.SIGINT)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
