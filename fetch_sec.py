import json
import urllib.request

HEADERS = {'User-Agent': 'StockBloc/1.0 (contact@stock-bloc.com)'}


def fetch_sec_filings(cik):
  formatted_cik = str(cik).zfill(10)
  url = f'https://data.sec.gov/submissions/CIK{formatted_cik}.json'

  try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode())

    recent = data.get('filings', {}).get('recent', {})
    forms = recent.get('form', [])
    dates = recent.get('filingDate', [])
    accessions = recent.get('accessionNumber', [])
    descriptions = recent.get('primaryDocDescription', [])

    filings_list = []
    for i in range(min(20, len(forms))):
      form = forms[i]
      if form in ['13F-HR', '10-K', '10-Q']:
        accession_no_hyphen = accessions[i].replace('-', '')
        doc_url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_hyphen}/{accessions[i]}.txt'
        filings_list.append({
            'form_type': form,
            'filing_date': dates[i],
            'description': descriptions[i] or f'SEC Form {form}',
            'doc_url': doc_url,
        })
    return filings_list
  except Exception as e:
    print(f'Error fetching CIK {cik}: {e}')
    return []


def main():
  target_funds = [
      {
          'fund_name': 'Situational Awareness LP',
          'manager': 'Leopold Aschenbrenner',
          'cik': '0002045724',
      }
  ]

  output = {'updated_at': '', 'funds': []}

  for fund in target_funds:
    filings = fetch_sec_filings(fund['cik'])
    output['funds'].append({
        'fund_name': fund['fund_name'],
        'manager': fund['manager'],
        'cik': fund['cik'],
        'filings': filings,
    })

  with open('sec_intel_data.json', 'w') as f:
    json.dump(output, f, indent=2)

  print('Successfully updated sec_intel_data.json!')


if __name__ == '__main__':
  main()
