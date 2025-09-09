#!/usr/bin/env python3
"""
Kalshi Top Volumes Extractor
Gets the top 5 markets by volume for each specified category
"""

from kalshi_api_client import KalshiAPIClient
import json
from datetime import datetime
from typing import Dict, List, Any

class KalshiTopVolumesExtractor:
    """Extract top volume markets from specific Kalshi categories"""
    
    def __init__(self, demo: bool = False):
        self.client = KalshiAPIClient(demo=demo)
        self.target_categories = [
            'Politics', 'Sports', 'Crypto', 'World', 'Economics', 'Culture'
        ]
    
    def get_top_volumes_by_category(self, category: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get top N markets by volume for a specific category
        
        Args:
            category: Category name to search
            top_n: Number of top markets to return
            
        Returns:
            List of top markets sorted by volume (descending)
        """
        print(f"🔍 Searching {category} category...")
        
        # Get all series in this category
        series_list = self.client.get_series_list(category=category)
        
        if not series_list:
            print(f"   ⚠️  No series found for {category}")
            return []
        
        print(f"   📊 Found {len(series_list)} series in {category}")
        
        all_markets = []
        
        # Get markets for each series
        for series in series_list:
            series_ticker = series.get('ticker')
            markets = self.client.get_markets(series_ticker=series_ticker, status='open')
            
            # Add series info to each market
            for market in markets:
                market['series_title'] = series.get('title', 'Unknown')
                market['series_ticker'] = series_ticker
                market['category'] = category
            
            all_markets.extend(markets)
        
        print(f"   📈 Found {len(all_markets)} total markets")
        
        # Sort by volume (descending) and return top N
        sorted_markets = sorted(all_markets, key=lambda x: x.get('volume', 0), reverse=True)
        top_markets = sorted_markets[:top_n]
        
        print(f"   🏆 Top {len(top_markets)} markets by volume:")
        for i, market in enumerate(top_markets, 1):
            volume = market.get('volume', 0)
            yes_price = market.get('yes_price', 0)
            print(f"      {i}. {market.get('ticker', 'N/A')} - Vol: {volume:,} - Yes: {yes_price}¢")
        
        return top_markets
    
    def get_all_top_volumes(self, top_n: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get top N markets by volume for all target categories
        
        Args:
            top_n: Number of top markets to return per category
            
        Returns:
            Dictionary with category names as keys and top markets as values
        """
        print("🚀 Kalshi Top Volumes Extractor")
        print("=" * 50)
        print(f"Target Categories: {', '.join(self.target_categories)}")
        print(f"Top {top_n} markets per category by volume")
        print()
        
        all_results = {}
        
        for category in self.target_categories:
            print(f"\n{'='*20} {category.upper()} {'='*20}")
            top_markets = self.get_top_volumes_by_category(category, top_n)
            all_results[category] = top_markets
            
            if top_markets:
                total_volume = sum(market.get('volume', 0) for market in top_markets)
                avg_yes_price = sum(market.get('yes_price', 0) for market in top_markets) / len(top_markets)
                print(f"   📊 Total Volume: {total_volume:,}")
                print(f"   📊 Average Yes Price: {avg_yes_price:.1f}¢")
            else:
                print(f"   ❌ No data found for {category}")
        
        return all_results
    
    def export_top_volumes(self, data: Dict[str, List[Dict[str, Any]]], 
                          filename: str = None) -> str:
        """
        Export top volumes data to JSON file
        
        Args:
            data: Top volumes data by category
            filename: Output filename (auto-generated if None)
            
        Returns:
            Filename of exported data
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_top_volumes_{timestamp}.json"
        
        # Add metadata
        export_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'categories_analyzed': list(data.keys()),
            'total_categories': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Data exported to: {filename}")
        return filename
    
    def print_summary_report(self, data: Dict[str, List[Dict[str, Any]]]):
        """Print a summary report of all top volumes"""
        
        print("\n" + "="*60)
        print("📊 TOP VOLUMES SUMMARY REPORT")
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
                series_title = market.get('series_title', 'Unknown')
                
                print(f"  {i}. {ticker}")
                print(f"     Title: {title}")
                print(f"     Series: {series_title}")
                print(f"     Volume: {volume:,} | Yes Price: {yes_price}¢")
                print()
        
        print("="*60)
        print(f"📈 OVERALL STATISTICS:")
        print(f"   Total Markets Analyzed: {total_markets}")
        print(f"   Total Volume: {total_volume:,}")
        print(f"   Average Volume per Market: {total_volume // total_markets if total_markets > 0 else 0:,}")
        print("="*60)

def main():
    """Main function to run the top volumes extractor"""
    
    print("🎯 Kalshi Top Volumes Extractor")
    print("Categories: Politics, Sports, Crypto, World, Economics, Culture")
    print("Top 5 markets by volume per category")
    print()
    
    # Initialize extractor
    extractor = KalshiTopVolumesExtractor(demo=False)  # Set to True for demo
    
    try:
        # Get top volumes for all categories
        top_volumes_data = extractor.get_all_top_volumes(top_n=5)
        
        # Print summary report
        extractor.print_summary_report(top_volumes_data)
        
        # Export data
        filename = extractor.export_top_volumes(top_volumes_data)
        
        print(f"\n✅ Extraction complete! Data saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
