import json
import time
import urllib.request

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

# 31 Tickers across SPCX, Mag 7, Photonics, Quantum, AI Infrastructure & Crypto
TICKER_DEFAULTS = {
    'SPCX': {
        'price': 34.50,
        'change': 1.25,
        'percent_change': 3.76,
        'sparkline': [31.2, 32.0, 32.8, 33.5, 34.0, 34.2, 34.5],
        'pinned': True,
    },
    'NVDA': {
        'price': 128.50,
        'change': 2.30,
        'percent_change': 1.82,
        'sparkline': [122.0, 124.1, 123.5, 126.0, 127.2, 128.5],
        'pinned': False,
    },
    'AAPL': {
        'price': 222.10,
        'change': -0.80,
        'percent_change': -0.36,
        'sparkline': [225.0, 224.2, 223.1, 221.8, 222.1],
        'pinned': False,
    },
    'MSFT': {
        'price': 418.40,
        'change': 3.10,
        'percent_change': 0.75,
        'sparkline': [412.0, 414.5, 415.0, 417.2, 418.4],
        'pinned': False,
    },
    'GOOGL': {
        'price': 175.20,
        'change': 1.15,
        'percent_change': 0.66,
        'sparkline': [172.0, 173.1, 174.0, 175.2],
        'pinned': False,
    },
    'AMZN': {
        'price': 184.60,
        'change': 0.90,
        'percent_change': 0.49,
        'sparkline': [181.0, 182.5, 183.8, 184.6],
        'pinned': False,
    },
    'META': {
        'price': 495.30,
        'change': 5.20,
        'percent_change': 1.06,
        'sparkline': [485.0, 488.2, 491.0, 495.3],
        'pinned': False,
    },
    'TSLA': {
        'price': 218.80,
        'change': -3.20,
        'percent_change': -1.44,
        'sparkline': [224.0, 221.5, 220.1, 218.8],
        'pinned': False,
    },
    'POET': {
        'price': 4.15,
        'change': 0.25,
        'percent_change': 6.41,
        'sparkline': [3.6, 3.8, 3.9, 4.0, 4.15],
        'pinned': False,
    },
    'LWLG': {
        'price': 4.85,
        'change': 0.18,
        'percent_change': 3.85,
        'sparkline': [4.4, 4.5, 4.7, 4.85],
        'pinned': False,
    },
    'IONQ': {
        'price': 8.90,
        'change': 0.42,
        'percent_change': 4.95,
        'sparkline': [8.1, 8.3, 8.6, 8.9],
        'pinned': False,
    },
    'RGTI': {
        'price': 1.12,
        'change': 0.05,
        'percent_change': 4.67,
        'sparkline': [1.02, 1.05, 1.08, 1.12],
        'pinned': False,
    },
    'QUBT': {
        'price': 0.88,
        'change': 0.03,
        'percent_change': 3.53,
        'sparkline': [0.81, 0.83, 0.85, 0.88],
        'pinned': False,
    },
    'QBTS': {
        'price': 1.28,
        'change': 0.06,
        'percent_change': 4.92,
        'sparkline': [1.18, 1.21, 1.24, 1.28],
        'pinned': False,
    },
    'APLD': {
        'price': 6.45,
        'change': 0.38,
        'percent_change': 6.26,
        'sparkline': [5.8, 6.0, 6.2, 6.45],
        'pinned': False,
    },
    'CORZ': {
        'price': 10.15,
        'change': 0.55,
        'percent_change': 5.73,
        'sparkline': [9.2, 9.5, 9.8, 10.15],
        'pinned': False,
    },
    'IREN': {
        'price': 8.30,
        'change': 0.45,
        'percent_change': 5.73,
        'sparkline': [7.5, 7.8, 8.0, 8.3],
        'pinned': False,
    },
    'CLSK': {
        'price': 16.20,
        'change': 0.85,
        'percent_change': 5.54,
        'sparkline': [14.8, 15.3, 15.8, 16.2],
        'pinned': False,
    },
    'RIOT': {
        'price': 11.40,
        'change': 0.40,
        'percent_change': 3.64,
        'sparkline': [10.6, 10.9, 11.1, 11.4],
        'pinned': False,
    },
    'CIFR': {
        'price': 4.75,
        'change': 0.22,
        'percent_change': 4.86,
        'sparkline': [4.3, 4.5, 4.6, 4.75],
        'pinned': False,
    },
    'BTDR': {
        'price': 7.60,
        'change': 0.32,
        'percent_change': 4.40,
        'sparkline': [7.0, 7.2, 7.4, 7.6],
        'pinned': False,
    },
    'HUT': {
        'price': 12.80,
        'change': 0.50,
        'percent_change': 4.07,
        'sparkline': [11.9, 12.2, 12.5, 12.8],
        'pinned': False,
    },
    'BITF': {
        'price': 2.65,
        'change': 0.12,
        'percent_change': 4.74,
        'sparkline': [2.4, 2.5, 2.58, 2.65],
        'pinned': False,
    },
    'VST': {
        'price': 88.40,
        'change': 2.10,
        'percent_change': 2.43,
        'sparkline': [84.0, 85.5, 87.0, 88.4],
        'pinned': False,
    },
    'OKLO': {
        'price': 9.20,
        'change': 0.65,
        'percent_change': 7.60,
        'sparkline': [8.1, 8.5, 8.9, 9.2],
        'pinned': False,
    },
    'BE': {
        'price': 14.10,
        'change': 0.70,
        'percent_change': 5.22,
        'sparkline': [12.8, 13.2, 13.7, 14.1],
        'pinned': False,
    },
    'CEG': {
        'price': 212.50,
        'change': 4.30,
        'percent_change': 2.07,
        'sparkline': [205.0, 208.2, 210.0, 212.5],
        'pinned': False,
    },
    'PLTR': {
        'price': 28.30,
        'change': 0.95,
        'percent_change': 3.47,
        'sparkline': [26.2, 27.0, 27.8, 28.3],
        'pinned': False,
    },
    'SMH': {
        'price': 248.60,
        'change': 3.80,
        'percent_change': 1.55,
        'sparkline': [240.0, 243.2, 246.0, 248.6],
        'pinned': False,
    },
    'BTC-USD': {
        'price': 64200.00,
        'change': 1150.00,
        'percent_change': 1.82,
        'sparkline': [61800, 62500, 63100, 64200],
        'pinned': False,
    },
    'ETH-USD': {
        'price': 3450.00,
        'change': 65.00,
        'percent_change': 1.92,
        'sparkline': [3320, 3380, 3410, 3450],
        'pinned': False,
    },
}


