#!/usr/bin/env python3
"""
Kalshi Data Viewer - Beautiful GUI for viewing Kalshi market data
Displays top volume markets in an attractive, easy-to-read format
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class KalshiDataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Kalshi Market Data Viewer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.current_data = {}
        self.setup_ui()
        self.load_latest_data()
    
    def setup_ui(self):
        """Set up the beautiful user interface"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎯 Kalshi Market Data Viewer", 
                              font=("Arial", 24, "bold"), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="Top 5 Markets by Volume - Live Data", 
                                 font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg='#ecf0f1')
        btn_frame.pack(pady=15)
        
        self.refresh_btn = tk.Button(btn_frame, text="🔄 Refresh Data", 
                                    command=self.refresh_data, 
                                    font=("Arial", 12, "bold"),
                                    bg='#3498db', fg='white', 
                                    relief=tk.RAISED, bd=3,
                                    padx=20, pady=10)
        self.refresh_btn.pack(side=tk.LEFT, padx=10)
        
        self.load_btn = tk.Button(btn_frame, text="📁 Load File", 
                                 command=self.load_data_file, 
                                 font=("Arial", 12, "bold"),
                                 bg='#9b59b6', fg='white', 
                                 relief=tk.RAISED, bd=3,
                                 padx=20, pady=10)
        self.load_btn.pack(side=tk.LEFT, padx=10)
        
        self.export_btn = tk.Button(btn_frame, text="💾 Export", 
                                   command=self.export_data, 
                                   font=("Arial", 12, "bold"),
                                   bg='#27ae60', fg='white', 
                                   relief=tk.RAISED, bd=3,
                                   padx=20, pady=10)
        self.export_btn.pack(side=tk.LEFT, padx=10)
        
        self.prices_btn = tk.Button(btn_frame, text="💰 Get Live Prices", 
                                   command=self.get_live_prices, 
                                   font=("Arial", 12, "bold"),
                                   bg='#e67e22', fg='white', 
                                   relief=tk.RAISED, bd=3,
                                   padx=20, pady=10)
        self.prices_btn.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready to display data...", 
                                    font=("Arial", 10), bg='#ecf0f1', fg='#7f8c8d')
        self.status_label.pack(pady=(0, 10))
        
        # Main content area
        self.setup_content_area(main_frame)
    
    def setup_content_area(self, parent):
        """Set up the main content display area"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Style the notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Create tabs for each category
        self.category_tabs = {}
        categories = ['Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture']
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6']
        
        for i, category in enumerate(categories):
            tab_frame = tk.Frame(self.notebook, bg='#f8f9fa')
            self.notebook.add(tab_frame, text=f"🏛️ {category}" if category == 'Politics' else 
                             f"⚽ {category}" if category == 'Sports' else
                             f"💰 {category}" if category == 'Crypto' else
                             f"🌍 {category}" if category == 'World' else
                             f"📈 {category}" if category == 'Economics' else
                             f"🎭 {category}")
            
            # Create scrollable frame for this category
            canvas = tk.Canvas(tab_frame, bg='#f8f9fa')
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.category_tabs[category] = scrollable_frame
    
    def load_latest_data(self):
        """Load the most recent data file"""
        try:
            # Look for the most recent JSON file
            json_files = [f for f in os.listdir('.') if f.startswith('kalshi_top_volumes_') and f.endswith('.json')]
            if json_files:
                latest_file = max(json_files, key=os.path.getctime)
                self.load_data_from_file(latest_file)
                self.status_label.config(text=f"Loaded: {latest_file}")
            else:
                self.status_label.config(text="No data files found. Click 'Refresh Data' to fetch new data.")
        except Exception as e:
            self.status_label.config(text=f"Error loading data: {e}")
    
    def refresh_data(self):
        """Refresh data by running the extraction script"""
        self.status_label.config(text="Refreshing data... Please wait...")
        self.root.update()
        
        try:
            import subprocess
            result = subprocess.run(['python', 'run_kalshi_extraction.py'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.load_latest_data()
                self.status_label.config(text="Data refreshed successfully!")
                messagebox.showinfo("Success", "Data refreshed successfully!")
            else:
                self.status_label.config(text="Error refreshing data")
                messagebox.showerror("Error", f"Failed to refresh data: {result.stderr}")
        except Exception as e:
            self.status_label.config(text="Error refreshing data")
            messagebox.showerror("Error", f"Failed to refresh data: {e}")
    
    def load_data_file(self):
        """Load data from a selected file"""
        filename = filedialog.askopenfilename(
            title="Select Kalshi Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.load_data_from_file(filename)
    
    def load_data_from_file(self, filename):
        """Load data from a specific file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract the data section
            if 'data' in data:
                self.current_data = data['data']
            else:
                self.current_data = data
            
            self.display_data()
            self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def display_data(self):
        """Display the loaded data in the interface"""
        if not self.current_data:
            return
        
        # Clear existing content
        for tab in self.category_tabs.values():
            for widget in tab.winfo_children():
                widget.destroy()
        
        # Display data for each category
        for category, markets in self.current_data.items():
            if category not in self.category_tabs:
                continue
                
            tab = self.category_tabs[category]
            
            if not markets:
                # No data message
                no_data_label = tk.Label(tab, text=f"No data available for {category}", 
                                       font=("Arial", 16), fg='#7f8c8d', bg='#f8f9fa')
                no_data_label.pack(pady=50)
                continue
            
            # Category header
            header_frame = tk.Frame(tab, bg='#2c3e50', relief=tk.RAISED, bd=2)
            header_frame.pack(fill=tk.X, pady=(10, 20), padx=20)
            
            category_label = tk.Label(header_frame, text=f"{category.upper()} MARKETS", 
                                    font=("Arial", 18, "bold"), fg='white', bg='#2c3e50')
            category_label.pack(pady=10)
            
            # Calculate totals
            total_volume = sum(market.get('volume', 0) for market in markets)
            avg_yes_price = sum(market.get('yes_price', 0) for market in markets) / len(markets)
            avg_yes_display = f"${avg_yes_price/100:.2f}" if avg_yes_price > 0 else "N/A"
            
            stats_label = tk.Label(header_frame, 
                                 text=f"Total Volume: {total_volume:,} | Markets: {len(markets)} | Avg Yes Price: {avg_yes_display}", 
                                 font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
            stats_label.pack(pady=(0, 10))
            
            # Display each market
            for i, market in enumerate(markets, 1):
                self.create_market_card(tab, market, i)
    
    def create_market_card(self, parent, market, rank):
        """Create a beautiful card for each market"""
        
        # Card frame
        card_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, pady=5, padx=20)
        
        # Rank and ticker
        header_frame = tk.Frame(card_frame, bg='#34495e')
        header_frame.pack(fill=tk.X)
        
        rank_label = tk.Label(header_frame, text=f"#{rank}", 
                             font=("Arial", 14, "bold"), fg='white', bg='#34495e')
        rank_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        ticker_label = tk.Label(header_frame, text=market.get('ticker', 'N/A'), 
                               font=("Arial", 14, "bold"), fg='white', bg='#34495e')
        ticker_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        volume_label = tk.Label(header_frame, text=f"Volume: {market.get('volume', 0):,}", 
                               font=("Arial", 12, "bold"), fg='#2ecc71', bg='#34495e')
        volume_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Market details
        details_frame = tk.Frame(card_frame, bg='white')
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_text = market.get('title', 'Unknown')
        if len(title_text) > 80:
            title_text = title_text[:77] + "..."
        
        title_label = tk.Label(details_frame, text=title_text, 
                              font=("Arial", 11), fg='#2c3e50', bg='white', wraplength=800)
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Series info
        series_text = f"Series: {market.get('series_title', 'Unknown')}"
        series_label = tk.Label(details_frame, text=series_text, 
                               font=("Arial", 10), fg='#7f8c8d', bg='white')
        series_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Price info
        price_frame = tk.Frame(details_frame, bg='white')
        price_frame.pack(fill=tk.X)
        
        yes_price = market.get('yes_price', 0)
        no_price = market.get('no_price', 0)
        
        # Format prices properly
        yes_display = f"${yes_price/100:.2f}" if yes_price > 0 else "N/A"
        no_display = f"${no_price/100:.2f}" if no_price > 0 else "N/A"
        
        yes_label = tk.Label(price_frame, text=f"YES: {yes_display}", 
                            font=("Arial", 11, "bold"), fg='#27ae60', bg='white')
        yes_label.pack(side=tk.LEFT)
        
        no_label = tk.Label(price_frame, text=f"NO: {no_display}", 
                           font=("Arial", 11, "bold"), fg='#e74c3c', bg='white')
        no_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Add Kalshi link button
        link_btn = tk.Button(price_frame, text="🔗 View on Kalshi", 
                            command=lambda: self.open_kalshi_link(market.get('ticker', '')),
                            font=("Arial", 9), fg='#3498db', bg='white', 
                            relief=tk.FLAT, cursor='hand2')
        link_btn.pack(side=tk.RIGHT)
    
    def open_kalshi_link(self, ticker):
        """Open the Kalshi website for a specific market"""
        if not ticker:
            messagebox.showwarning("Warning", "No ticker available for this market")
            return
        
        import webbrowser
        kalshi_url = f"https://kalshi.com/markets/{ticker}"
        webbrowser.open(kalshi_url)
    
    def get_live_prices(self):
        """Get live prices for all markets"""
        self.status_label.config(text="Getting live prices... Please wait...")
        self.root.update()
        
        try:
            # Run the extraction to get fresh data with live prices
            import subprocess
            result = subprocess.run(['python', 'run_kalshi_extraction.py'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.load_latest_data()
                self.status_label.config(text="Live prices updated successfully!")
                messagebox.showinfo("Success", "Live prices updated successfully!")
            else:
                self.status_label.config(text="Error getting live prices")
                messagebox.showerror("Error", f"Failed to get live prices: {result.stderr}")
        except Exception as e:
            self.status_label.config(text="Error getting live prices")
            messagebox.showerror("Error", f"Failed to get live prices: {e}")
    
    def export_data(self):
        """Export current view to a file"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Data View",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("🎯 KALSHI MARKET DATA VIEWER\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    for category, markets in self.current_data.items():
                        f.write(f"{category.upper()} MARKETS\n")
                        f.write("-" * 30 + "\n")
                        
                        if not markets:
                            f.write("No data available\n\n")
                            continue
                        
                        total_volume = sum(market.get('volume', 0) for market in markets)
                        f.write(f"Total Volume: {total_volume:,}\n")
                        f.write(f"Markets: {len(markets)}\n\n")
                        
                        for i, market in enumerate(markets, 1):
                            f.write(f"{i}. {market.get('ticker', 'N/A')}\n")
                            f.write(f"   {market.get('title', 'Unknown')}\n")
                            f.write(f"   Series: {market.get('series_title', 'Unknown')}\n")
                            f.write(f"   Volume: {market.get('volume', 0):,}\n")
                            
                            yes_price = market.get('yes_price', 0)
                            no_price = market.get('no_price', 0)
                            yes_display = f"${yes_price/100:.2f}" if yes_price > 0 else "N/A"
                            no_display = f"${no_price/100:.2f}" if no_price > 0 else "N/A"
                            
                            f.write(f"   YES: {yes_display} | NO: {no_display}\n")
                            f.write(f"   Kalshi Link: https://kalshi.com/markets/{market.get('ticker', 'N/A')}\n\n")
                        
                        f.write("\n")
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

def main():
    """Main function to run the data viewer"""
    root = tk.Tk()
    app = KalshiDataViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
