import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"CAR by countries.xlsx", 
    sheet_name="Values", usecols="A:F", header=0) #skiprows=541, nrows=62,


# Create a scatterplot with 'total_bill' on x-axis, 'tip' on y-axis,
# and color the points by 'day' using the hue parameter.
sns.scatterplot(
    data=data, 
    x="Provision to equity", 
    y="CAR", 
    hue="Is CAR enough?",   # color by 'day'
    palette="deep",
    size='Hanke Index',
    sizes=(3, 100),
)

plt.xlim(-0.1, 0.5)
plt.ylim(0, 0.5)

# Add a title and display the plot
plt.title("Total Bill vs. Tip by Day")
plt.show()
