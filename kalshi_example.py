#!/usr/bin/env python3
"""
Example script demonstrating Kalshi API usage for data extraction
"""

from kalshi_api_client import KalshiAPIClient
import json

def explore_kalshi_categories():
    """Explore available Kalshi categories and extract sample data"""
    
    print("🔍 Kalshi Category Explorer")
    print("=" * 50)
    
    # Initialize the client
    client = KalshiAPIClient(demo=False)  # Set to True for demo environment
    
    # 1. Get all available categories
    print("\n📋 Available Categories:")
    categories = client.get_categories()
    
    for i, category in enumerate(categories, 1):
        print(f"   {i:2d}. {category}")
    
    if not categories:
        print("   No categories found. Check your API connection.")
        return
    
    # 2. Let user select a category to explore
    print(f"\n🎯 Select a category to explore (1-{len(categories)}):")
    try:
        choice = int(input("Enter choice: ")) - 1
        if 0 <= choice < len(categories):
            selected_category = categories[choice]
        else:
            selected_category = categories[0]  # Default to first category
    except (ValueError, KeyboardInterrupt):
        selected_category = categories[0]  # Default to first category
    
    print(f"\n📊 Exploring category: {selected_category}")
    
    # 3. Get detailed data for the selected category
    category_data = client.browse_category_data(selected_category)
    
    # 4. Display summary
    print(f"\n📈 Category Summary:")
    print(f"   Series Count: {category_data['series_count']}")
    print(f"   Total Markets: {category_data['total_markets']}")
    
    # 5. Show detailed series information
    print(f"\n📚 Series Details:")
    for i, series in enumerate(category_data['series'][:5], 1):  # Show first 5 series
        print(f"\n   {i}. {series['ticker']} - {series['title']}")
        print(f"      Category: {series.get('category', 'N/A')}")
        print(f"      Frequency: {series.get('frequency', 'N/A')}")
        print(f"      Markets: {len(series['markets'])}")
        
        # Show sample markets
        if series['markets']:
            print(f"      Sample Markets:")
            for market in series['markets'][:3]:  # Show first 3 markets
                yes_price = market.get('yes_price', 0)
                volume = market.get('volume', 0)
                print(f"        • {market.get('ticker', 'N/A')}: {market.get('title', 'N/A')}")
                print(f"          Yes Price: {yes_price}¢ | Volume: {volume}")
    
    # 6. Export data
    print(f"\n💾 Exporting data...")
    filename = client.export_category_data(selected_category)
    print(f"   Data saved to: {filename}")
    
    # 7. Get overall market summary
    print(f"\n🌐 Overall Market Summary:")
    summary = client.get_market_summary()
    print(f"   Total Markets: {summary['total_markets']}")
    print(f"   Total Volume: {summary['total_volume']:,}")
    print(f"   Average Yes Price: {summary['average_yes_price']}¢")
    
    return category_data

def quick_category_browse(category_name: str):
    """Quickly browse a specific category"""
    
    client = KalshiAPIClient(demo=False)
    
    print(f"🚀 Quick Browse: {category_name}")
    print("=" * 40)
    
    # Get series in the category
    series_list = client.get_series_list(category=category_name)
    
    if not series_list:
        print(f"No series found for category: {category_name}")
        return
    
    print(f"Found {len(series_list)} series in {category_name}")
    
    for series in series_list[:10]:  # Show first 10 series
        print(f"\n📊 {series['ticker']} - {series['title']}")
        print(f"   Frequency: {series.get('frequency', 'N/A')}")
        
        # Get markets for this series
        markets = client.get_markets(series_ticker=series['ticker'], status='open')
        print(f"   Open Markets: {len(markets)}")
        
        if markets:
            # Show top market by volume
            top_market = max(markets, key=lambda m: m.get('volume', 0))
            print(f"   Top Market: {top_market['ticker']} (Vol: {top_market.get('volume', 0)})")

def main():
    """Main function with menu options"""
    
    print("🎯 Kalshi Data Extractor")
    print("=" * 30)
    print("1. Explore all categories")
    print("2. Quick browse specific category")
    print("3. Get market summary")
    print("4. Exit")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            explore_kalshi_categories()
        elif choice == "2":
            category = input("Enter category name: ").strip()
            quick_category_browse(category)
        elif choice == "3":
            client = KalshiAPIClient(demo=False)
            summary = client.get_market_summary()
            print(f"\n📊 Market Summary:")
            print(f"   Total Markets: {summary['total_markets']}")
            print(f"   Total Volume: {summary['total_volume']:,}")
            print(f"   Average Yes Price: {summary['average_yes_price']}¢")
        elif choice == "4":
            print("Goodbye!")
        else:
            print("Invalid choice. Please run again.")
            
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
