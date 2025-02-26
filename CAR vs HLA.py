import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load the data
path="C:\\Users\\Arthur\\OneDrive\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"CAR vs HLA.xlsx", 
    sheet_name="Final chart", usecols="A:G", header=0)

#data['Log NPL ratio']=np.log(data['NPL ratio'])
#data=data[data['Range']!='20-30']
#data['NPL ratio sq']=np.square(data['NPL ratio']/100)

my_order = data['Range'].unique()
my_order=['(-10;-9]', '(-9;-8]','(-8;-7]','(-7;-6]', 
          '(-6;-5]','(-5;-4]', '(-4;-3]', '(-3;-2]','(-2;-1]', 
          '(-1;0]', '(0;1]', '(1;2]', '(2;3]', '(3;4]', '(4;5]',
          '(5;6]','(6;7]','(7;8]','(8;9]','(9;10]', '(11;12]',
          '(13;14]', '(14;15]', '(16;17]', '(23;24]']


data['Range'] = pd.Categorical(data['Range'], 
                                categories=my_order, 
                                ordered=True)

filtered_list=['(-5;-4]', '(-4;-3]', '(-3;-2]','(-2;-1]', 
          '(-1;0]', '(0;1]', '(1;2]', '(2;3]', '(3;4]', '(4;5]',
          '(5;6]']

data=data[data['Range'].isin(filtered_list)]

#Chart
sns.set_theme(style="whitegrid")
#iris = sns.load_dataset("iris")

# "Melt" the dataset to "long-form" or "tidy" representation
#iris = iris.melt(id_vars="species", var_name="measurement")

# Initialize the figure
f, ax = plt.subplots()
sns.despine(bottom=True, left=True)

sns.pointplot(
    data=data, x="Range", y="delta HLA", #hue="species",
    dodge=.8 - .8 / 3, order=filtered_list, palette="dark",
    markers="o", markersize=8, errorbar=None,
)
# Show each observation with a scatterplot
sns.stripplot(
    data=data, x="Range", y="delta HLA", #hue="NPL ratio",
    dodge=True, order=filtered_list, alpha=0.1, zorder=1, legend=False,
)

# Show the conditional means, aligning each pointplot in the
# center of the strips by adjusting the width allotted to each
# category (.8 by default) by the number of hue levels

plt.xlabel("Change in bank capital adequacy ratio (CAR),%", fontweight='bold')
plt.ylabel("Change in liquidity\n (measured as change in HLA/Total assets ratio, p.p.", fontweight='bold')

ax.text(
    0.99, 0.01, 
    "Data from IMF Financial soundness indicators database\nChart prepared by Arthur Grigoryan, CFA",
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

ax.set_title("Bank solvency deterioration may\n induce liquidity outflow.", fontsize=25, fontweight='bold', color='grey')
#ax.get_yaxis().set_visible(False)
#plt.yticks([]) 
plt.axhline(y=0, color="black", linewidth=1)
plt.ylim(-2, 2.2)

plt.show()














