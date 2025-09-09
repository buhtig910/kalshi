#!/usr/bin/env python3
"""
Kalshi Data Viewer - Simple GUI for viewing Kalshi market data
Uses tkinter (built into Python) - no additional packages needed!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
from datetime import datetime
from kalshi_top_volumes import KalshiTopVolumesExtractor

class KalshiDataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalshi Data Viewer")
        self.root.geometry("1000x700")
        
        # Data storage
        self.current_data = {}
        self.is_extracting = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎯 Kalshi Market Data Viewer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Extract button
        self.extract_btn = ttk.Button(control_frame, text="🚀 Extract Top Volumes", 
                                     command=self.start_extraction)
        self.extract_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Load data button
        self.load_btn = ttk.Button(control_frame, text="📁 Load Data File", 
                                  command=self.load_data_file)
        self.load_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Export button
        self.export_btn = ttk.Button(control_frame, text="💾 Export Data", 
                                    command=self.export_data, state="disabled")
        self.export_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Demo mode checkbox
        self.demo_var = tk.BooleanVar()
        self.demo_check = ttk.Checkbutton(control_frame, text="Demo Mode", 
                                         variable=self.demo_var)
        self.demo_check.grid(row=0, column=3, padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready to extract data...")
        self.status_label.grid(row=2, column=0, columnspan=4, pady=(5, 0))
        
        # Main content area with notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Summary tab
        self.setup_summary_tab()
        
        # Categories tab
        self.setup_categories_tab()
        
        # Raw data tab
        self.setup_raw_data_tab()
    
    def setup_summary_tab(self):
        """Set up the summary tab"""
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="📊 Summary")
        
        # Summary text area
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=20, width=80)
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)
    
    def setup_categories_tab(self):
        """Set up the categories tab with treeview"""
        categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(categories_frame, text="📋 Categories")
        
        # Treeview for categories
        columns = ('Category', 'Markets', 'Total Volume', 'Avg Yes Price')
        self.tree = ttk.Treeview(categories_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('Category', text='Category')
        self.tree.heading('Markets', text='Markets')
        self.tree.heading('Total Volume', text='Total Volume')
        self.tree.heading('Avg Yes Price', text='Avg Yes Price')
        
        self.tree.column('Category', width=120)
        self.tree.column('Markets', width=80)
        self.tree.column('Total Volume', width=120)
        self.tree.column('Avg Yes Price', width=100)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(categories_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=10)
        
        # Configure grid
        categories_frame.columnconfigure(0, weight=1)
        categories_frame.rowconfigure(0, weight=1)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_category_double_click)
    
    def setup_raw_data_tab(self):
        """Set up the raw data tab"""
        raw_frame = ttk.Frame(self.notebook)
        self.notebook.add(raw_frame, text="🔍 Raw Data")
        
        # Raw data text area
        self.raw_text = scrolledtext.ScrolledText(raw_frame, height=20, width=80)
        self.raw_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid
        raw_frame.columnconfigure(0, weight=1)
        raw_frame.rowconfigure(0, weight=1)
    
    def start_extraction(self):
        """Start data extraction in a separate thread"""
        if self.is_extracting:
            messagebox.showwarning("Warning", "Extraction already in progress!")
            return
        
        self.is_extracting = True
        self.extract_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Extracting data... Please wait...")
        
        # Run extraction in separate thread
        thread = threading.Thread(target=self.extract_data_thread)
        thread.daemon = True
        thread.start()
    
    def extract_data_thread(self):
        """Extract data in background thread"""
        try:
            demo_mode = self.demo_var.get()
            extractor = KalshiTopVolumesExtractor(demo=demo_mode)
            self.current_data = extractor.get_all_top_volumes(top_n=5)
            
            # Update UI in main thread
            self.root.after(0, self.extraction_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.extraction_error(str(e)))
    
    def extraction_complete(self):
        """Called when extraction is complete"""
        self.is_extracting = False
        self.extract_btn.config(state="normal")
        self.export_btn.config(state="normal")
        self.progress.stop()
        self.status_label.config(text="Extraction complete!")
        
        # Update all tabs with new data
        self.update_summary_tab()
        self.update_categories_tab()
        self.update_raw_data_tab()
        
        messagebox.showinfo("Success", "Data extraction completed successfully!")
    
    def extraction_error(self, error_msg):
        """Called when extraction fails"""
        self.is_extracting = False
        self.extract_btn.config(state="normal")
        self.progress.stop()
        self.status_label.config(text="Extraction failed!")
        
        messagebox.showerror("Error", f"Extraction failed: {error_msg}")
    
    def load_data_file(self):
        """Load data from JSON file"""
        filename = filedialog.askopenfilename(
            title="Select Kalshi Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract the data section
                if 'data' in data:
                    self.current_data = data['data']
                else:
                    self.current_data = data
                
                # Update UI
                self.update_summary_tab()
                self.update_categories_tab()
                self.update_raw_data_tab()
                self.export_btn.config(state="normal")
                
                self.status_label.config(text=f"Loaded data from {filename}")
                messagebox.showinfo("Success", "Data loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def export_data(self):
        """Export current data to file"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Kalshi Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                export_data = {
                    'extraction_timestamp': datetime.now().isoformat(),
                    'categories_analyzed': list(self.current_data.keys()),
                    'total_categories': len(self.current_data),
                    'data': self.current_data
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def update_summary_tab(self):
        """Update the summary tab with current data"""
        self.summary_text.delete(1.0, tk.END)
        
        if not self.current_data:
            self.summary_text.insert(tk.END, "No data available. Click 'Extract Top Volumes' to get data.")
            return
        
        # Generate summary
        summary = self.generate_summary()
        self.summary_text.insert(tk.END, summary)
    
    def update_categories_tab(self):
        """Update the categories tab with current data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.current_data:
            return
        
        # Add data to treeview
        for category, markets in self.current_data.items():
            if not markets:
                continue
            
            total_volume = sum(market.get('volume', 0) for market in markets)
            avg_yes_price = sum(market.get('yes_price', 0) for market in markets) / len(markets)
            
            self.tree.insert('', 'end', values=(
                category,
                len(markets),
                f"{total_volume:,}",
                f"{avg_yes_price:.1f}¢"
            ))
    
    def update_raw_data_tab(self):
        """Update the raw data tab with current data"""
        self.raw_text.delete(1.0, tk.END)
        
        if not self.current_data:
            self.raw_text.insert(tk.END, "No data available.")
            return
        
        # Format raw data as JSON
        formatted_data = json.dumps(self.current_data, indent=2, ensure_ascii=False)
        self.raw_text.insert(tk.END, formatted_data)
    
    def generate_summary(self):
        """Generate a text summary of the data"""
        if not self.current_data:
            return "No data available."
        
        summary = []
        summary.append("🎯 KALSHI TOP VOLUMES SUMMARY")
        summary.append("=" * 50)
        summary.append("")
        
        total_markets = 0
        total_volume = 0
        
        for category, markets in self.current_data.items():
            if not markets:
                summary.append(f"❌ {category.upper()}: No data available")
                continue
            
            category_volume = sum(market.get('volume', 0) for market in markets)
            avg_yes_price = sum(market.get('yes_price', 0) for market in markets) / len(markets)
            
            total_markets += len(markets)
            total_volume += category_volume
            
            summary.append(f"📊 {category.upper()}:")
            summary.append(f"   Markets: {len(markets)}")
            summary.append(f"   Total Volume: {category_volume:,}")
            summary.append(f"   Average Yes Price: {avg_yes_price:.1f}¢")
            summary.append("")
            
            # Top markets
            summary.append("   🏆 Top Markets:")
            for i, market in enumerate(markets, 1):
                ticker = market.get('ticker', 'N/A')
                title = market.get('title', 'Unknown')[:50] + "..." if len(market.get('title', '')) > 50 else market.get('title', 'Unknown')
                volume = market.get('volume', 0)
                yes_price = market.get('yes_price', 0)
                
                summary.append(f"      {i}. {ticker} - {title}")
                summary.append(f"         Volume: {volume:,} | Yes: {yes_price}¢")
            summary.append("")
        
        # Overall statistics
        summary.append("=" * 50)
        summary.append("📈 OVERALL STATISTICS:")
        summary.append(f"   Total Markets: {total_markets}")
        summary.append(f"   Total Volume: {total_volume:,}")
        summary.append(f"   Average Volume per Market: {total_volume // total_markets if total_markets > 0 else 0:,}")
        summary.append("=" * 50)
        
        return "\n".join(summary)
    
    def on_category_double_click(self, event):
        """Handle double-click on category row"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        category = item['values'][0]
        
        # Show detailed view for this category
        self.show_category_details(category)
    
    def show_category_details(self, category):
        """Show detailed view for a specific category"""
        if category not in self.current_data:
            return
        
        markets = self.current_data[category]
        if not markets:
            messagebox.showinfo("Category Details", f"No data available for {category}")
            return
        
        # Create new window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Category Details - {category}")
        detail_window.geometry("800x600")
        
        # Create text widget
        text_widget = scrolledtext.ScrolledText(detail_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generate detailed text
        details = []
        details.append(f"📊 {category.upper()} - DETAILED VIEW")
        details.append("=" * 60)
        details.append("")
        
        total_volume = sum(market.get('volume', 0) for market in markets)
        avg_yes_price = sum(market.get('yes_price', 0) for market in markets) / len(markets)
        
        details.append(f"Total Markets: {len(markets)}")
        details.append(f"Total Volume: {total_volume:,}")
        details.append(f"Average Yes Price: {avg_yes_price:.1f}¢")
        details.append("")
        
        for i, market in enumerate(markets, 1):
            details.append(f"{i}. {market.get('ticker', 'N/A')} - {market.get('title', 'Unknown')}")
            details.append(f"   Series: {market.get('series_title', 'Unknown')}")
            details.append(f"   Volume: {market.get('volume', 0):,}")
            details.append(f"   Yes Price: {market.get('yes_price', 0)}¢")
            details.append(f"   No Price: {market.get('no_price', 0)}¢")
            details.append("")

        text_widget.insert(tk.END, "\n".join(details))
        text_widget.config(state=tk.DISABLED)

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = KalshiDataViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
