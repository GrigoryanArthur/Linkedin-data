import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick

# Load the dataset
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"CAR by countries.xlsx", 
    sheet_name="Values", usecols="A:G", header=0) #skiprows=541, nrows=62,


bins = [-25, 0, 10, 25]  
labels = ["Low", "Medium", "High"]

data['gdp growth bins']=pd.cut(data["Hanke Index"], bins=bins, labels=labels, include_lowest=True)

size_mapping = {
    "Low": 2,      # Marker size for total_bill in [0,10]
    "Medium": 6,  # Marker size for total_bill in (10,20]
    "High": 75  # Marker size for total_bill in (20,60]
}

custom_palette = {
    "CCyB would cover this": "darkgreen",
    "Combined buffer would be enough": "darkorange",
    "Capital shortfall": "darkred"
}

# # Create a scatterplot with 'total_bill' on x-axis, 'tip' on y-axis,
# # and color the points by 'day' using the hue parameter.
# ax=sns.scatterplot(
#     data=data, 
#     x="Provision to equity", 
#     y="Excess CAR", 
#     hue="Is CAR enough?",   # color by 'day'
#     palette=custom_palette,
#     size='gdp growth bins',
#     sizes=size_mapping,
#     legend=False
# )

# plt.xlim(-0.025, 0.075)
# plt.ylim(0, 0.5)

# plt.ylabel("Excess capital above minimum \n (measured as Capital Adequacy Ratio - 8%)", fontweight='bold', color='grey')
# plt.xlabel("Yearly Provisions to Risk Weighted Assets, %", fontweight='bold', color='grey')

# ax.text(
#     0.01, 0.07, 
#     "Data from IMF FSIs\n Chart prepared by Arthur Grigoryan, CFA",
#     fontsize=8,
#     #fontweight='bold',
#     fontstyle='italic',
#     color='grey',
#     rotation=90,
#     fontfamily='sans-serif',
#     transform=ax.transAxes,        # use axes-relative coordinates
#     ha='left',                     # horizontally align left
#     va='bottom',                   # vertically align bottom
# )

# ax.set_title("In about 93% of cases, the Countercyclical capital \n buffer alone would be enough to absorb losses", fontsize=12, fontweight='bold', color='black')

# ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
# ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

# # Add a title and display the plot
# #plt.title("Total Bill vs. Tip by Day")
# plt.show()



sns.set_theme(style="white", context="paper")
ax=sns.stripplot(
    data=data[data['Year']>=2005], x="Year", y="Provision to equity", hue="Is CAR enough?",
    dodge=False, #order=my_order, 
    alpha=0.5, zorder=1, legend=False,
    palette=custom_palette,
    edgecolor="grey",       # black border around the points
    linewidth=0.5,
    jitter=0.2, 
    size=4,
)

#plt.xlim(-0.025, 0.075)
plt.ylim(-0.025, 0.075)

plt.ylabel("Yearly Provisions to Risk Weighted Assets, %", fontweight='bold', color='grey', size=11)
#plt.xlabel("Yearl", fontweight='bold', color='grey')

ax.xaxis.set_major_locator(mtick.MultipleLocator(3))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

ax.text(
    0.01, 0.01, 
    "Data from IMF FSIs. Chart prepared by Arthur Grigoryan, CFA",
    fontsize=8,
    #fontweight='bold',
    fontstyle='italic',
    color='grey',
    #rotation=90,
    fontfamily='sans-serif',
    transform=ax.transAxes,        # use axes-relative coordinates
    ha='left',                     # horizontally align left
    va='bottom',                   # vertically align bottom
)

ax.set_title("In about 93% of cases, the Countercyclical capital \n buffer alone would be enough to absorb losses", fontsize=15, fontweight='bold', color='black')

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Rotate tick labels vertically
plt.setp(ax.get_xticklabels(), rotation=90)

plt.show()

