import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import subprocess
import os

class SpyHuntGUI:
    def __init__(self, master):
        self.master = master
        master.title("SpyHunt GUI")
        
        # URL Input
        self.label = tk.Label(master, text="Enter URL:")
        self.label.pack()
        
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()
        
        # Execute Button
        self.execute_button = tk.Button(master, text="Fetch Title", command=self.fetch_title)
        self.execute_button.pack()
        
        # Additional Functionality Buttons
        self.scan_button = tk.Button(master, text="Run Scan", command=self.run_scan)
        self.scan_button.pack()
        
        self.clear_button = tk.Button(master, text="Clear Output", command=self.clear_output)
        self.clear_button.pack()
        
        # Output Text Box
        self.output_text = tk.Text(master, height=20, width=80)
        self.output_text.pack()

    def fetch_title(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            self.output_text.insert(tk.END, f"Title: {title}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

    def run_scan(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return
        
        # Example scan functionality (placeholder)
        try:
            # Here you can implement the actual scanning logic
            result = self.scan_function(url)  # Replace with actual scan function
            self.output_text.insert(tk.END, f"Scan Result: {result}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Scan Error: {str(e)}\n")

    def scan_function(self, url):
        # Placeholder for actual scanning logic
        # You can implement various functionalities similar to those in zwyck.py
        return f"Scanning {url}... (this is a placeholder result)"

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SpyHuntGUI(root)
    root.mainloop()