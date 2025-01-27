import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import cairosvg    # for SVG -> PNG conversion
import numpy as np
import io
from PIL import Image

# -------------------------------------------------------------------
# 1) SAMPLE DATA
# -------------------------------------------------------------------
data = {
    'country': ['US', 'IT', 'ES', 'JP'],
    'date': ['2020-01-30', '2020-02-23', '2020-03-09', '2020-01-15']
}
df = pd.DataFrame(data)
# Convert 'date' strings to actual datetime objects
df['date'] = pd.to_datetime(df['date'])
# Sort by date (optional)
df = df.sort_values('date').reset_index(drop=True)

# For each row, assign a Y-value so that each flag appears at a different height
df['y'] = range(1, len(df) + 1)

# -------------------------------------------------------------------
# 2) FUNCTION TO LOAD & CONVERT SVG TO A NUMPY ARRAY
# -------------------------------------------------------------------
def load_svg_as_array(iso_code, folder='flags'):
    """
    Given a 2-letter ISO country code (e.g. 'US'),
    reads the corresponding .svg file from 'folder/xx.svg',
    converts it to PNG bytes via cairosvg,
    and returns a NumPy array that can be used with Matplotlib.
    """
    svg_path = f"{folder}/{iso_code.lower()}.svg"
    # Read the SVG file
    with open(svg_path, 'rb') as f:
        svg_data = f.read()
    # Convert the SVG bytes to PNG bytes
    png_data = cairosvg.svg2png(bytestring=svg_data)
    # Convert PNG bytes to a Pillow Image
    pil_img = Image.open(io.BytesIO(png_data))
    # Convert Pillow Image to NumPy array
    img_array = np.array(pil_img)
    return img_array

# -------------------------------------------------------------------
# 3) PLOT WITH FLAGS AS MARKERS
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

for i, row in df.iterrows():
    # Convert the datetime to a Matplotlib numeric date
    x_value = mdates.date2num(row['date'])
    y_value = row['y']
    
    # Load that country's SVG, convert to array
    flag_array = load_svg_as_array(row['country'])
    
    # Embed the image as an offset marker
    offset_img = OffsetImage(flag_array, zoom=0.3)  # adjust zoom as needed
    ab = AnnotationBbox(
        offset_img,
        (x_value, y_value),
        frameon=False  # no box around the image
    )
    ax.add_artist(ab)

# -------------------------------------------------------------------
# 4) FORMAT THE AXES
# -------------------------------------------------------------------
# Use automatic date tick locator/formatter
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()  # rotate and align date labels

# Set y-limits so flags are comfortably in the plot
ax.set_ylim(0, len(df) + 1)

# Optional labels
plt.title("Country COVID Response Dates (SVG Flags)")
plt.xlabel("Date")
plt.ylabel("Position")

plt.show()









flag_img = plt.imread("C:\\path\\to\\my\\flag.png")
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\Round flags\\circle-flags\\flags\\"
plt.imread(path+str(df.iloc[0,0])+".svg")
