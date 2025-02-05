import pandas as pd

data = {
    'Country': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'Year': [2010, 2011, 2012, 2010, 2011, 2012, 2010, 2011, 2012],
    'CreditToGDP': [100, 110, 120, 200, 210, 250, 150, 180, 200],
    'PerCapitaIncome': [50, 55, 58, 80, 83, 90, 70, 75, 82]
}

df = pd.DataFrame(data)
df

# 1) Merge in 2010 values by country
df_2010 = df[df['Year'] == 2010].rename(
    columns={'CreditToGDP': 'CreditToGDP_2010', 'PerCapitaIncome': 'PerCapitaIncome_2010'}
)
df_merged = pd.merge(df, df_2010[['Country','CreditToGDP_2010','PerCapitaIncome_2010']], 
                     on='Country', how='left')

# 2) Calculate normalized values
df_merged['CreditToGDP_rel'] = df_merged['CreditToGDP'] / df_merged['CreditToGDP_2010']
df_merged['PerCapitaIncome_rel'] = df_merged['PerCapitaIncome'] / df_merged['PerCapitaIncome_2010']

df_merged.head()

import plotly.express as px

fig = px.scatter(
    df_merged,
    x="CreditToGDP_rel",
    y="PerCapitaIncome_rel",
    color="Country",               # Different color for each country
    animation_frame="Year",        # Slider or play button by 'Year'
    animation_group="Country",     # Ensures that transitions use the same point for a country
    hover_name="Country",          # Tooltip will show country name
    range_x=[0.9, 1.5],            # Adjust axes ranges as needed
    range_y=[0.9, 1.5],            # so that we see the movement clearly
    title="Credit-to-GDP vs. Per Capita Income (Indexed to 2010=1)"
)

fig.update_layout(
    xaxis_title="Credit to GDP (Relative to 2010)",
    yaxis_title="Per Capita Income (Relative to 2010)"
)

fig.show()






