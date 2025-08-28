import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ---- geometric median (Weiszfeld) ----
# df: columns ['country','year','gdp_pc','credit_gdp']
path="C:\\Users\\Arthur\\OneDrive\\Documents\\Linkedin data\\8 Aug 2025 Animated chart\\"
df=pd.read_excel(path+"Data worldbank.xlsx", 
    sheet_name="Final", header=0)
# --- Animated scatter with smooth country motion + center-of-gravity trail ---
# Requirements: plotly, pandas, numpy
# ===================== CONFIG =====================
CENTER_METHOD = "geomedian"   # "mean", "median", or "geomedian"
USE_INTERPOLATION = False      # True -> fill missing years per country (linear)
FPS = 2                        # frames per second when exporting with screen-recording
FRAME_DURATION_MS = 200        # UI animation speed
LOG_X = True                   # log-scale GDP per capita

# Column names in your df:
COL_COUNTRY = "country"
COL_YEAR = "year"
COL_X = "gdp_pc"
COL_Y = "credit_gdp"
COL_COLOR = "region"           # optional
COL_SIZE = "population"        # optional

# ===================== INPUT ======================
# Expect df already loaded with columns above
# Example:
# df = pd.read_csv("your_data.csv")

# --------- Helpers ----------
def geom_median(points, eps=1e-7, max_iter=1000):
    """Geometric median via Weiszfeld's algorithm."""
    pts = np.asarray(points, dtype=float)
    if len(pts) == 0:
        return np.array([np.nan, np.nan])
    x = pts.mean(axis=0)
    for _ in range(max_iter):
        d = np.linalg.norm(pts - x, axis=1)
        if np.any(d < eps):  # exactly at a point
            return pts[d.argmin()]
        w = 1.0 / d
        x_new = (pts * w[:, None]).sum(axis=0) / w.sum()
        if np.linalg.norm(x - x_new) < eps:
            return x_new
        x = x_new
    return x

def center_of(points, method="geomedian"):
    if len(points) == 0:
        return (np.nan, np.nan)
    if method == "mean":
        c = np.mean(points, axis=0)
    elif method == "median":
        c = np.median(points, axis=0)
    else:  # geomedian default
        c = geom_median(points)
    return (float(c[0]), float(c[1]))

def maybe_interpolate(df, col_country, col_year, cols_to_interp, freq="Y"):
    """
    Fill missing years per country by linear interpolation (within min/max year of that country).
    Assumes annual integer years; keeps only integer years in the final output.
    """
    out = []
    for g, d in df.groupby(col_country, sort=False):
        dd = d.sort_values(col_year).copy()
        # Build complete integer-year index from min..max observed
        yr_min, yr_max = int(dd[col_year].min()), int(dd[col_year].max())
        idx = pd.Index(range(yr_min, yr_max + 1), name=col_year)
        dd = dd.set_index(col_year).reindex(idx)
        # carry other columns forward/backward where appropriate
        for c in dd.columns:
            if c not in cols_to_interp:
                dd[c] = dd[c].ffill().bfill()
        # interpolate numeric targets
        dd[cols_to_interp] = dd[cols_to_interp].interpolate(limit_direction="both")
        dd[col_country] = g
        dd = dd.reset_index()
        out.append(dd)
    return pd.concat(out, ignore_index=True)

# --------- Prep data ----------
_needed = {COL_COUNTRY, COL_YEAR, COL_X, COL_Y}
missing = _needed - set(df.columns)
if missing:
    raise ValueError(f"DataFrame is missing required columns: {missing}")

df = df.copy()
# Ensure numeric + drop rows with missing essentials
df[COL_YEAR] = pd.to_numeric(df[COL_YEAR], errors="coerce").astype("Int64")
df[COL_X] = pd.to_numeric(df[COL_X], errors="coerce")
df[COL_Y] = pd.to_numeric(df[COL_Y], errors="coerce")
df = df.dropna(subset=[COL_COUNTRY, COL_YEAR, COL_X, COL_Y])

# Optional interpolation
if USE_INTERPOLATION:
    numeric_targets = [COL_X, COL_Y]
    df = maybe_interpolate(df, COL_COUNTRY, COL_YEAR, numeric_targets)

years = sorted(pd.unique(df[COL_YEAR].dropna()))
has_color = COL_COLOR in df.columns
has_size = COL_SIZE in df.columns

# --------- Build frames with stable IDs and center trail ----------
frames = []
center_trail_x, center_trail_y = [], []

# Precompute per-year centers (so we can increment the trail each frame)
centers = {}
for yr in years:
    d = df[df[COL_YEAR] == yr]
    pts = d[[COL_X, COL_Y]].to_numpy()
    cx, cy = center_of(pts, CENTER_METHOD)
    centers[yr] = (cx, cy)

