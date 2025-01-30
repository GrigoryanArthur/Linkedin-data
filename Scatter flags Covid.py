import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd

# ------------------------------------------------------------------
# SAMPLE DATA
# ------------------------------------------------------------------
# Let's say we have 4 countries with some (x,y) coordinates.
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"iMaPP_database-2024-12-2.xlsx", 
    sheet_name="MaPP", usecols="AX:BA", skiprows=32, nrows=103, header=0)

df = pd.DataFrame(data)

# Convert 'Date' to a proper datetime type and sort by date
#df['Date'] = pd.to_datetime(df['Date'])
#df = df.sort_values('Date').reset_index(drop=True)

#df['Y'] = range(1, len(df) + 1)


countries = df['iso2'].tolist()
x_coords   = df['X'].tolist()
y_coords   = df['Y'].tolist()

# Path to the folder that has our .png flags:
flags_folder = "C:/Users/Arthur/Documents/Linkedin data/Round flags/PNG/"

# ------------------------------------------------------------------
# CREATE FIGURE & AXIS
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4))

# ------------------------------------------------------------------
# PLOT EACH POINT AS A FLAG
# ------------------------------------------------------------------
for country, x, y in zip(countries, x_coords, y_coords):
    # Build the file path to the flag
    flag_path = os.path.join(flags_folder, country + ".png")
    
    # Read the PNG image as a numpy array
    img_array = plt.imread(flag_path)
    
    # Create an 'OffsetImage' to be placed at (x, y)
    imagebox = OffsetImage(img_array, zoom=0.035)  # 'zoom' adjusts the flag size
    
    # Create an AnnotationBbox to tie the image to the (x, y) data position
    ab = AnnotationBbox(
        imagebox,
        (x, y),
        frameon=True,
        bboxprops=dict(
            boxstyle="circle,pad=0.01",  # or "circle,pad=0.5" for a circle
            edgecolor="black",
            linewidth=1,
            facecolor="none"
        )
    )    
    ax.add_artist(ab)

# ------------------------------------------------------------------
# OPTIONAL: PLOT A NORMAL SCATTER IN THE BACKGROUND (just for reference)
# ------------------------------------------------------------------
# If you want to see where your points are in the coordinate system
# (and confirm they're in the right place), you can do:
ax.scatter(x_coords, y_coords, marker='o', color='red', alpha=0.2)

# ------------------------------------------------------------------
# ADJUST THE AXIS LIMITS & LABELS
# ------------------------------------------------------------------
# Make sure all flags are comfortably in view
#ax.set_xlim(0, 5)
#ax.set_ylim(0, 6)

ax.set_xticks([])            # removes the tick marks
ax.set_xticklabels([])  

ax.set_yticks([])            # removes the tick marks
ax.set_yticklabels([])  


ax.text(
    0.01, 0.4, 
    "Data from IMF's iMaPP database \nChart prepared by Arthur Grigoryan, CFA",
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

ax.set_title("Most of MacroPru loosening cases happened in March 2020 \n Although some countries reacted faster than the most", fontsize=15, fontweight='bold', color='black')

#plt.title("Scatter Plot with Country Flags")
#plt.xlabel("X-Axis")
#plt.ylabel("Y-Axis")

plt.show()



