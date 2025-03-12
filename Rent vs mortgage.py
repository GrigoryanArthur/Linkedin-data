import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load the data
path="C:\\Users\\Arthur\\OneDrive\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"Numbeo data.xlsx", 
    sheet_name="Values levels", usecols="A:H", header=0)


my_order=['(0;5]', '(5;10]','(10;15]','(15;20]', 
          '(20;25]','(25;30]', '(30;35]', '(35;40]','(40;45]', 
          '(45;50]', '(50;55]', '(55;60]', '(60;65]', '(65;70]', '(70;75]',
          '(75,;0]','(80;85]','(85;90]','(90;95]','(95;100]']


data['Range'] = pd.Categorical(data['Range'], 
                                categories=my_order, 
                                ordered=True)

filtered_list=[ '(10;15]','(15;20]', 
          '(20;25]','(25;30]', '(30;35]', '(35;40]','(40;45]', 
          '(45;50]', '(50;55]', '(55;60]', '(60;65]', '(65;70]', '(70;75]',
          '(95;100]']

data=data[data['Range'].isin(filtered_list)]


#Chart
sns.set_theme(style="white")

# 1) Create a figure and a single Axes:
f, ax = plt.subplots()
sns.despine(bottom=True, left=True)  # optional

# 2) Plot the first pointplot on the left y-axis
sns.pointplot(
    data=data,
    x="Range",
    y="Mortgage loans as a share of total loans",
    order=filtered_list,
    markers="o",
    markersize=8,
    errorbar=None,
    join=False,
    legend=False,
    color="darkred",
    ax=ax  # <--- Render on this primary Axes
)

# 3) Create a twin Axes sharing the same x-axis (but independent y-axis)
ax2 = ax.twinx()

ax.spines["left"].set_color("darkred")       # Left spine
ax.tick_params(axis="y", colors="darkred")   # Tick labels and ticks
ax.yaxis.label.set_color("darkred") 

ax2.spines["right"].set_color("darkgreen")
ax2.tick_params(axis="y", colors="darkgreen")
ax2.yaxis.label.set_color("darkgreen")

# 4) Plot the second pointplot on the right y-axis
sns.pointplot(
    data=data,
    x="Range",
    y="Affordability Index",
    order=filtered_list,
    markers="o",
    markersize=8,
    errorbar=None,
    join=False,
    legend=False,
    color="darkgreen",
    ax=ax2  # <--- Render on the new, right-side Axes
)

# 5) (Optional) If you also have a stripplot for the first metric:
sns.stripplot(
    data=data,
    x="Range",
    y="Mortgage loans as a share of total loans",
    dodge=True,
    order=filtered_list,
    alpha=0.1,
    zorder=1,
    legend=False,
    ax=ax  # keep it on the left axis
)

# 6) Label axes
ax.set_xlabel("Price to rent ratio,%", fontweight='bold')
ax.set_ylabel("Mortgage portfolio as a share of total loans", fontweight='bold')

# Give the right axis a separate label if desired
ax2.set_ylabel("Mortgage affordability Index \n (the higher the bettwer)", fontweight='bold')

# 7) Add any text, titles, or other formatting
ax.text(
    0.95, 0.01,
    "Data from IMF Financial Soundness Indicators and numbeo.com\nChart prepared by Arthur Grigoryan, CFA",
    fontsize=8,
    fontstyle='italic',
    color='grey',
    rotation=90,
    transform=ax.transAxes,
    ha='left',
    va='bottom',
)
ax.set_title(
    "Higher rental costs may encourage \n  to buy homes through mortgages.",
    fontsize=25, fontweight='bold', color='grey'
)

#plt.ylim(0, 40)        # Y-limits for the left axis
ax2.set_ylim(0, 3)   # Example Y-limits for the right axis—adjust as needed
ax.set_ylim(0,40)

ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

plt.show()








