from scholarly import scholarly
import yaml
import os

# Your Google Scholar ID
SCHOLAR_ID = 'Cr8J98cAAAAJ'

try:
    # Fetch your profile directly by ID
    author = scholarly.search_author_id(SCHOLAR_ID)
    author_filled = scholarly.fill(author)
    
    publications = []
    
    for pub in author_filled['publications']:
        try:
            pub_filled = scholarly.fill(pub)
            bib = pub_filled['bib']
            
            publications.append({
                'title': bib.get('title', 'Untitled'),
                'authors': bib.get('author', 'Unknown'),
                'year': bib.get('pub_year', 'N/A'),
                'venue': bib.get('venue', bib.get('journal', 'N/A')),
                'citations': pub_filled.get('num_citations', 0),
                'url': pub_filled.get('pub_url', ''),
                'scholar_url': pub_filled.get('url_scholarbib', '')
            })
        except Exception as e:
            print(f"Error processing publication: {e}")
            continue
    
    # Sort by year (most recent first)
    publications.sort(key=lambda x: str(x['year']), reverse=True)
    
    # Ensure _data directory exists
    os.makedirs('_data', exist_ok=True)
    
    # Save to YAML
    with open('_data/publications.yml', 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, allow_unicode=True, sort_keys=False)
    
    print(f"Successfully fetched {len(publications)} publications")
    
except Exception as e:
    print(f"Error fetching publications: {e}")
    exit(1)