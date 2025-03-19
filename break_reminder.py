import tkinter as tk
from tkinter import ttk
import time
import threading
import subprocess
from datetime import datetime, timedelta

class BreakReminder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Break Reminder")
        self.root.geometry("400x300")
        
        # Default break interval (in minutes)
        self.break_interval = tk.StringVar(value="20")
        
        # Create and pack widgets
        self.status_label = ttk.Label(self.root, text="Status: Not Running")
        self.status_label.pack(pady=10)
        
        # Break interval configuration
        interval_frame = ttk.Frame(self.root)
        interval_frame.pack(pady=10)
        
        ttk.Label(interval_frame, text="Break Interval (minutes):").pack(side=tk.LEFT, padx=5)
        self.interval_entry = ttk.Entry(interval_frame, textvariable=self.break_interval, width=8)
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_button = ttk.Button(interval_frame, text="Update", command=self.update_interval)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.time_label = ttk.Label(self.root, text="Next break in: --:--")
        self.time_label.pack(pady=15)
        
        self.start_button = ttk.Button(self.root, text="Stop", command=self.toggle_reminder)
        self.start_button.pack(pady=10)
        
        self.is_running = True
        self.reminder_thread = None
        self.next_break = None
        
        # Start the reminder automatically
        self.start_reminder()
        
    def toggle_reminder(self):
        if not self.is_running:
            self.start_reminder()
        else:
            self.stop_reminder()
    
    def update_interval(self):
        try:
            # Validate and update break interval
            interval = int(self.break_interval.get())
            if interval <= 0:
                raise ValueError("Interval must be positive")
            
            # Calculate new next break time
            current_time = datetime.now()
            self.next_break = current_time + timedelta(minutes=interval)
            self.status_label.config(text="Status: Running")
            
        except ValueError as e:
            self.status_label.config(text="Status: Invalid interval!")
    
    def start_reminder(self):
        try:
            # Validate and update break interval
            interval = int(self.break_interval.get())
            if interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError as e:
            self.status_label.config(text="Status: Invalid interval!")
            return
            
        self.is_running = True
        self.start_button.config(text="Stop")
        self.status_label.config(text="Status: Running")
        self.reminder_thread = threading.Thread(target=self.reminder_loop)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
    
    def stop_reminder(self):
        self.is_running = False
        self.start_button.config(text="Start")
        self.status_label.config(text="Status: Stopped")
        self.time_label.config(text="Next break in: --:--")
    
    def show_break_notification(self):
        # Show system notification using osascript
        subprocess.run([
            'osascript',
            '-e',
            'display notification "Take a 5-minute break to stretch and rest your eyes." with title "Break Time!"'
        ])
        
        # Bring window to front and make it stay on top
        self.root.after(0, self._bring_window_to_front)
        
        # Update status label
        self.status_label.config(text="Status: Break Time!")
        
        # Wait for 5 seconds before starting the next timer
        time.sleep(5)
        
        # Reset status and start next timer
        self.status_label.config(text="Status: Running")
        current_time = datetime.now()
        self.next_break = current_time + timedelta(minutes=int(self.break_interval.get()))
    
    def _bring_window_to_front(self):
        """Helper method to bring window to front and make it stay on top"""
        # Simple AppleScript to activate the application
        apple_script = '''
        tell application "System Events"
            tell process "Python"
                set frontmost to true
            end tell
        end tell
        '''
        
        # Execute the AppleScript
        subprocess.run(['osascript', '-e', apple_script])
        
        # Enhanced Tkinter window management
        self.root.update_idletasks()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        
        # Center the window on screen
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Schedule multiple focus attempts to ensure it works
        for i in range(3):
            self.root.after(i * 100, lambda: self.root.focus_force())
        
        # Remove topmost after 10 seconds
        self.root.after(10000, lambda: self.root.attributes('-topmost', False))
    
    def reminder_loop(self):
        while self.is_running:
            try:
                interval = int(self.break_interval.get())
                # Calculate next break time if not set
                if self.next_break is None:
                    current_time = datetime.now()
                    self.next_break = current_time + timedelta(minutes=interval)
                
                # Update time label every second
                while self.is_running:
                    current_time = datetime.now()
                    time_until_break = self.next_break - current_time
                    
                    if time_until_break.total_seconds() <= 0:
                        # Time for a break
                        self.show_break_notification()
                        time_until_break = self.next_break - datetime.now()
                    
                    minutes = int(time_until_break.total_seconds() // 60)
                    seconds = int(time_until_break.total_seconds() % 60)
                    self.time_label.config(text=f"Next break in: {minutes:02d}:{seconds:02d}")
                    time.sleep(1)
                    
            except ValueError:
                self.status_label.config(text="Status: Invalid interval!")
                self.stop_reminder()
                break
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BreakReminder()
    app.run() 