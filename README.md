# 🎯 Kalshi Data Extractor

A comprehensive Python toolkit for extracting and analyzing market data from Kalshi prediction markets. Get the top 5 markets by volume for each category with lightning-fast performance.

## 🚀 Features

- **Multiple Extraction Methods**: Choose from standard, fast, or lightning-fast extraction
- **GUI Interface**: Easy-to-use graphical interface with tkinter
- **Category Analysis**: Focus on Politics, Sports, Crypto, World, Economics, and Culture
- **Volume-Based Ranking**: Get the highest volume markets for each category
- **Data Export**: Export results to JSON with timestamps
- **Real-time Progress**: Live updates during data extraction

## 📊 Categories Analyzed

- **Politics** - Political events and elections
- **Sports** - Sports predictions and championships  
- **Crypto** - Cryptocurrency price predictions
- **World** - International events and relations
- **Economics** - Economic indicators and Fed decisions
- **Culture** - Cultural events and trends

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/buhtig910/kalshi.git
   cd kalshi
   ```

2. **Install dependencies:**
   ```bash
   python setup.py
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### GUI Interface (Recommended for beginners)
```bash
python kalshi_gui.py
```
- Click "Extract Top Volumes" to get data
- View results in organized tabs
- Export data with one click

### Command Line Interface
```bash
# Standard extraction
python run_kalshi_extraction.py

# Lightning fast extraction
python kalshi_lightning_fast.py

# Demo mode
python run_kalshi_extraction.py demo
```

## 📁 File Structure

```
kalshi/
├── kalshi_gui.py              # GUI interface
├── run_kalshi_extraction.py   # Main command line script
├── kalshi_lightning_fast.py   # Fast extraction method
├── kalshi_api_client.py       # Core API client
├── kalshi_top_volumes.py      # Volume-based extraction
├── setup.py                   # Setup script
├── requirements.txt           # Python dependencies
├── CHANGELOG.md              # Project changelog
└── README.md                 # This file
```

## ⚡ Performance

- **Standard Method**: ~30-60 seconds (individual API calls)
- **Lightning Fast**: ~5-10 seconds (bulk API calls)
- **GUI Interface**: User-friendly with progress bars

## 📊 Sample Output

```
🎯 KALSHI TOP VOLUMES SUMMARY
==================================================

POLITICS:
  1. KXMAYORNYCPARTY-25-D
     Will a representative of the Democratic party win the NYC Mayor race in 2025?
     Volume: 7,994,131 | Yes Price: 0¢

  2. KXMAYORNYCPARTY-25-AC
     Will a representative of the Andrew Cuomo party win the NYC Mayor race in 2025?
     Volume: 5,474,945 | Yes Price: 0¢

ECONOMICS:
  1. KXFEDDECISION-25SEP-H0
     Will the Federal Reserve Hike rates by 0bps at their September 2025 meeting?
     Volume: 16,510,008 | Yes Price: 0¢

  2. KXFEDDECISION-25SEP-C26
     Will the Federal Reserve Cut rates by >25bps at their September 2025 meeting?
     Volume: 11,697,175 | Yes Price: 0¢
```

## 🔧 Configuration

### Demo Mode
For testing without affecting live data:
```python
extractor = KalshiExtractor(demo=True)
```

### API Limits
- Default limit: 10,000 markets per request
- Adjustable in the code for different needs

## 📈 Data Export

Results are automatically exported to JSON files with:
- Extraction timestamp
- Category breakdown
- Market details (ticker, title, volume, prices)
- Series information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the CHANGELOG.md for recent updates
2. Ensure all dependencies are installed
3. Try running in demo mode first
4. Check your internet connection

## 🔗 Links

- [Kalshi Official API Documentation](https://docs.kalshi.com/)
- [Kalshi Python Library](https://pypi.org/project/kalshi-py/)
- [GitHub Repository](https://github.com/buhtig910/kalshi)

---

**Happy Trading! 📈**
