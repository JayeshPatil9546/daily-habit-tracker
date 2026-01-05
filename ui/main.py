"""
Daily Habit Tracker - Tkinter Desktop UI
Modern graphical interface for tracking daily habits
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
from datetime import datetime, date
from typing import List, Dict
import os

class HabitTrackerUI:
    """Main Tkinter UI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Habit Tracker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # API Configuration
        self.api_url = os.getenv('API_URL', 'http://localhost:5000/api')
        self.user_id = 1  # Demo user
        
        # Style Configuration
        self.root.configure(bg='#f0f0f0')
        self.style = ttk.Style()
        self.setup_styles()
        
        # Data
        self.habits = []
        self.daily_logs = {}
        
        # Create UI
        self.create_widgets()
        self.load_habits()
        
    def setup_styles(self):
        """Configure ttk styles"""
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Normal.TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="📋 Daily Habit Tracker", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        date_label = ttk.Label(header_frame, text=f"Today: {date.today().strftime('%A, %B %d, %Y')}", style='Normal.TLabel')
        date_label.pack(side=tk.RIGHT)
        
        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="➕ Add Habit", command=self.add_habit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Analytics", command=self.show_analytics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📅 Calendar", command=self.show_calendar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", command=self.load_habits).pack(side=tk.LEFT, padx=5)
        
        # Main Content Frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Habits List Label
        list_label = ttk.Label(content_frame, text="Today's Habits", style='Heading.TLabel')
        list_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Scrollable Frame for Habits
        canvas = tk.Canvas(content_frame, bg='white', highlightthickness=1)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scrollable_frame = scrollable_frame
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status Bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
        
    def load_habits(self):
        """Load habits from API"""
        try:
            self.status_label.config(text="Loading habits...")
            self.root.update()
            
            response = requests.get(f"{self.api_url}/habits?user_id={self.user_id}")
            
            if response.status_code == 200:
                self.habits = response.json()
                self.display_habits()
                self.status_label.config(text=f"Loaded {len(self.habits)} habits")
            else:
                messagebox.showerror("Error", "Failed to load habits from API")
                self.status_label.config(text="Error loading habits")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", "Cannot connect to API. Make sure the Flask server is running on port 5000")
            self.status_label.config(text="Connection failed")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading habits: {str(e)}")
            self.status_label.config(text="Error occurred")
    
    def display_habits(self):
        """Display habits as checkboxes in the UI"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.habits:
            empty_label = ttk.Label(self.scrollable_frame, text="No habits yet. Add one to get started!")
            empty_label.pack(pady=20)
            return
        
        for habit in self.habits:
            self.create_habit_card(habit)
    
    def create_habit_card(self, habit):
        """Create a card for each habit"""
        card_frame = ttk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=1)
        card_frame.pack(fill=tk.X, pady=5, padx=2)
        
        # Checkbox and Habit Name
        content_frame = ttk.Frame(card_frame)
        content_frame.pack(fill=tk.X, padx=10, pady=8)
        
        # Checkbox
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(
            content_frame, 
            text=f"{habit.get('icon', '🎯')} {habit['name']}",
            variable=var,
            command=lambda h=habit, v=var: self.log_habit_completion(h, v)
        )
        checkbox.pack(side=tk.LEFT, anchor=tk.W, expand=True)
        
        # Category Badge
        category = habit.get('category', 'general').upper()
        badge = ttk.Label(content_frame, text=category, font=('Arial', 8))
        badge.pack(side=tk.RIGHT, padx=5)
        
        # Delete Button
        delete_btn = ttk.Button(
            content_frame,
            text="✕",
            width=2,
            command=lambda h=habit: self.delete_habit(h['id'])
        )
        delete_btn.pack(side=tk.RIGHT, padx=2)
    
    def log_habit_completion(self, habit, var):
        """Log habit completion to API"""
        try:
            today = date.today().isoformat()
            
            payload = {
                "habit_id": habit['id'],
                "date": today,
                "completed": var.get(),
                "notes": ""
            }
            
            response = requests.post(f"{self.api_url}/logs", json=payload)
            
            if response.status_code == 201:
                self.status_label.config(text=f"Logged: {habit['name']}")
            else:
                messagebox.showerror("Error", "Failed to log habit")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error logging habit: {str(e)}")
    
    def add_habit_dialog(self):
        """Show dialog to add new habit"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Habit")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Name
        ttk.Label(dialog, text="Habit Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        desc_text = tk.Text(dialog, height=3, width=30)
        desc_text.grid(row=1, column=1, padx=10, pady=5)
        
        # Category
        ttk.Label(dialog, text="Category:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        category_var = ttk.Combobox(dialog, values=['fitness', 'health', 'learning', 'wellness', 'general'], width=27)
        category_var.grid(row=2, column=1, padx=10, pady=5)
        category_var.current(4)
        
        # Icon
        ttk.Label(dialog, text="Icon Emoji:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        icon_entry = ttk.Entry(dialog, width=30)
        icon_entry.insert(0, "🎯")
        icon_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Submit Button
        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Validation", "Please enter a habit name")
                return
            
            try:
                payload = {
                    "user_id": self.user_id,
                    "name": name,
                    "description": desc_text.get("1.0", tk.END),
                    "category": category_var.get(),
                    "icon": icon_entry.get()
                }
                
                response = requests.post(f"{self.api_url}/habits", json=payload)
                
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Habit added successfully!")
                    dialog.destroy()
                    self.load_habits()
                else:
                    messagebox.showerror("Error", "Failed to add habit")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error adding habit: {str(e)}")
        
        ttk.Button(dialog, text="Add Habit", command=submit).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_habit(self, habit_id):
        """Delete a habit"""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this habit?"):
            try:
                response = requests.delete(f"{self.api_url}/habits/{habit_id}")
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Habit deleted!")
                    self.load_habits()
                else:
                    messagebox.showerror("Error", "Failed to delete habit")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting habit: {str(e)}")
    
    def show_analytics(self):
        """Show analytics window"""
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Analytics & Insights")
        analytics_window.geometry("600x400")
        
        info_text = tk.Text(analytics_window, wrap=tk.WORD, padx=10, pady=10)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info_text.insert(tk.END, "📊 ANALYTICS & GROWTH INSIGHTS\n")
        info_text.insert(tk.END, "=" * 40 + "\n\n")
        
        for habit in self.habits:
            info_text.insert(tk.END, f"✓ {habit['name']}\n")
            info_text.insert(tk.END, f"  Category: {habit.get('category', 'N/A')}\n")
            info_text.insert(tk.END, f"  Created: {habit.get('created_at', 'N/A')}\n\n")
        
        info_text.config(state=tk.DISABLED)
    
    def show_calendar(self):
        """Show calendar view"""
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Calendar View")
        calendar_window.geometry("600x300")
        
        info_label = ttk.Label(calendar_window, text="📅 Calendar view coming soon!\nTrack daily completion across months.", justify=tk.CENTER)
        info_label.pack(pady=50)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HabitTrackerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
