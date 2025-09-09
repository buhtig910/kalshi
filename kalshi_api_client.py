#!/usr/bin/env python3
"""
Kalshi API Client for browsing categories and extracting data
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

class KalshiAPIClient:
    """Client for interacting with Kalshi API to browse categories and extract data"""
    
    def __init__(self, base_url: str = "https://api.elections.kalshi.com/trade-api/v2", 
                 demo: bool = False):
        """
        Initialize the Kalshi API client
        
        Args:
            base_url: Base URL for the API
            demo: If True, use demo environment
        """
        if demo:
            self.base_url = "https://demo-api.kalshi.co/trade-api/v2"
        else:
            self.base_url = base_url
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kalshi-Data-Extractor/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request to the API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
    
    def get_series_list(self, category: Optional[str] = None, 
                       limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get list of all series, optionally filtered by category
        
        Args:
            category: Filter by category (e.g., 'Economics', 'Politics', 'Sports')
            limit: Maximum number of series to return
            
        Returns:
            List of series data
        """
        params = {'limit': limit}
        if category:
            params['category'] = category
            
        response = self._make_request('series', params)
        return response.get('series', [])
    
    def get_categories(self) -> List[str]:
        """
        Get all available categories
        
        Returns:
            List of unique categories
        """
        series_list = self.get_series_list(limit=1000)
        categories = set()
        
        for series in series_list:
            if 'category' in series and series['category']:
                categories.add(series['category'])
        
        return sorted(list(categories))
    
    def get_series_details(self, series_ticker: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific series
        
        Args:
            series_ticker: The ticker symbol for the series
            
        Returns:
            Series details
        """
        return self._make_request(f'series/{series_ticker}')
    
    def get_markets(self, series_ticker: Optional[str] = None, 
                   status: str = 'open', limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get markets, optionally filtered by series
        
        Args:
            series_ticker: Filter by specific series
            status: Market status ('open', 'closed', 'all')
            limit: Maximum number of markets to return
            
        Returns:
            List of market data
        """
        params = {'status': status, 'limit': limit}
        if series_ticker:
            params['series_ticker'] = series_ticker
            
        response = self._make_request('markets', params)
        return response.get('markets', [])
    
    def get_market_orderbook(self, market_ticker: str) -> Dict[str, Any]:
        """
        Get order book for a specific market
        
        Args:
            market_ticker: The ticker symbol for the market
            
        Returns:
            Order book data
        """
        return self._make_request(f'markets/{market_ticker}/orderbook')
    
    def get_events(self, series_ticker: Optional[str] = None, 
                  limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get events, optionally filtered by series
        
        Args:
            series_ticker: Filter by specific series
            limit: Maximum number of events to return
            
        Returns:
            List of event data
        """
        params = {'limit': limit}
        if series_ticker:
            params['series_ticker'] = series_ticker
            
        response = self._make_request('events', params)
        return response.get('events', [])
    
    def browse_category_data(self, category: str, include_markets: bool = True) -> Dict[str, Any]:
        """
        Browse all data for a specific category
        
        Args:
            category: Category to browse
            include_markets: Whether to include market data
            
        Returns:
            Comprehensive data for the category
        """
        print(f"Browsing category: {category}")
        
        # Get series in this category
        series_list = self.get_series_list(category=category)
        print(f"Found {len(series_list)} series in {category}")
        
        category_data = {
            'category': category,
            'series_count': len(series_list),
            'series': [],
            'total_markets': 0,
            'markets': []
        }
        
        for series in series_list:
            series_ticker = series.get('ticker')
            series_title = series.get('title', 'Unknown')
            
            print(f"  Processing series: {series_ticker} - {series_title}")
            
            # Get detailed series info
            series_details = self.get_series_details(series_ticker)
            series_data = {
                'ticker': series_ticker,
                'title': series_title,
                'category': series.get('category'),
                'frequency': series.get('frequency'),
                'details': series_details.get('series', {}),
                'markets': []
            }
            
            if include_markets:
                # Get markets for this series
                markets = self.get_markets(series_ticker=series_ticker, status='open')
                series_data['markets'] = markets
                category_data['total_markets'] += len(markets)
                
                print(f"    Found {len(markets)} open markets")
            
            category_data['series'].append(series_data)
        
        return category_data
    
    def export_category_data(self, category: str, filename: Optional[str] = None) -> str:
        """
        Export category data to JSON file
        
        Args:
            category: Category to export
            filename: Output filename (auto-generated if None)
            
        Returns:
            Filename of exported data
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kalshi_{category.lower()}_{timestamp}.json"
        
        data = self.browse_category_data(category)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data exported to: {filename}")
        return filename
    
    def get_market_summary(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a summary of all markets, optionally filtered by category
        
        Args:
            category: Filter by category
            
        Returns:
            Market summary data
        """
        if category:
            series_list = self.get_series_list(category=category)
            series_tickers = [s['ticker'] for s in series_list]
            all_markets = []
            
            for ticker in series_tickers:
                markets = self.get_markets(series_ticker=ticker, status='open')
                all_markets.extend(markets)
        else:
            all_markets = self.get_markets(status='open', limit=1000)
        
        # Calculate summary statistics
        total_volume = sum(market.get('volume', 0) for market in all_markets)
        avg_yes_price = sum(market.get('yes_price', 0) for market in all_markets) / len(all_markets) if all_markets else 0
        
        return {
            'total_markets': len(all_markets),
            'total_volume': total_volume,
            'average_yes_price': round(avg_yes_price, 2),
            'markets': all_markets[:50]  # Include first 50 markets for details
        }


def main():
    """Example usage of the Kalshi API client"""
    print("Kalshi API Data Extractor")
    print("=" * 40)
    
    # Initialize client (use demo=True for testing)
    client = KalshiAPIClient(demo=False)
    
    # Get available categories
    print("\n1. Available Categories:")
    categories = client.get_categories()
    for i, category in enumerate(categories, 1):
        print(f"   {i}. {category}")
    
    # Browse a specific category (let's use the first one)
    if categories:
        selected_category = categories[0]
        print(f"\n2. Browsing category: {selected_category}")
        
        # Get category data
        category_data = client.browse_category_data(selected_category)
        
        print(f"\nCategory Summary:")
        print(f"  Series: {category_data['series_count']}")
        print(f"  Total Markets: {category_data['total_markets']}")
        
        # Show some example series
        print(f"\nExample Series:")
        for series in category_data['series'][:3]:
            print(f"  - {series['ticker']}: {series['title']}")
            if series['markets']:
                print(f"    Markets: {len(series['markets'])}")
        
        # Export data
        filename = client.export_category_data(selected_category)
        print(f"\nData exported to: {filename}")
    
    # Get market summary
    print(f"\n3. Market Summary:")
    summary = client.get_market_summary()
    print(f"  Total Markets: {summary['total_markets']}")
    print(f"  Total Volume: {summary['total_volume']}")
    print(f"  Average Yes Price: {summary['average_yes_price']}¢")


if __name__ == "__main__":
    main()
