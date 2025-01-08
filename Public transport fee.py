import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
path='C:\\Users\\Arthur\\Documents\\Linkedin data\\'
df=pd.read_excel(path+'Public transport fares numbeo 13 Nov 2024.xlsx', usecols='F:K', header=0)
df=df.dropna(how='any')

df.columns

sns.scatterplot(data=df, x='GDP per capita (th. USD, PPP)', y='Average monthly pass for public transport by reported cities (USD)',
 hue='Country group')

# Highlight a specific point (e.g., x=4, y=8)
highlight_x = [20.4451, 20.4451]
highlight_y = [23, 11]
plt.scatter(highlight_x, highlight_y, color='red', s=100, edgecolor='black', label='ARM')

# Add a data label
plt.annotate('Armenia-from 1 Jan',  # Text for the label
             (highlight_x[0], highlight_y[0]),  # Position of the point
             textcoords="offset points",  # How to position the label
             xytext=(250, 40),  # Offset from the point (x, y)
             ha='center',  # Horizontal alignment
             fontsize=10,  # Font size for the label
             arrowprops=dict(facecolor='grey', arrowstyle='->'),
             color='red',
             fontweight='bold')  # Optional arrow

plt.annotate('Armenia-now',  # Text for the label
             (highlight_x[1], highlight_y[1]),  # Position of the point
             textcoords="offset points",  # How to position the label
             xytext=(150, 10),  # Offset from the point (x, y)
             ha='center',  # Horizontal alignment
             fontsize=10,  # Font size for the label
             arrowprops=dict(facecolor='grey', arrowstyle='->'),
             color='red',
             fontweight='bold')  # Optional arrow

# Add data labels to each point
for i in range(len(df)):
    plt.text(x=df['GDP per capita (th. USD, PPP)'][i], 
    y=df['Average monthly pass for public transport by reported cities (USD)'][i], 
    s=df['Country code'][i], 
             fontsize=5, ha='right', va='bottom', color='grey') 

plt.ylabel('Average monthly pass for public \n transport by reported cities (USD)')
plt.xlabel('GDP per capita (th. USD, PPP)')

# Set x and y axis limits
plt.xlim(0, 100)  # x-axis from 0 to 6
plt.ylim(5, 100)

# Add a title to the chart
plt.title('Public transport monthly fare \n vs income by country', fontsize=16, fontweight='bold', color='grey')

# Add text below the plot
plt.figtext(0.5, -0.05, 'Source: Numbeo.com, Worldbank data, own calculations', 
            fontsize=12, ha='left', va='bottom')
            
# Add legend for the highlighted point
plt.legend()

# Show plot
plt.show()