for yr in years:
    d = df[df[COL_YEAR] == yr].copy()
    # Marker kwargs
    marker_kwargs = {}
    if has_size:
        marker_kwargs["size"] = d[COL_SIZE]
        marker_kwargs["sizemode"] = "area"
        marker_kwargs["sizeref"] = (d[COL_SIZE].max() / (40**2)) if d[COL_SIZE].notna().any() else 1
        marker_kwargs["sizemin"] = 4

    # Country scatter (stable IDs make smooth tweening)
    country_scatter = go.Scatter(
        x=d[COL_X],
        y=d[COL_Y],
        mode="markers+text",
        ids=d[COL_COUNTRY],           # <-- key for smooth motion
        text=d[COL_COUNTRY],
        textposition="top center",
        textfont=dict(size=8, color="rgba(0,0,0,0.5)"),  # 50% transparent
        hovertemplate="%{text}<br>GDP pc=%{x}<br>Credit/GDP=%{y}<extra></extra>",
        marker=marker_kwargs,
        name="Countries",
        showlegend=False
    )

    # Center for this frame
    cx, cy = centers[yr]
    center_point = go.Scatter(
        x=[cx], y=[cy], mode="markers",
        marker=dict(symbol="x", size=16),
        name="Center",
        hovertemplate=f"Center ({CENTER_METHOD})<br>x=%{{x}}<br>y=%{{y}}<extra></extra>",
        showlegend=False
    )

    # Update trail up to current year
    center_trail_x.append(cx)
    center_trail_y.append(cy)
    trail = go.Scatter(
        x=center_trail_x,
        y=center_trail_y,
        mode="lines+markers",
        name="Center trail",
        hoverinfo="skip",
        showlegend=False
    )

    # Optional color dimension: replot as separate traces per color (keeps legend static)
    data_traces = []
    if has_color:
        for val, dd in d.groupby(COL_COLOR):
            mk = dict(marker_kwargs) if marker_kwargs else {}
            data_traces.append(go.Scatter(
                x=dd[COL_X], y=dd[COL_Y], mode="markers",
                ids=dd[COL_COUNTRY],
                text=dd[COL_COUNTRY],
                name=str(val),
                hovertemplate="%{text}<br>GDP pc=%{x}<br>Credit/GDP=%{y}<extra></extra>",
                showlegend=True if yr == years[0] else False,
                marker=mk
            ))
        frame_data = data_traces + [center_point, trail]
    else:
        frame_data = [country_scatter, center_point, trail]
    
    frames.append(go.Frame(
    name=str(int(yr)),
    data=frame_data,
    layout=go.Layout(
        title=f"Credit-to-GDP vs GDP per capita — {int(yr)}",
        annotations=[
            dict(
                text=str(int(yr)),
                xref="paper", yref="paper",
                x=0.9, y=0.1,        # position inside chart
                showarrow=False,
                font=dict(size=60, color="rgba(0,0,0,0.15)")  # big, faint
            )
        ]
    )
))


# --------- Figure layout ----------
# Initial data = first frame
init_data = frames[0].data

title_main = "Credit-to-GDP vs GDP per capita (100+ countries)"
subtitle = f"Center = {CENTER_METHOD} • Points tween across years"

fig = go.Figure(
    data=init_data,
    layout=go.Layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=title_main,
        xaxis_title="GDP per capita",
        yaxis_title="Credit-to-GDP (%)",
        xaxis=dict(type="log" if LOG_X else "linear"),
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "Play", "method": "animate",
                 "args": [None, {"frame": {"duration": FRAME_DURATION_MS, "redraw": False},
                                 "fromcurrent": True, "transition": {"duration": 150}}]},
                {"label": "Pause", "method": "animate",
                 "args": [[None], {"mode": "immediate",
                                   "frame": {"duration": 0, "redraw": False},
                                   "transition": {"duration": 0}}]}
            ],
            "x": 0, "y": 1.15, "xanchor": "left", "yanchor": "top"
        }],
        sliders=[{
            "active": 0,
            "pad": {"t": 30},
            "currentvalue": {"prefix": "Year: "},
            "steps": [{"label": str(int(yr)), "method": "animate",
                       "args": [[str(int(yr))],
                                {"mode": "immediate",
                                 "frame": {"duration": FRAME_DURATION_MS, "redraw": False},
                                 "transition": {"duration": 150}}]} for yr in years]
        }],
        showlegend=has_color
    ),
    frames=frames
)

# Add a small subtitle annotation
fig.add_annotation(
    xref="paper", yref="paper", x=0, y=1.09, showarrow=False,
    text=subtitle
)

# --------- Preview / Export ----------
# Preview interactively:
fig.show()

# Save a standalone HTML (shareable, opens in any browser):
# fig.write_html("animated_scatter.html", include_plotlyjs="cdn", auto_open=True)

# For LinkedIn video, quickest path is screen-recording the animation in the browser.
# If you prefer a true MP4 pipeline, export frames and stitch with ffmpeg.
# (Plotly's static image export requires additional setup; screen-record is usually simpler.)
