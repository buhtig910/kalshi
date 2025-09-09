#!/usr/bin/env python3
"""
Simple runner script for Kalshi top volumes extraction
"""

from kalshi_top_volumes import KalshiTopVolumesExtractor
import sys

def main():
    """Run the Kalshi top volumes extraction"""
    
    print("🚀 Starting Kalshi Top Volumes Extraction...")
    print("Target: Top 5 markets by volume for each category")
    print("Categories: Politics, Sports, Crypto, World, Economics, Culture")
    print()
    
    # Check if user wants demo mode
    demo_mode = False
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'demo':
        demo_mode = True
        print("🔧 Running in DEMO mode")
        print()
    
    try:
        # Initialize extractor
        extractor = KalshiTopVolumesExtractor(demo=demo_mode)
        
        # Extract top volumes
        results = extractor.get_all_top_volumes(top_n=5)
        
        # Print summary
        extractor.print_summary_report(results)
        
        # Export data
        filename = extractor.export_top_volumes(results)
        
        print(f"\n✅ SUCCESS! Data extracted and saved to: {filename}")
        print("\nTo run in demo mode: python run_kalshi_extraction.py demo")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Extraction cancelled by user")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the Kalshi API is accessible")
        print("3. Try running in demo mode: python run_kalshi_extraction.py demo")

if __name__ == "__main__":
    main()
