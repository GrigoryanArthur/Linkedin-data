import requests
import pandas as pd

# API endpoint and parameters
base_url = "https://api.openalex.org/works"
params = {
    "filter": "publication_year:1990",
    "sort": "cited_by_count:desc",
    "per-page": "200"
}

# Fetch top 100 most cited papers from 1990
response = requests.get(base_url, params=params)
data = response.json()

# Extract the works data
works = data.get("results", [])

# Prepare a structure to hold citation data
citation_records = []

for work in works:
    work_id = work.get('id', '')
    work_title = work.get('display_name', 'Unknown Title')
    # counts_by_year is a list of dicts: [{"year": XXXX, "cited_by_count": N}, ...]
    counts_by_year = work.get('counts_by_year', [])
    
    # Convert counts_by_year into a dictionary: {year: cited_by_count, ...}
    year_dict = {item['year']: item['cited_by_count'] for item in counts_by_year}
    
    # Create a record that includes the title and all year citation counts
    record = {'title': work_title, 'work_id': work_id}
    record.update(year_dict)
    citation_records.append(record)

# Convert list of dictionaries into a DataFrame
df = pd.DataFrame(citation_records)

# 'title' and 'work_id' serve as identifiers. Set 'title' as the index for convenience.
df.set_index('title', inplace=True)

# Sort columns so years go in ascending order. Exclude non-year columns first.
non_year_cols = ['work_id']
year_cols = [col for col in df.columns if col not in non_year_cols]
year_cols_sorted = sorted(year_cols)

df = df[non_year_cols + year_cols_sorted]

# Print the DataFrame
print(df)

# Example: Save to CSV
df.to_excel("citation_matrix_1990_top100.xlsx")
