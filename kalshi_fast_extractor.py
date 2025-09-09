#!/usr/bin/env python3
"""
Fast Kalshi Data Extractor
Uses bulk API calls and parallel processing for much faster data extraction
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import concurrent.futures
from threading import Lock
import time

class FastKalshiExtractor:
    """Fast Kalshi data extractor using bulk API calls and parallel processing"""
    
    def __init__(self, demo: bool = False):
        self.base_url = "https://demo-api.kalshi.co/trade-api/v2" if demo else "https://api.elections.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kalshi-Fast-Extractor/1.0'
        })
        self.target_categories = ['Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture']
        self.lock = Lock()
        self.results = {}
    
    def get_all_markets_bulk(self, limit: int = 10000) -> List[Dict[str, Any]]:
        """
        Get all markets in one bulk call - much faster than individual series calls
        
        Args:
            limit: Maximum number of markets to retrieve
            
        Returns:
            List of all markets
        """
        print("🚀 Fetching all markets in bulk...")
        
        try:
            # Get all markets at once
            response = self.session.get(f"{self.base_url}/markets", params={
                'status': 'open',
                'limit': limit
            })
            response.raise_for_status()
            data = response.json()
            
            markets = data.get('markets', [])
            print(f"   📊 Retrieved {len(markets)} markets in one call")
            return markets
            
        except Exception as e:
            print(f"   ❌ Error fetching markets: {e}")
            return []
    
    def get_series_bulk(self, limit: int = 10000) -> List[Dict[str, Any]]:
        """
        Get all series in one bulk call
        
        Args:
            limit: Maximum number of series to retrieve
            
        Returns:
            List of all series
        """
        print("🚀 Fetching all series in bulk...")
        
        try:
            response = self.session.get(f"{self.base_url}/series", params={'limit': limit})
            response.raise_for_status()
            data = response.json()
            
            series = data.get('series', [])
            print(f"   📊 Retrieved {len(series)} series in one call")
            return series
            
        except Exception as e:
            print(f"   ❌ Error fetching series: {e}")
            return []
    
    def process_category_fast(self, category: str, all_markets: List[Dict], series_map: Dict) -> List[Dict[str, Any]]:
        """
        Process a single category using pre-fetched data
        
        Args:
            category: Category name
            all_markets: All markets data
            series_map: Series ticker to series data mapping
            
        Returns:
            Top 5 markets for the category
        """
        print(f"🔍 Processing {category} category...")
        
        # Filter markets by category using series data
        category_markets = []
        
        for market in all_markets:
            series_ticker = market.get('series_ticker')
            if series_ticker in series_map:
                series_data = series_map[series_ticker]
                if series_data.get('category') == category:
                    # Add series info to market
                    market['series_title'] = series_data.get('title', 'Unknown')
                    market['category'] = category
                    category_markets.append(market)
        
        print(f"   📈 Found {len(category_markets)} markets in {category}")
        
        if not category_markets:
            print(f"   ⚠️  No markets found for {category}")
            return []
        
        # Sort by volume and get top 5
        sorted_markets = sorted(category_markets, key=lambda x: x.get('volume', 0), reverse=True)
        top_markets = sorted_markets[:5]
        
        print(f"   🏆 Top 5 markets by volume:")
        for i, market in enumerate(top_markets, 1):
            volume = market.get('volume', 0)
            yes_price = market.get('yes_price', 0)
            print(f"      {i}. {market.get('ticker', 'N/A')} - Vol: {volume:,} - Yes: {yes_price}¢")
        
        return top_markets
    
    def extract_top_volumes_fast(self, top_n: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fast extraction of top volumes using bulk API calls
        
        Args:
            top_n: Number of top markets per category
            
        Returns:
            Dictionary with top markets by category
        """
        print("🚀 Fast Kalshi Top Volumes Extractor")
        print("=" * 50)
        print(f"Target Categories: {', '.join(self.target_categories)}")
        print(f"Top {top_n} markets per category by volume")
        print()
        
        start_time = time.time()
        
        # Step 1: Get all data in bulk
        print("📡 Step 1: Fetching all data in bulk...")
        all_markets = self.get_all_markets_bulk()
        all_series = self.get_series_bulk()
        
        if not all_markets or not all_series:
            print("❌ Failed to fetch data")
            return {}
        
        # Step 2: Create series mapping for fast lookup
        print("🔗 Step 2: Creating series mapping...")
        series_map = {series['ticker']: series for series in all_series}
        print(f"   📊 Mapped {len(series_map)} series")
        
        # Step 3: Process each category
        print("⚡ Step 3: Processing categories...")
        results = {}
        
        for category in self.target_categories:
            print(f"\n{'='*20} {category.upper()} {'='*20}")
            top_markets = self.process_category_fast(category, all_markets, series_map)
            results[category] = top_markets
            
            if top_markets:
                total_volume = sum(market.get('volume', 0) for market in top_markets)
                avg_yes_price = sum(market.get('yes_price', 0) for market in top_markets) / len(top_markets)
                print(f"   📊 Total Volume: {total_volume:,}")
                print(f"   📊 Average Yes Price: {avg_yes_price:.1f}¢")
            else:
                print(f"   ❌ No data found for {category}")
        
        end_time = time.time()
        print(f"\n⏱️  Total extraction time: {end_time - start_time:.2f} seconds")
        
        return results
    
    def export_fast_results(self, data: Dict[str, List[Dict[str, Any]]], 
                           filename: str = None) -> str:
        """Export results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_fast_top_volumes_{timestamp}.json"
        
        export_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'fast_bulk_api',
            'categories_analyzed': list(data.keys()),
            'total_categories': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Data exported to: {filename}")
        return filename
    
    def print_fast_summary(self, data: Dict[str, List[Dict[str, Any]]]):
        """Print summary of fast extraction results"""
        print("\n" + "="*60)
        print("📊 FAST EXTRACTION SUMMARY")
        print("="*60)
        
        total_markets = 0
        total_volume = 0
        
        for category, markets in data.items():
            if not markets:
                print(f"\n{category.upper()}: No data available")
                continue
                
            print(f"\n{category.upper()}:")
            print("-" * 40)
            
            category_volume = sum(market.get('volume', 0) for market in markets)
            total_volume += category_volume
            total_markets += len(markets)
            
            for i, market in enumerate(markets, 1):
                ticker = market.get('ticker', 'N/A')
                title = market.get('title', 'Unknown')
                volume = market.get('volume', 0)
                yes_price = market.get('yes_price', 0)
                
                print(f"  {i}. {ticker}")
                print(f"     {title}")
                print(f"     Volume: {volume:,} | Yes Price: {yes_price}¢")
                print()
        
        print("="*60)
        print(f"📈 OVERALL STATISTICS:")
        print(f"   Total Markets: {total_markets}")
        print(f"   Total Volume: {total_volume:,}")
        print(f"   Average Volume per Market: {total_volume // total_markets if total_markets > 0 else 0:,}")
        print("="*60)

def main():
    """Main function for fast extraction"""
    print("⚡ Kalshi Fast Data Extractor")
    print("Using bulk API calls for maximum speed!")
    print()
    
    # Initialize fast extractor
    extractor = FastKalshiExtractor(demo=False)  # Set to True for demo
    
    try:
        # Extract data using fast method
        results = extractor.extract_top_volumes_fast(top_n=5)
        
        # Print summary
        extractor.print_fast_summary(results)
        
        # Export data
        filename = extractor.export_fast_results(results)
        
        print(f"\n✅ Fast extraction complete! Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during fast extraction: {e}")

if __name__ == "__main__":
    main()
