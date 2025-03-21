import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load the data
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"Bank concentration and NPL.xlsx", 
    sheet_name="Final", usecols="A:J", header=0)

data['Log NPL ratio']=np.log(data['NPL ratio'])
data=data[data['Range']!='20-30']
data['NPL ratio sq']=np.square(data['NPL ratio']/100)

my_order = ["30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]


#Chart
sns.set_theme(style="whitegrid")
#iris = sns.load_dataset("iris")

# "Melt" the dataset to "long-form" or "tidy" representation
#iris = iris.melt(id_vars="species", var_name="measurement")

# Initialize the figure
f, ax = plt.subplots()
sns.despine(bottom=True, left=True)

sns.pointplot(
    data=data, x="Range", y="NPL ratio sq", #hue="species",
    dodge=.8 - .8 / 3, order=my_order, palette="dark",
    markers="o", markersize=8, errorbar=None,
)
# Show each observation with a scatterplot
sns.stripplot(
    data=data, x="Range", y="NPL ratio sq", #hue="NPL ratio",
    dodge=True, order=my_order, alpha=0.1, zorder=1, legend=False,
)

# Show the conditional means, aligning each pointplot in the
# center of the strips by adjusting the width allotted to each
# category (.8 by default) by the number of hue levels

plt.xlabel("Banking system concentraion \n (measured as share of biggest 5 banks' assets in the system)", fontweight='bold')
plt.ylabel("Riskiness \n (measured squared NPL ratio)", fontweight='bold')

ax.text(
    0.01, 0.5, 
    "Data from Worldbank and IMF \nChart prepared by Arthur Grigoryan, CFA",
    fontsize=8,
    #fontweight='bold',
    fontstyle='italic',
    color='grey',
    rotation=90,
    fontfamily='sans-serif',
    transform=ax.transAxes,        # use axes-relative coordinates
    ha='left',                     # horizontally align left
    va='bottom',                   # vertically align bottom
)

ax.set_title("The banking system is safest when the \n top 5 banks hold about 60-70% of the market.", fontsize=16, fontweight='bold', color='grey')
#ax.get_yaxis().set_visible(False)
plt.yticks([]) 

plt.ylim(0, 0.025)

plt.show()







