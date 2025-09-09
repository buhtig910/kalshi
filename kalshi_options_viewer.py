#!/usr/bin/env python3
"""
Kalshi Options Viewer - Shows specific betting options and outcomes
Enhanced GUI that displays actual market options like Yes/No or specific ranges
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Any

class KalshiOptionsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Kalshi Options Viewer - Market Betting Options")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # API setup
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kalshi-Options-Viewer/1.0'
        })
        
        # Data storage
        self.current_data = {}
        self.market_details = {}
        
        self.setup_ui()
        self.load_sample_data()
    
    def setup_ui(self):
        """Set up the enhanced user interface"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎯 Kalshi Options Viewer", 
                              font=("Arial", 24, "bold"), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="View Specific Betting Options & Outcomes", 
                                 font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg='#ecf0f1')
        btn_frame.pack(pady=15)
        
        self.load_btn = tk.Button(btn_frame, text="📁 Load Data", 
                                 command=self.load_data_file, 
                                 font=("Arial", 12, "bold"),
                                 bg='#9b59b6', fg='white', 
                                 relief=tk.RAISED, bd=3,
                                 padx=20, pady=10)
        self.load_btn.pack(side=tk.LEFT, padx=10)
        
        self.fetch_btn = tk.Button(btn_frame, text="🔍 Fetch Options", 
                                  command=self.fetch_market_options, 
                                  font=("Arial", 12, "bold"),
                                  bg='#e67e22', fg='white', 
                                  relief=tk.RAISED, bd=3,
                                  padx=20, pady=10)
        self.fetch_btn.pack(side=tk.LEFT, padx=10)
        
        self.export_btn = tk.Button(btn_frame, text="💾 Export", 
                                   command=self.export_data, 
                                   font=("Arial", 12, "bold"),
                                   bg='#27ae60', fg='white', 
                                   relief=tk.RAISED, bd=3,
                                   padx=20, pady=10)
        self.export_btn.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready to view market options...", 
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
        
        for category in categories:
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
    
    def load_sample_data(self):
        """Load sample data to demonstrate the interface"""
        try:
            # Look for the most recent JSON file
            json_files = [f for f in os.listdir('.') if f.startswith('kalshi_top_volumes_') and f.endswith('.json')]
            if json_files:
                latest_file = max(json_files, key=os.path.getctime)
                self.load_data_from_file(latest_file)
                self.status_label.config(text=f"Loaded: {latest_file}")
            else:
                self.status_label.config(text="No data files found. Load a data file to get started.")
        except Exception as e:
            self.status_label.config(text=f"Error loading data: {e}")
    
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
    
    def fetch_market_options(self):
        """Fetch detailed options for the current markets"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data loaded. Please load a data file first.")
            return
        
        self.status_label.config(text="Fetching market options... Please wait...")
        self.root.update()
        
        try:
            # Get detailed options for top markets
            detailed_data = {}
            
            for category, markets in self.current_data.items():
                if not markets:
                    detailed_data[category] = []
                    continue
                
                print(f"Fetching options for {category}...")
                detailed_markets = []
                
                # Get details for top 3 markets in each category
                for market in markets[:3]:
                    ticker = market.get('ticker')
                    if ticker:
                        details = self.get_market_details(ticker)
                        if details:
                            detailed_market = {**market, **details}
                            detailed_markets.append(detailed_market)
                        else:
                            detailed_markets.append(market)
                
                detailed_data[category] = detailed_markets
            
            self.current_data = detailed_data
            self.display_data()
            self.status_label.config(text="Market options fetched successfully!")
            messagebox.showinfo("Success", "Market options fetched successfully!")
            
        except Exception as e:
            self.status_label.config(text="Error fetching options")
            messagebox.showerror("Error", f"Failed to fetch market options: {e}")
    
    def get_market_details(self, ticker):
        """Get detailed market information including options"""
        try:
            # Get market details
            market_response = self.session.get(f"{self.base_url}/markets/{ticker}")
            if market_response.status_code == 200:
                market_data = market_response.json()
                return {'market_details': market_data.get('market', {})}
            else:
                print(f"   ⚠️  Could not fetch details for {ticker}")
                return {}
        except Exception as e:
            print(f"   ❌ Error fetching details for {ticker}: {e}")
            return {}
    
    def display_data(self):
        """Display the loaded data with options"""
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
            
            stats_label = tk.Label(header_frame, 
                                 text=f"Total Volume: {total_volume:,} | Markets: {len(markets)}", 
                                 font=("Arial", 12), fg='#bdc3c7', bg='#2c3e50')
            stats_label.pack(pady=(0, 10))
            
            # Display each market with options
            for i, market in enumerate(markets, 1):
                self.create_market_card_with_options(tab, market, i)
    
    def create_market_card_with_options(self, parent, market, rank):
        """Create a detailed card showing market options"""
        
        # Card frame
        card_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, pady=5, padx=20)
        
        # Header with rank and ticker
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
        if len(title_text) > 100:
            title_text = title_text[:97] + "..."
        
        title_label = tk.Label(details_frame, text=title_text, 
                              font=("Arial", 12, "bold"), fg='#2c3e50', bg='white', wraplength=1000)
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Series info
        series_text = f"Series: {market.get('series_title', 'Unknown')}"
        series_label = tk.Label(details_frame, text=series_text, 
                               font=("Arial", 10), fg='#7f8c8d', bg='white')
        series_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Market options section
        options_frame = tk.Frame(details_frame, bg='#f8f9fa', relief=tk.SUNKEN, bd=1)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        options_title = tk.Label(options_frame, text="🎯 BETTING OPTIONS", 
                                font=("Arial", 11, "bold"), fg='#2c3e50', bg='#f8f9fa')
        options_title.pack(pady=(10, 5))
        
        # Get market details if available
        market_details = market.get('market_details', {})
        
        if market_details:
            # Display specific options based on market type
            market_type = market_details.get('market_type', 'unknown')
            
            if market_type == 'binary':
                # Yes/No market
                self.display_binary_options(options_frame, market, market_details)
            elif market_type == 'categorical':
                # Multiple choice market
                self.display_categorical_options(options_frame, market, market_details)
            elif market_type == 'scalar':
                # Range market
                self.display_scalar_options(options_frame, market, market_details)
            else:
                # Unknown type - show basic info
                self.display_basic_options(options_frame, market)
        else:
            # No detailed info - show basic options
            self.display_basic_options(options_frame, market)
        
        # Price and link info
        price_frame = tk.Frame(details_frame, bg='white')
        price_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Get the actual bid/ask prices from the detailed data
        yes_bid = market.get('yes_bid', 0)
        yes_ask = market.get('yes_ask', 0)
        no_bid = market.get('no_bid', 0)
        no_ask = market.get('no_ask', 0)
        last_price = market.get('last_price', 0)
        
        # Convert cents to dollars (prices are in usd_cent format)
        yes_bid_display = f"${yes_bid/100:.2f}" if yes_bid > 0 else "N/A"
        yes_ask_display = f"${yes_ask/100:.2f}" if yes_ask > 0 else "N/A"
        no_bid_display = f"${no_bid/100:.2f}" if no_bid > 0 else "N/A"
        no_ask_display = f"${no_ask/100:.2f}" if no_ask > 0 else "N/A"
        last_display = f"${last_price/100:.2f}" if last_price > 0 else "N/A"
        
        # Create a more detailed price display
        price_details_frame = tk.Frame(price_frame, bg='white')
        price_details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # YES prices
        yes_frame = tk.Frame(price_details_frame, bg='white')
        yes_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        yes_title = tk.Label(yes_frame, text="YES:", font=("Arial", 10, "bold"), fg='#27ae60', bg='white')
        yes_title.pack()
        
        yes_prices = tk.Label(yes_frame, text=f"Bid: {yes_bid_display} | Ask: {yes_ask_display}", 
                             font=("Arial", 9), fg='#27ae60', bg='white')
        yes_prices.pack()
        
        # NO prices
        no_frame = tk.Frame(price_details_frame, bg='white')
        no_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        no_title = tk.Label(no_frame, text="NO:", font=("Arial", 10, "bold"), fg='#e74c3c', bg='white')
        no_title.pack()
        
        no_prices = tk.Label(no_frame, text=f"Bid: {no_bid_display} | Ask: {no_ask_display}", 
                            font=("Arial", 9), fg='#e74c3c', bg='white')
        no_prices.pack()
        
        # Last price
        if last_price > 0:
            last_frame = tk.Frame(price_details_frame, bg='white')
            last_frame.pack(side=tk.LEFT, padx=(0, 20))
            
            last_title = tk.Label(last_frame, text="Last:", font=("Arial", 10, "bold"), fg='#3498db', bg='white')
            last_title.pack()
            
            last_price_label = tk.Label(last_frame, text=last_display, 
                                       font=("Arial", 9), fg='#3498db', bg='white')
            last_price_label.pack()
        
        # Kalshi link button
        link_btn = tk.Button(price_frame, text="🔗 View on Kalshi", 
                            command=lambda: self.open_kalshi_link(market.get('ticker', '')),
                            font=("Arial", 9), fg='#3498db', bg='white', 
                            relief=tk.FLAT, cursor='hand2')
        link_btn.pack(side=tk.RIGHT)
    
    def display_binary_options(self, parent, market, market_details):
        """Display options for binary (Yes/No) markets"""
        options_text = "This is a YES/NO market. You can bet on either outcome:"
        options_label = tk.Label(parent, text=options_text, 
                                font=("Arial", 10), fg='#2c3e50', bg='#f8f9fa')
        options_label.pack(pady=5)
        
        # Yes/No options
        options_frame = tk.Frame(parent, bg='#f8f9fa')
        options_frame.pack(pady=5)
        
        yes_option = tk.Label(options_frame, text="✅ YES - The event will happen", 
                             font=("Arial", 10, "bold"), fg='#27ae60', bg='#f8f9fa')
        yes_option.pack(side=tk.LEFT, padx=10)
        
        no_option = tk.Label(options_frame, text="❌ NO - The event will not happen", 
                            font=("Arial", 10, "bold"), fg='#e74c3c', bg='#f8f9fa')
        no_option.pack(side=tk.LEFT, padx=10)
    
    def display_categorical_options(self, parent, market, market_details):
        """Display options for categorical markets"""
        categories = market_details.get('categories', [])
        
        if categories:
            options_text = "Choose from these specific options:"
            options_label = tk.Label(parent, text=options_text, 
                                    font=("Arial", 10), fg='#2c3e50', bg='#f8f9fa')
            options_label.pack(pady=5)
            
            for i, category in enumerate(categories, 1):
                cat_name = category.get('name', f'Option {i}')
                cat_label = tk.Label(parent, text=f"{i}. {cat_name}", 
                                    font=("Arial", 10), fg='#2c3e50', bg='#f8f9fa')
                cat_label.pack(anchor=tk.W, padx=20, pady=2)
        else:
            self.display_basic_options(parent, market)
    
    def display_scalar_options(self, parent, market, market_details):
        """Display options for scalar (range) markets"""
        min_val = market_details.get('min_value')
        max_val = market_details.get('max_value')
        
        if min_val is not None and max_val is not None:
            options_text = f"Bet on a specific value within this range:"
            options_label = tk.Label(parent, text=options_text, 
                                    font=("Arial", 10), fg='#2c3e50', bg='#f8f9fa')
            options_label.pack(pady=5)
            
            range_text = f"Range: {min_val} to {max_val}"
            range_label = tk.Label(parent, text=range_text, 
                                  font=("Arial", 10, "bold"), fg='#e67e22', bg='#f8f9fa')
            range_label.pack(pady=5)
        else:
            self.display_basic_options(parent, market)
    
    def display_basic_options(self, parent, market):
        """Display basic options when detailed info is not available"""
        options_text = "Basic YES/NO market - detailed options not available"
        options_label = tk.Label(parent, text=options_text, 
                                font=("Arial", 10), fg='#7f8c8d', bg='#f8f9fa')
        options_label.pack(pady=5)
    
    def open_kalshi_link(self, ticker):
        """Open the Kalshi website for a specific market"""
        if not ticker:
            messagebox.showwarning("Warning", "No ticker available for this market")
            return
        
        import webbrowser
        
        # Open the main Kalshi markets page
        webbrowser.open("https://kalshi.com/markets")
        
        # Show a message with the ticker for manual search
        messagebox.showinfo("Kalshi Market Search", 
                           f"Market Ticker: {ticker}\n\n"
                           f"1. The Kalshi markets page has been opened\n"
                           f"2. Search for: '{ticker}'\n"
                           f"3. Or look for the market title in the list\n\n"
                           f"Note: Some markets may be closed or restricted")
    
    def export_data(self):
        """Export current view to a file"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Options Data",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("🎯 KALSHI OPTIONS VIEWER\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    for category, markets in self.current_data.items():
                        f.write(f"{category.upper()} MARKETS\n")
                        f.write("-" * 30 + "\n")
                        
                        if not markets:
                            f.write("No data available\n\n")
                            continue
                        
                        for i, market in enumerate(markets, 1):
                            f.write(f"{i}. {market.get('ticker', 'N/A')}\n")
                            f.write(f"   {market.get('title', 'Unknown')}\n")
                            f.write(f"   Series: {market.get('series_title', 'Unknown')}\n")
                            f.write(f"   Volume: {market.get('volume', 0):,}\n")
                            
                            # Write options
                            market_details = market.get('market_details', {})
                            if market_details:
                                market_type = market_details.get('market_type', 'unknown')
                                f.write(f"   Market Type: {market_type}\n")
                                
                                if market_type == 'binary':
                                    f.write(f"   Options: YES or NO\n")
                                elif market_type == 'categorical':
                                    categories = market_details.get('categories', [])
                                    if categories:
                                        f.write(f"   Options: {', '.join([cat.get('name', 'Unknown') for cat in categories])}\n")
                                elif market_type == 'scalar':
                                    min_val = market_details.get('min_value')
                                    max_val = market_details.get('max_value')
                                    if min_val is not None and max_val is not None:
                                        f.write(f"   Range: {min_val} to {max_val}\n")
                            
                            f.write(f"   Search on Kalshi: https://kalshi.com/markets (search for '{market.get('ticker', 'N/A')}')\n\n")
                        
                        f.write("\n")
                
                messagebox.showinfo("Success", f"Options data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

def main():
    """Main function to run the options viewer"""
    root = tk.Tk()
    app = KalshiOptionsViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
