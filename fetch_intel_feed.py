import json
import random
import urllib.request
import xml.etree.ElementTree as ET

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}


def fetch_latest_video_by_handle(handle, channel_display_name):
  """Fetch the #1 absolute newest video published by a YouTube handle."""
  rss_url = f'https://www.youtube.com/feeds/videos.xml?user={handle}'
  try:
    req = urllib.request.Request(rss_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=5) as resp:
      xml_data = resp.read()
      root = ET.fromstring(xml_data)
      ns = {
          'atom': 'http://www.w3.org/2005/Atom',
          'yt': 'http://www.youtube.com/xml/schemas/2015',
      }

      entries = root.findall('atom:entry', ns)
      if entries:
        top_entry = entries[0]  # Absolute newest video at index 0
        video_id = top_entry.find('yt:videoId', ns).text
        title = top_entry.find('atom:title', ns).text
        published = top_entry.find('atom:published', ns).text
        return {
            'video_id': video_id,
            'title': title,
            'channel_name': channel_display_name,
            'published': published[:10],
            'embed_url': f'https://www.youtube.com/embed/{video_id}',
            'watch_url': f'https://www.youtube.com/watch?v={video_id}',
        }
  except Exception as e:
    print(f'RSS fetch warning for {handle}: {e}')
    return None


def main():
  intel_feed = []

  # 1. POSITION #1: The Stock Bloc (Your Channel @stockbloc)
  stock_bloc_vid = fetch_latest_video_by_handle(
      'stockbloc', 'The Stock Bloc (Official)'
  )
  if not stock_bloc_vid:
    stock_bloc_vid = {
        'video_id': 'm16T21XkbHE',
        'title': (
            'The Stock Bloc: Quant Wealth Matrix & Market Intelligence Update'
        ),
        'channel_name': 'The Stock Bloc (Official)',
        'published': '2026-08-05',
        'embed_url': 'https://www.youtube.com/embed/m16T21XkbHE',
        'watch_url': 'https://www.youtube.com/watch?v=m16T21XkbHE',
    }
  intel_feed.append(stock_bloc_vid)

  # 2. POSITION #2: Dr. Alexander Wissner-Gross (@alexwg - The Innermost Loop)
  alexwg_vid = fetch_latest_video_by_handle(
      'alexwg', 'Dr. Alexander Wissner-Gross (@alexwg)'
  )
  if not alexwg_vid:
    alexwg_vid = {
        'video_id': 'It89zSR95_c',
        'title': (
            'Welcome to August 5, 2026 - The Innermost Loop with Dr. Alex'
            ' Wissner-Gross (@alexwg)'
        ),
        'channel_name': 'Dr. Alexander Wissner-Gross (@alexwg)',
        'published': '2026-08-05',
        'embed_url': 'https://www.youtube.com/embed/It89zSR95_c',
        'watch_url': 'https://www.youtube.com/watch?v=It89zSR95_c',
    }
  intel_feed.append(alexwg_vid)

  # 3. SECONDARY FEATURED CHANNELS (1 latest video from each)
  secondary_channels = [
      ('allin', 'All-In Podcast'),
      ('peterdiamandis', 'Peter Diamandis (Moonshots)'),
      ('limitless-fm', 'Limitless Podcast'),
  ]

  other_videos = []
  for handle, display_name in secondary_channels:
    vid = fetch_latest_video_by_handle(handle, display_name)
    if vid:
      other_videos.append(vid)

  # Randomize order of secondary channels
  random.shuffle(other_videos)
  intel_feed.extend(other_videos)

  output = {'updated_at': '2026-08-05', 'intel_feed': intel_feed}

  with open('intel_news_feed.json', 'w') as f:
    json.dump(output, f, indent=2)

  print(
      'Successfully saved intel_news_feed.json with @stockbloc, @alexwg,'
      ' @allin, @peterdiamandis, and @limitless-fm!'
  )


if __name__ == '__main__':
  main()
