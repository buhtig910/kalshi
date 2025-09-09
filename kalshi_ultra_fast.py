#!/usr/bin/env python3
"""
Ultra Fast Kalshi Data Extractor
Uses the official kalshi-py library with optimized queries
"""

from kalshi_py import Client
from kalshi_py.api.market import get_markets, get_series_list
import json
from datetime import datetime
from typing import Dict, List, Any
import time

class UltraFastKalshiExtractor:
    """Ultra fast extractor using official kalshi-py library"""
    
    def __init__(self, demo: bool = False):
        self.demo = demo
        self.base_url = "https://demo-api.kalshi.co/trade-api/v2" if demo else "https://api.elections.kalshi.com/trade-api/v2"
        self.client = Client(base_url=self.base_url)
        self.target_categories = ['Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture']
    
    def extract_ultra_fast(self, top_n: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Ultra fast extraction using optimized kalshi-py calls
        
        Args:
            top_n: Number of top markets per category
            
        Returns:
            Dictionary with top markets by category
        """
        print("⚡ Ultra Fast Kalshi Extractor")
        print("=" * 50)
        print(f"Target Categories: {', '.join(self.target_categories)}")
        print(f"Top {top_n} markets per category by volume")
        print()
        
        start_time = time.time()
        
        # Step 1: Get all markets in one call
        print("📡 Fetching all markets...")
        try:
            markets_response = get_markets.sync(client=self.client, status='open', limit=10000)
            all_markets = markets_response.markets if hasattr(markets_response, 'markets') else []
            print(f"   📊 Retrieved {len(all_markets)} markets")
        except Exception as e:
            print(f"   ❌ Error fetching markets: {e}")
            return {}
        
        # Step 2: Get all series in one call
        print("📡 Fetching all series...")
        try:
            series_response = get_series_list.sync(client=self.client, limit=10000)
            all_series = series_response.series if hasattr(series_response, 'series') else []
            print(f"   📊 Retrieved {len(all_series)} series")
        except Exception as e:
            print(f"   ❌ Error fetching series: {e}")
            return {}
        
        # Step 3: Create category mapping
        print("🔗 Creating category mapping...")
        series_to_category = {}
        for series in all_series:
            if hasattr(series, 'ticker') and hasattr(series, 'category'):
                series_to_category[series.ticker] = series.category
        
        # Step 4: Process categories
        print("⚡ Processing categories...")
        results = {}
        
        for category in self.target_categories:
            print(f"\n{'='*20} {category.upper()} {'='*20}")
            
            # Filter markets by category
            category_markets = []
            for market in all_markets:
                if hasattr(market, 'series_ticker'):
                    series_ticker = market.series_ticker
                    if series_ticker in series_to_category and series_to_category[series_ticker] == category:
                        # Convert to dict for easier handling
                        market_dict = {
                            'ticker': getattr(market, 'ticker', 'N/A'),
                            'title': getattr(market, 'title', 'Unknown'),
                            'volume': getattr(market, 'volume', 0),
                            'yes_price': getattr(market, 'yes_price', 0),
                            'no_price': getattr(market, 'no_price', 0),
                            'series_ticker': series_ticker,
                            'category': category
                        }
                        category_markets.append(market_dict)
            
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
                print(f"      {i}. {market.get('ticker', 'N/A')} - Vol: {volume:,} - Yes: {yes_price}¢")
            
            if top_markets:
                total_volume = sum(market.get('volume', 0) for market in top_markets)
                avg_yes_price = sum(market.get('yes_price', 0) for market in top_markets) / len(top_markets)
                print(f"   📊 Total Volume: {total_volume:,}")
                print(f"   📊 Average Yes Price: {avg_yes_price:.1f}¢")
            
            results[category] = top_markets
        
        end_time = time.time()
        print(f"\n⏱️  Total extraction time: {end_time - start_time:.2f} seconds")
        
        return results
    
    def export_results(self, data: Dict[str, List[Dict[str, Any]]], 
                      filename: str = None) -> str:
        """Export results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_ultra_fast_{timestamp}.json"
        
        export_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'ultra_fast_kalshi_py',
            'categories_analyzed': list(data.keys()),
            'total_categories': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Data exported to: {filename}")
        return filename

def main():
    """Main function for ultra fast extraction"""
    print("⚡⚡ Kalshi Ultra Fast Data Extractor")
    print("Using official kalshi-py library with optimized queries!")
    print()
    
    # Initialize ultra fast extractor
    extractor = UltraFastKalshiExtractor(demo=False)  # Set to True for demo
    
    try:
        # Extract data using ultra fast method
        results = extractor.extract_ultra_fast(top_n=5)
        
        # Export data
        filename = extractor.export_results(results)
        
        print(f"\n✅ Ultra fast extraction complete! Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during ultra fast extraction: {e}")

if __name__ == "__main__":
    main()
