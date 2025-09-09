#!/usr/bin/env python3
"""
Kalshi Debug Viewer - Shows raw data to understand price format
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class KalshiDebugViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Kalshi Debug Viewer - Raw Data Inspector")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.current_data = {}
        self.setup_ui()
        self.load_sample_data()
    
    def setup_ui(self):
        """Set up the debug interface"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#e74c3c', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🔍 Kalshi Debug Viewer", 
                              font=("Arial", 24, "bold"), fg='white', bg='#e74c3c')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="Raw Data Inspector - See What We're Actually Getting", 
                                 font=("Arial", 12), fg='#f8f9fa', bg='#e74c3c')
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
        
        self.analyze_btn = tk.Button(btn_frame, text="🔍 Analyze Prices", 
                                    command=self.analyze_prices, 
                                    font=("Arial", 12, "bold"),
                                    bg='#e67e22', fg='white', 
                                    relief=tk.RAISED, bd=3,
                                    padx=20, pady=10)
        self.analyze_btn.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Load data to see raw price information...", 
                                    font=("Arial", 10), bg='#ecf0f1', fg='#7f8c8d')
        self.status_label.pack(pady=(0, 10))
        
        # Main content area
        self.setup_content_area(main_frame)
    
    def setup_content_area(self, parent):
        """Set up the content display area"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Raw data tab
        raw_frame = tk.Frame(self.notebook, bg='#f8f9fa')
        self.notebook.add(raw_frame, text="📊 Raw Data")
        
        # Raw data text area
        self.raw_text = tk.Text(raw_frame, height=30, width=100, font=("Consolas", 10))
        raw_scrollbar = ttk.Scrollbar(raw_frame, orient="vertical", command=self.raw_text.yview)
        self.raw_text.configure(yscrollcommand=raw_scrollbar.set)
        
        self.raw_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        raw_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Price analysis tab
        price_frame = tk.Frame(self.notebook, bg='#f8f9fa')
        self.notebook.add(price_frame, text="💰 Price Analysis")
        
        # Price analysis text area
        self.price_text = tk.Text(price_frame, height=30, width=100, font=("Consolas", 10))
        price_scrollbar = ttk.Scrollbar(price_frame, orient="vertical", command=self.price_text.yview)
        self.price_text.configure(yscrollcommand=price_scrollbar.set)
        
        self.price_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        price_scrollbar.pack(side="right", fill="y", pady=10)
    
    def load_sample_data(self):
        """Load sample data"""
        try:
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
            
            if 'data' in data:
                self.current_data = data['data']
            else:
                self.current_data = data
            
            self.display_raw_data()
            self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def display_raw_data(self):
        """Display raw data in the text area"""
        self.raw_text.delete(1.0, tk.END)
        
        if not self.current_data:
            self.raw_text.insert(tk.END, "No data loaded.")
            return
        
        # Format and display raw data
        formatted_data = json.dumps(self.current_data, indent=2, ensure_ascii=False)
        self.raw_text.insert(tk.END, formatted_data)
    
    def analyze_prices(self):
        """Analyze price data to understand the format"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        
        self.price_text.delete(1.0, tk.END)
        
        analysis = []
        analysis.append("💰 PRICE ANALYSIS REPORT")
        analysis.append("=" * 50)
        analysis.append("")
        
        total_markets = 0
        markets_with_prices = 0
        price_examples = []
        
        for category, markets in self.current_data.items():
            if not markets:
                continue
            
            analysis.append(f"📊 {category.upper()}:")
            analysis.append("-" * 30)
            
            for market in markets:
                total_markets += 1
                
                ticker = market.get('ticker', 'N/A')
                yes_price = market.get('yes_price', 0)
                no_price = market.get('no_price', 0)
                volume = market.get('volume', 0)
                
                analysis.append(f"Market: {ticker}")
                analysis.append(f"  Raw YES price: {yes_price} (type: {type(yes_price).__name__})")
                analysis.append(f"  Raw NO price: {no_price} (type: {type(no_price).__name__})")
                analysis.append(f"  Volume: {volume}")
                
                if yes_price > 0 or no_price > 0:
                    markets_with_prices += 1
                    price_examples.append({
                        'ticker': ticker,
                        'yes': yes_price,
                        'no': no_price,
                        'volume': volume
                    })
                
                # Try different price interpretations
                if yes_price > 0:
                    analysis.append(f"  YES as cents: {yes_price}¢")
                    analysis.append(f"  YES as dollars: ${yes_price/100:.2f}")
                    analysis.append(f"  YES as decimal: {yes_price/100:.4f}")
                
                if no_price > 0:
                    analysis.append(f"  NO as cents: {no_price}¢")
                    analysis.append(f"  NO as dollars: ${no_price/100:.2f}")
                    analysis.append(f"  NO as decimal: {no_price/100:.4f}")
                
                analysis.append("")
        
        # Summary
        analysis.append("=" * 50)
        analysis.append("📈 SUMMARY:")
        analysis.append(f"  Total markets: {total_markets}")
        analysis.append(f"  Markets with prices: {markets_with_prices}")
        analysis.append(f"  Markets without prices: {total_markets - markets_with_prices}")
        analysis.append("")
        
        if price_examples:
            analysis.append("🎯 PRICE EXAMPLES:")
            for example in price_examples[:5]:  # Show first 5 examples
                analysis.append(f"  {example['ticker']}: YES={example['yes']}¢ (${example['yes']/100:.2f}), NO={example['no']}¢ (${example['no']/100:.2f})")
        
        analysis.append("")
        analysis.append("💡 INTERPRETATION:")
        analysis.append("  - Prices appear to be in cents (e.g., 45 = 45¢ = $0.45)")
        analysis.append("  - To convert to dollars: divide by 100")
        analysis.append("  - Many markets show 0 prices, which might mean:")
        analysis.append("    * Market is closed")
        analysis.append("    * No current trading activity")
        analysis.append("    * Data not available in this API response")
        
        self.price_text.insert(tk.END, "\n".join(analysis))

def main():
    """Main function to run the debug viewer"""
    root = tk.Tk()
    app = KalshiDebugViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
