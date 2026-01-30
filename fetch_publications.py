import requests
import yaml
import os

# Your ORCID ID
ORCID_ID = '0000-0002-4395-7510'

headers = {
    'Accept': 'application/json'
}

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
        work_summary = group['work-summary'][0]
        
        # Extract title
        title_obj = work_summary.get('title', {})
        title = title_obj.get('title', {}).get('value', 'Untitled') if title_obj else 'Untitled'
        
        # Extract year
        pub_date = work_summary.get('publication-date')
        year = pub_date.get('year', {}).get('value', 'N/A') if pub_date else 'N/A'
        
        # Extract journal/venue
        journal = work_summary.get('journal-title')
        venue = journal.get('value', 'N/A') if journal else 'N/A'
        
        # Extract external IDs (DOI, etc.)
        external_ids = work_summary.get('external-ids', {}).get('external-id', [])
        doi = None
        url_link = None
        
        for ext_id in external_ids:
            if ext_id.get('external-id-type') == 'doi':
                doi = ext_id.get('external-id-value')
                url_link = f"https://doi.org/{doi}"
                break
        
        publications.append({
            'title': title,
            'year': year,
            'venue': venue,
            'doi': doi if doi else '',
            'url': url_link if url_link else ''
        })
    
    # Sort by year (most recent first)
    publications.sort(key=lambda x: str(x['year']), reverse=True)
    
    # Ensure _data directory exists
    os.makedirs('_data', exist_ok=True)
    
    # Save to YAML
    with open('_data/publications.yml', 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, allow_unicode=True, sort_keys=False)
    
    print(f"Successfully fetched {len(publications)} publications from ORCID")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)