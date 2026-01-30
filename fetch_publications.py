import requests
import yaml
import os
import time

# Your ORCID ID
ORCID_ID = '0000-0002-4395-7510'

headers = {
    'Accept': 'application/json'
}

def get_crossref_metadata(doi):
    """Fetch metadata from CrossRef using DOI"""
    try:
        crossref_url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(crossref_url)
        if response.status_code == 200:
            data = response.json()['message']
            return {
                'venue': data.get('container-title', [''])[0] or data.get('publisher', ''),
                'type': data.get('type', '')
            }
    except Exception as e:
        print(f"CrossRef error: {e}")
    return None

try:
    # Fetch works from ORCID
    url = f'https://pub.orcid.org/v3.0/{ORCID_ID}/works'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching from ORCID: {response.status_code}")
        exit(1)
    
    data = response.json()
    publications = []
    
    for group in data.get('group', []):
        try:
            work_summary = group['work-summary'][0]
            put_code = work_summary.get('put-code')
            
            # Fetch detailed work information
            detail_url = f'https://pub.orcid.org/v3.0/{ORCID_ID}/work/{put_code}'
            detail_response = requests.get(detail_url, headers=headers)
            
            if detail_response.status_code != 200:
                print(f"Skipping work {put_code}: HTTP {detail_response.status_code}")
                continue
                
            work_detail = detail_response.json()
            
            # Extract title
            title_obj = work_detail.get('title', {})
            title = title_obj.get('title', {}).get('value', 'Untitled') if title_obj else 'Untitled'
            
            # Extract year
            pub_date = work_detail.get('publication-date')
            year = pub_date.get('year', {}).get('value', 'N/A') if pub_date else 'N/A'
            
            # Extract venue from ORCID
            journal = work_detail.get('journal-title')
            venue = journal.get('value', '') if journal else ''
            
            # Extract contributors - with safe handling
            authors = []
            contributors_data = work_detail.get('contributors')
            if contributors_data and isinstance(contributors_data, dict):
                contributor_list = contributors_data.get('contributor', [])
                if contributor_list:
                    for contributor in contributor_list:
                        credit_name = contributor.get('credit-name')
                        if credit_name and isinstance(credit_name, dict):
                            name = credit_name.get('value', '')
                            if name:
                                authors.append(name)
            
            authors_str = ', '.join(authors) if authors else 'Unknown'
            
            # Extract DOI
            external_ids = work_detail.get('external-ids', {}).get('external-id', [])
            doi = None
            url_link = None
            
            if external_ids:
                for ext_id in external_ids:
                    if ext_id.get('external-id-type') == 'doi':
                        doi = ext_id.get('external-id-value')
                        url_link = f"https://doi.org/{doi}"
                        break
            
            # If venue is missing, try CrossRef
            if doi and (not venue or venue == 'N/A'):
                print(f"Fetching venue from CrossRef for: {title[:50]}...")
                crossref_data = get_crossref_metadata(doi)
                if crossref_data and crossref_data['venue']:
                    venue = crossref_data['venue']
                time.sleep(0.2)
            
            publications.append({
                'title': title,
                'authors': authors_str,
                'year': year,
                'venue': venue if venue else 'N/A',
                'doi': doi if doi else '',
                'url': url_link if url_link else ''
            })
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error processing publication: {e}")
            continue
    
    # Sort by year
    publications.sort(key=lambda x: str(x['year']), reverse=True)
    
    os.makedirs('_data', exist_ok=True)
    
    with open('_data/publications.yml', 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, allow_unicode=True, sort_keys=False)
    
    print(f"Successfully fetched {len(publications)} publications")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)