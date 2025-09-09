#!/usr/bin/env python3
"""
Kalshi Detailed Extractor - Gets specific market options and outcomes
Shows actual betting options like Yes/No answers or specific price ranges
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import time

class KalshiDetailedExtractor:
    """Extract detailed market data with specific options and outcomes"""
    
    def __init__(self, demo: bool = False):
        self.base_url = "https://demo-api.kalshi.co/trade-api/v2" if demo else "https://api.elections.kalshi.com/trade-api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kalshi-Detailed-Extractor/1.0'
        })
        self.target_categories = ['Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture']
    
    def get_market_details(self, market_ticker: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific market including options
        
        Args:
            market_ticker: The ticker symbol for the market
            
        Returns:
            Detailed market information with options
        """
        try:
            # Get market details
            market_response = self.session.get(f"{self.base_url}/markets/{market_ticker}")
            market_response.raise_for_status()
            market_data = market_response.json()
            
            # Get order book for pricing
            orderbook_response = self.session.get(f"{self.base_url}/markets/{market_ticker}/orderbook")
            orderbook_data = orderbook_response.json() if orderbook_response.status_code == 200 else {}
            
            return {
                'market': market_data.get('market', {}),
                'orderbook': orderbook_data.get('orderbook', {})
            }
            
        except Exception as e:
            print(f"   ❌ Error getting details for {market_ticker}: {e}")
            return {}
    
    def extract_detailed_data(self, top_n: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract detailed market data with specific options
        
        Args:
            top_n: Number of top markets per category
            
        Returns:
            Dictionary with detailed market data by category
        """
        print("🔍 Kalshi Detailed Market Extractor")
        print("=" * 50)
        print(f"Target Categories: {', '.join(self.target_categories)}")
        print(f"Top {top_n} markets per category with detailed options")
        print()
        
        start_time = time.time()
        
        # Step 1: Get all markets and series
        print("📡 Fetching markets and series...")
        try:
            markets_response = self.session.get(f"{self.base_url}/markets", params={
                'status': 'open',
                'limit': 10000
            })
            markets_response.raise_for_status()
            markets_data = markets_response.json()
            all_markets = markets_data.get('markets', [])
            
            series_response = self.session.get(f"{self.base_url}/series", params={
                'limit': 10000
            })
            series_response.raise_for_status()
            series_data = series_response.json()
            all_series = series_data.get('series', [])
            
            print(f"   📊 Retrieved {len(all_markets)} markets and {len(all_series)} series")
            
        except Exception as e:
            print(f"   ❌ Error fetching data: {e}")
            return {}
        
        # Step 2: Create series mapping
        series_map = {s['ticker']: s for s in all_series}
        
        # Step 3: Process each category with detailed options
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
            
            # Get detailed information for each top market
            detailed_markets = []
            for i, market in enumerate(top_markets, 1):
                print(f"   🔍 Getting details for market {i}/{len(top_markets)}: {market.get('ticker', 'N/A')}")
                
                details = self.get_market_details(market.get('ticker', ''))
                if details:
                    # Combine basic market info with detailed options
                    detailed_market = {**market, **details}
                    detailed_markets.append(detailed_market)
                    
                    # Display the options
                    self.display_market_options(detailed_market, i)
                else:
                    detailed_markets.append(market)
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
            
            results[category] = detailed_markets
        
        end_time = time.time()
        print(f"\n⏱️  Total extraction time: {end_time - start_time:.2f} seconds")
        
        return results
    
    def display_market_options(self, market_data: Dict[str, Any], rank: int):
        """Display the specific options for a market"""
        market_info = market_data.get('market', {})
        orderbook = market_data.get('orderbook', {})
        
        ticker = market_info.get('ticker', 'N/A')
        title = market_info.get('title', 'Unknown')
        volume = market_data.get('volume', 0)
        
        print(f"      {rank}. {ticker} - {title}")
        print(f"         Volume: {volume:,}")
        
        # Display market type and options
        market_type = market_info.get('market_type', 'unknown')
        print(f"         Type: {market_type}")
        
        # Get Yes/No prices from orderbook
        yes_bids = orderbook.get('yes', [])
        no_bids = orderbook.get('no', [])
        
        if yes_bids and no_bids:
            yes_price = yes_bids[0][0] if yes_bids else 0
            no_price = no_bids[0][0] if no_bids else 0
            print(f"         YES: ${yes_price/100:.2f} | NO: ${no_price/100:.2f}")
        
        # Display specific options based on market type
        if market_type == 'binary':
            print(f"         Options: YES or NO")
        elif market_type == 'categorical':
            # For categorical markets, show the specific categories
            categories = market_info.get('categories', [])
            if categories:
                print(f"         Options: {', '.join([cat.get('name', 'Unknown') for cat in categories])}")
        elif market_type == 'scalar':
            # For scalar markets, show the range
            min_value = market_info.get('min_value')
            max_value = market_info.get('max_value')
            if min_value is not None and max_value is not None:
                print(f"         Range: {min_value} to {max_value}")
        
        print()
    
    def export_detailed_data(self, data: Dict[str, List[Dict[str, Any]]], 
                           filename: str = None) -> str:
        """Export detailed data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_detailed_{timestamp}.json"
        
        export_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'detailed_with_options',
            'categories_analyzed': list(data.keys()),
            'total_categories': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed data exported to: {filename}")
        return filename

def main():
    """Main function for detailed extraction"""
    print("🔍 Kalshi Detailed Market Extractor")
    print("Shows specific betting options and outcomes for each market!")
    print()
    
    # Initialize detailed extractor
    extractor = KalshiDetailedExtractor(demo=False)  # Set to True for demo
    
    try:
        # Extract detailed data
        results = extractor.extract_detailed_data(top_n=3)  # Start with 3 to avoid too many API calls
        
        # Export data
        filename = extractor.export_detailed_data(results)
        
        print(f"\n✅ Detailed extraction complete! Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during detailed extraction: {e}")

if __name__ == "__main__":
    main()
