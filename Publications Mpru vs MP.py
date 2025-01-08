import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker

#rc('text', usetex=True)
#rc('text.latex', preamble=r'\usepackage{xcolor}')

topic1 = "monetary"
topic2 = "macroprudential"
year_counts_mp = {}
year_counts_mpp = {}

#Monetary policy
for year in range(1965, 1985):
    url = "https://api.crossref.org/works"
    params = {
        "query": topic1,
        "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
        "rows": 0  # We only want the total count
    }

    response = requests.get(url, params=params).json()
    total_results = response["message"]["total-results"]
    year_counts_mp[year] = total_results

#MacroPru policy
for year in range(2004, 2024):
    url = "https://api.crossref.org/works"
    params = {
        "query": topic2,
        "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
        "rows": 0  # We only want the total count
    }

    response = requests.get(url, params=params).json()
    total_results = response["message"]["total-results"]
    year_counts_mpp[year] = total_results

df1 = pd.DataFrame(list(year_counts_mp.items()), columns=['Year', 'Count'])
df2 = pd.DataFrame(list(year_counts_mpp.items()), columns=['Year', 'Count'])

#plotting
years_monetary = (df1['Year']).astype(int).to_numpy()
pubs_monetary = df1['Count'].to_numpy()

years_macroprudential = df2['Year'].to_numpy()
pubs_macroprudential = df2['Count'].to_numpy()

# Create two subplots side-by-side with shared y-axis
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 5))
fig.subplots_adjust(wspace=0.05)

# Plot Monetary Policy Data
ax1.plot(years_monetary, pubs_monetary, marker='o', linestyle='-', color='blue')#, label='Monetary Policy')
ax1.set_xlim(1965, 1985)
#ax1.set_xlabel("Year (Monetary Policy)")
ax1.set_ylabel("Number of Publications")

# Plot Macroprudential Policy Data
ax2.plot(years_macroprudential, pubs_macroprudential, marker='o', linestyle='-', color='red')#, label='Macroprudential Policy')
ax2.set_xlim(2000, 2021)
#ax2.set_xlabel("Year (Macroprudential Policy)")

# Set integer tick locators for both axes
ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

# Rotate x-axis labels by 90 degrees
ax1.tick_params(axis='x', labelrotation=90)
ax2.tick_params(axis='x', labelrotation=90)

# Adjust y-limits
ymin = min(pubs_monetary.min(), pubs_macroprudential.min())
ymax = max(pubs_monetary.max(), pubs_macroprudential.max())
ax1.set_ylim(ymin - 1, ymax + 1)

# Hide the right spine of ax1 and the left spine of ax2 for the break
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.yaxis.tick_right()

# Draw the break markers
d = .015
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (-d, d), **kwargs)          # bottom diagonal of ax1
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)   # top diagonal of ax1

kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, d), (-d, d), **kwargs)                 # bottom diagonal of ax2
ax2.plot((-d, d), (1 - d, 1 + d), **kwargs)          # top diagonal of ax2

# Create a combined legend
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2
fig.legend(handles, labels, loc='lower center', ncol=2)

plt.text(0.01, 0.95, "Monetary Policy \n publications 1965 to 1985",
         horizontalalignment='left',
         verticalalignment='top',
         color='blue',
         fontweight='bold',
         transform=plt.gca().transAxes)

plt.text(0.1, 0.5, "Macroprudential Policy \n publications from 2004 to 2024",
         horizontalalignment='left',
         verticalalignment='center',
         color='red',
         fontweight='bold',
         transform=plt.gca().transAxes)

ax1.text(
    0.07, 0.07, 
    "Data from crossref.org.\n Chart prepared by Arthur Grigoryan, CFA",
    fontsize=12,
    #fontweight='bold',
    fontstyle='italic',
    color='grey',
    rotation=90,
    fontfamily='sans-serif',
    transform=ax1.transAxes,        # use axes-relative coordinates
    ha='left',                     # horizontally align left
    va='bottom',                   # vertically align bottom
)


plt.suptitle("Still a long way to go :)", fontsize=15, fontweight='bold', color='black')
plt.show()

