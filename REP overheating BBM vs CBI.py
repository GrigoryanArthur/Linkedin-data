import pandas as pd
import plotly.graph_objects as go

# Load demo data
path="C:\\Users\\Arthur\\OneDrive\\Documents\\Linkedin data\\"
df = pd.read_excel(path+"REP overheating episodes.xlsx",
    sheet_name="Final list", usecols="A:J", header=0)



# STEP 1: Clean and classify the data
df = df.copy()
binary_cols = [
    'LTV Tightened During Boom? (0/1)',
    'CCyB Raised During/Late Boom? (0/1)',
    'Other instruments Raised During/Late Boom? (0/1)'
]
df[binary_cols] = df[binary_cols].fillna(0).astype(int)
df['Peak Housing Price Growth (%)'] = df['Peak Housing Price Growth (%)'].fillna(0)

# Enhanced classification
def classify(row):
    ltv = row['LTV Tightened During Boom? (0/1)']
    ccyb = row['CCyB Raised During/Late Boom? (0/1)']
    other = row['Other instruments Raised During/Late Boom? (0/1)']
    if ltv == 1 and ccyb == 1:
        return 'LTV + CCyB Combined'
    elif ltv == 1:
        return 'LTV Only'
    elif ccyb == 1:
        return 'CCyB Only'
    elif other == 1:
        return 'Other Tool Substitution'
    else:
        return 'No Macroprudential Response'

df['Policy_Path'] = df.apply(classify, axis=1)

# STEP 2: Aggregate values
counts = df['Policy_Path'].value_counts()
means = df.groupby('Policy_Path')['Peak Housing Price Growth (%)'].mean().round(2)

ltv_only     = (df['Policy_Path'] == 'LTV Only').sum()
ltv_ccyb     = (df['Policy_Path'] == 'LTV + CCyB Combined').sum()
ccyb_only    = (df['Policy_Path'] == 'CCyB Only').sum()
other        = (df['Policy_Path'] == 'Other Tool Substitution').sum()
no_response  = (df['Policy_Path'] == 'No Macroprudential Response').sum()

# STEP 3: Define Sankey nodes and flows
labels = [
    "Housing Boom",                   # 0
    "LTV Tightened",                  # 1
    "No LTV Tightened",               # 2
    f"LTV Only (Avg: {means.get('LTV Only', 0)*100:.1f}%)",             # 3
    f"LTV + CCyB Combined (Avg: {means.get('LTV + CCyB Combined', 0)*100:.1f}%)",  # 4
    f"CCyB Only (Avg: {means.get('CCyB Only', 0)*100:.1f}%)",           # 5
    f"Other Tool Substitution (Avg: {means.get('Other Tool Substitution', 0)*100:.1f}%)", # 6
    f"No Response (Avg: {means.get('No Macroprudential Response', 0)*100:.1f}%)"   # 7
]

x_positions = [0.0, 0.25, 0.25, 0.75, 0.75, 0.75, 0.75, 0.75]
y_positions = [
    0.41,  # Housing Boom
    0.75,  # LTV Tightened
    0.30,  # No LTV Tightened
    0.95,  # LTV Only
    0.81,  # LTV + CCyB Combined
    0.55,  # CCyB Only
    0.25,  # Other Tool Substitution
    0.05   # No Response
]

source = [0, 0, 1, 1, 2, 2, 2]
target = [1, 2, 3, 4, 5, 6, 7]
value  = [ltv_only + ltv_ccyb, ccyb_only + other + no_response, ltv_only, ltv_ccyb, ccyb_only, other, no_response]
colors = [
    'rgba(0,128,0,0.5)',     # green
    'rgba(128,128,128,0.5)', # gray
    'rgba(0,128,0,0.5)',     # green
    'rgba(0,100,0,0.5)',     # dark green
    'rgba(255,165,0,0.5)',   # orange
    'rgba(30,144,255,0.5)',  # blue
    'rgba(220,20,60,0.5)'    # red
]

# STEP 4: Plot
fig = go.Figure(data=[go.Sankey(
    arrangement="fixed",  # key for full x/y control
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        #label=labels,
        color="lightgray",
        x=x_positions,
        y=y_positions
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=colors
    )
)])

fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')

fig.show()