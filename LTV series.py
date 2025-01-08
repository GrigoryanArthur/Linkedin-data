import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# # Generate sample data
# np.random.seed(42)
# data = np.random.rand(10, 10)  # Random 10x10 matrix
# columns = [f'Var{i+1}' for i in range(10)]
# df = pd.DataFrame(data, columns=columns)

# # Compute a correlation matrix (optional, here data is random, so this just illustrates a workflow)
# correlation_matrix = df.corr()

#Load the data
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"iMaPP_database-2024-12-2.xlsx", 
    sheet_name="LTV_average", usecols="O:PG", skiprows=541, nrows=62, header=0)

data.set_index('Year', inplace=True)
#data_cleaned = data.dropna()

# Plot the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=False, fmt=".2f", cmap="magma_r", cbar=True)
plt.title("The Loan-to-Value ratio became an active \n MacroPru instrument from mid-2010s, ", color='grey', fontweight='bold', fontsize=18)
#plt.xlabel("Year")
#plt.ylabel("Country")

n = 36  # Every 3rd year
plt.xticks(np.arange(0, data.shape[1], n), data.columns[::n], rotation=45, ha='right')

plt.gca().set_yticklabels(
    plt.gca().get_yticklabels(), fontstyle='italic', fontsize=10
)

plt.text(
    5, 55,  # Position: (-1.2 on x, 5 on y-axis center)
    "Data from IMF's iMaPP database \n Chart prepared by Arthur Grigoryan, CFA",
    color='white', 
    fontsize=8,
    fontstyle='italic', 
    rotation=90, 
    #va='center', 
    #ha='bottom'
)
plt.text(
    data.shape[1] + 3.5,  # Position to the right of the heatmap
    data.shape[0] / 2,    # Vertically centered
    "Darker colors indicate looser MacroPru policy", 
    fontsize=10, 
    color="black",
    fontweight='bold', 
    rotation=90, 
    va='center', 
    ha='left'
)
plt.show()

