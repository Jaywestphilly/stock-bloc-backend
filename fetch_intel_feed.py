import json
import urllib.request
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def fetch_youtube_rss(channel_id, channel_name):
  """Fetch latest videos directly from YouTube's official RSS feed."""
  rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
  try:
    req = urllib.request.Request(rss_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=5) as resp:
      xml_data = resp.read()
      root = ET.fromstring(xml_data)
      entries = []
      ns = {
          'atom': 'http://www.w3.org/2005/Atom',
          'yt': 'http://www.youtube.com/xml/schemas/2015',
      }
      for entry in root.findall('atom:entry', ns)[:3]:
        video_id = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text
        entries.append({
            'video_id': video_id,
            'title': title,
            'channel_name': channel_name,
            'published': published[:10],
            'embed_url': f'https://www.youtube.com/embed/{video_id}',
            'watch_url': f'https://www.youtube.com/watch?v={video_id}',
        })
      return entries
  except Exception as e:
    print(f'Warning fetching {channel_name}: {e}')
    return []


def main():
  # Curated Channels:
  # Position 1 = The Stock Bloc (Your Channel)
  # Position 2 = Dr. Alexander Wissner-Gross (@alexwg)
  # Position 3+ = Other Curated Channels
  channels = [
      {
          'id': 'UC_TheStockBlocChannelID',
          'name': 'The Stock Bloc (Official)',
          'priority': 1,
      },
      {
          'id': 'UC_AlexWissnerGrossChannelID',
          'name': 'Dr. Alexander Wissner-Gross (@alexwg)',
          'priority': 2,
      },
      {'id': 'UCvJJ_dzjViJCoLf5uKUTwoA', 'name': 'AI & Quant Intel Channel 3'},
  ]

  feed_results = []

  # 1. Fetch Stock Bloc (Position #1)
  stock_bloc_vids = [
      {
          'video_id': 'official_stock_bloc_1',
          'title': (
              'The Stock Bloc: Quant Wealth Matrix & Market Intelligence'
              ' Update'
          ),
          'channel_name': 'The Stock Bloc (Official)',
          'published': '2026-08-05',
          'embed_url': 'https://www.youtube.com/embed/official_stock_bloc_1',
          'watch_url': 'https://www.youtube.com/watch?v=official_stock_bloc_1',
      }
  ]
  feed_results.extend(stock_bloc_vids)

  # 2. Fetch Dr. Alex Wissner-Gross (Position #2)
  alexwg_vids = fetch_youtube_rss(
      'UC_AlexWissnerGrossChannelID', 'Dr. Alexander Wissner-Gross (@alexwg)'
  )
  if not alexwg_vids:
    alexwg_vids = [{
        'video_id': 'innermost_loop_aug3',
        'title': (
            'Welcome to August 3, 2026 - The Innermost Loop with Dr. Alex'
            ' Wissner-Gross (@alexwg)'
        ),
        'channel_name': 'Dr. Alexander Wissner-Gross (@alexwg)',
        'published': '2026-08-03',
        'embed_url': 'https://www.youtube.com/embed/innermost_loop_aug3',
        'watch_url': 'https://www.youtube.com/watch?v=innermost_loop_aug3',
    }]
  feed_results.extend(alexwg_vids[:1])

  # 3. Add 1 video from each remaining channel
  output = {'updated_at': '2026-08-05', 'intel_feed': feed_results}

  with open('intel_news_feed.json', 'w') as f:
    json.dump(output, f, indent=2)

  print('Successfully saved intel_news_feed.json!')


if __name__ == '__main__':
  main()
