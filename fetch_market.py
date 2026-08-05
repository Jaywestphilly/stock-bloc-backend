import json
import yfinance as yf


def fetch_watchlist_data():
  tickers = [
      # Top Pinned #1 Spot
      'SPCX',
      # Magnificent 7
      'NVDA',
      'AAPL',
      'MSFT',
      'GOOGL',
      'AMZN',
      'META',
      'TSLA',
      # Photonics Tech
      'POET',  # POET Technologies
      'LWLG',  # Lightwave Logic (LWG)
      # Quantum Computing
      'IONQ',  # IonQ
      'RGTI',  # Rigetti Computing
      'QUBT',  # Quantum Computing Inc.
      'QBTS',  # D-Wave Quantum
      # AI Infrastructure & Energy (Aschenbrenner Picks)
      'APLD',  # Applied Digital
      'CORZ',  # Core Scientific
      'IREN',  # Iris Energy
      'CLSK',  # CleanSpark
      'RIOT',  # Riot Platforms
      'CIFR',  # Cipher Mining
      'BTDR',  # Bitdeer Technologies
      'HUT',  # Hut 8 Mining
      'BITF',  # Bitfarms
      'VST',  # Vistra Corp (Nuclear Power)
      'OKLO',  # Oklo Inc.
      'BE',  # Bloom Energy
      'CEG',  # Constellation Energy
      'PLTR',  # Palantir
      'SMH',  # VanEck Semiconductor ETF
      # Crypto Anchors
      'BTC-USD',
      'ETH-USD',
  ]

  watchlist_results = []

  print('Fetching complete market watchlist data...')
  for symbol in tickers:
    try:
      ticker = yf.Ticker(symbol)
      info = ticker.fast_info

      # Fetch 7-day price history for mini sparkline charts
      history = ticker.history(period='7d')
      sparkline_prices = [
          round(p, 2) for p in history['Close'].tolist() if not round(p, 2) == 0
      ]

      current_price = round(info['lastPrice'], 2)
      previous_close = round(info['previousClose'], 2)
      price_change = round(