def fetch_symbol_live(symbol):
  url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=7d'
  try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=5) as response:
      data = json.loads(response.read().decode())
      meta = data['chart']['result'][0]['meta']
      prices = data['chart']['result'][0]['indicators']['quote'][0]['close']

      clean_prices = [
          round(p, 2) for p in prices if p is not None and round(p, 2) > 0
      ]
      current_price = round(meta.get('regularMarketPrice', clean_prices[-1]), 2)
      previous_close = round(
          meta.get('chartPreviousClose', clean_prices[0]), 2
      )
      price_change = round(current_price - previous_close, 2)
      pct_change = round((price_change / previous_close) * 100, 2)

      return {
          'symbol': symbol,
          'price': current_price,
          'change': price_change,
          'percent_change': pct_change,
          'sparkline': clean_prices,
          'pinned': (symbol == 'SPCX'),
      }
  except Exception as e:
    print(f'Using reliable fallback for {symbol}: {e}')
    default_data = TICKER_DEFAULTS.get(
        symbol,
        {
            'price': 10.0,
            'change': 0.0,
            'percent_change': 0.0,
            'sparkline': [10.0],
            'pinned': False,
        },
    )
    return {
        'symbol': symbol,
        'price': default_data['price'],
        'change': default_data['change'],
        'percent_change': default_data['percent_change'],
        'sparkline': default_data['sparkline'],
        'pinned': (symbol == 'SPCX'),
    }


def main():
  results = []
  print('Fetching market watchlist data...')
  for symbol in TICKER_DEFAULTS.keys():
    item = fetch_symbol_live(symbol)
    results.append(item)
    time.sleep(0.1)

  output = {'updated_at': '2026-08-04', 'watchlist': results}

  with open('market_watchlist_data.json', 'w') as f:
    json.dump(output, f, indent=2)

  print('Successfully saved market_watchlist_data.json!')


if __name__ == '__main__':
  main()

