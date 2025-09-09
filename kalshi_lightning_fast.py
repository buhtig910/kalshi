#!/usr/bin/env python3
"""
Lightning Fast Kalshi Data Extractor
Uses optimized API calls with correct parameters
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import time

class LightningFastKalshiExtractor:
    """Lightning fast extractor using optimized API calls"""
    
    def __init__(self, demo: bool = False):
        self.base_url = "https://demo-api.kalshi.co/trade-api/v2" if demo else "https://api.elections.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kalshi-Lightning-Fast/1.0'
        })
        self.target_categories = ['Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture']
    
    def get_all_data_lightning_fast(self) -> tuple[List[Dict], List[Dict]]:
        """
        Get all markets and series data using optimized queries
        
        Returns:
            Tuple of (markets, series) data
        """
        print("⚡ Lightning Fast Data Fetching...")
        start_time = time.time()
        
        try:
            # Get markets with optimized parameters
            print("📡 Fetching markets...")
            markets_response = self.session.get(f"{self.base_url}/markets", params={
                'status': 'open',
                'limit': 10000  # Reasonable limit
            })
            markets_response.raise_for_status()
            markets_data = markets_response.json()
            markets = markets_data.get('markets', [])
            print(f"   📊 Retrieved {len(markets)} markets")
            
            # Get series with optimized parameters
            print("📡 Fetching series...")
            series_response = self.session.get(f"{self.base_url}/series", params={
                'limit': 10000  # Reasonable limit
            })
            series_response.raise_for_status()
            series_data = series_response.json()
            series = series_data.get('series', [])
            print(f"   📊 Retrieved {len(series)} series")
            
            fetch_time = time.time() - start_time
            print(f"   ⚡ Total fetch time: {fetch_time:.2f} seconds")
            
            return markets, series
            
        except Exception as e:
            print(f"   ❌ Error fetching data: {e}")
            return [], []
    
    def extract_lightning_fast(self, top_n: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lightning fast extraction using optimized bulk queries
        
        Args:
            top_n: Number of top markets per category
            
        Returns:
            Dictionary with top markets by category
        """
        print("⚡⚡⚡⚡ Kalshi Lightning Fast Extractor")
        print("=" * 50)
        print(f"Target Categories: {', '.join(self.target_categories)}")
        print(f"Top {top_n} markets per category by volume")
        print()
        
        total_start = time.time()
        
        # Step 1: Get all data
        all_markets, all_series = self.get_all_data_lightning_fast()
        
        if not all_markets or not all_series:
            print("❌ Failed to fetch data")
            return {}
        
        # Step 2: Create fast lookup maps
        print("🔗 Creating lookup maps...")
        series_map = {s['ticker']: s for s in all_series}
        
        # Step 3: Process each category lightning fast
        print("⚡ Processing categories...")
        results = {}
        
        for category in self.target_categories:
            print(f"\n{'='*20} {category.upper()} {'='*20}")
            
            # Filter markets for this category
            category_markets = []
            for market in all_markets:
                series_ticker = market.get('series_ticker')
                if series_ticker in series_map:
                    series_info = series_map[series_ticker]
                    if series_info.get('category') == category:
                        # Add series info to market
                        market['series_title'] = series_info.get('title', 'Unknown')
                        market['category'] = category
                        category_markets.append(market)
            
            print(f"   📈 Found {len(category_markets)} markets in {category}")
            
            if not category_markets:
                print(f"   ⚠️  No markets found for {category}")
                results[category] = []
                continue
            
            # Sort by volume and get top N
            sorted_markets = sorted(category_markets, key=lambda x: x.get('volume', 0), reverse=True)
            top_markets = sorted_markets[:top_n]
            
            print(f"   🏆 Top {len(top_markets)} markets by volume:")
            for i, market in enumerate(top_markets, 1):
                volume = market.get('volume', 0)
                yes_price = market.get('yes_price', 0)
                ticker = market.get('ticker', 'N/A')
                title = market.get('title', 'Unknown')
                # Truncate long titles
                if len(title) > 60:
                    title = title[:57] + "..."
                print(f"      {i}. {ticker}")
                print(f"         {title}")
                print(f"         Vol: {volume:,} - Yes: {yes_price}¢")
            
            if top_markets:
                total_volume = sum(market.get('volume', 0) for market in top_markets)
                avg_yes_price = sum(market.get('yes_price', 0) for market in top_markets) / len(top_markets)
                print(f"   📊 Total Volume: {total_volume:,}")
                print(f"   📊 Average Yes Price: {avg_yes_price:.1f}¢")
            
            results[category] = top_markets
        
        total_time = time.time() - total_start
        print(f"\n⏱️  Total extraction time: {total_time:.2f} seconds")
        
        return results
    
    def export_results(self, data: Dict[str, List[Dict[str, Any]]], 
                      filename: str = None) -> str:
        """Export results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_lightning_fast_{timestamp}.json"
        
        export_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'lightning_fast_optimized',
            'categories_analyzed': list(data.keys()),
            'total_categories': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Data exported to: {filename}")
        return filename

def main():
    """Main function for lightning fast extraction"""
    print("⚡⚡⚡⚡ Kalshi Lightning Fast Data Extractor")
    print("Using optimized API calls for maximum speed!")
    print()
    
    # Initialize lightning fast extractor
    extractor = LightningFastKalshiExtractor(demo=False)  # Set to True for demo
    
    try:
        # Extract data using lightning fast method
        results = extractor.extract_lightning_fast(top_n=5)
        
        # Export data
        filename = extractor.export_results(results)
        
        print(f"\n✅ Lightning fast extraction complete! Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during lightning fast extraction: {e}")

if __name__ == "__main__":
    main()
