import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pycountry
import pandas as pd

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FLAG_DIR = os.path.join(MODULE_DIR, 'flag_icons')

def lookup_country_code(country_name:str, flag_dir=DEFAULT_FLAG_DIR):
    lookup_df = pd.read_excel(os.path.join(flag_dir,'country_code_list.xlsx'))
    row = lookup_df[lookup_df['Country'] == country_name]['Alpha-2 code']
    if not row.empty: code = row.iloc[0]
    if not row.empty:
        print(f'{country_name} has code {code}')
    else:
        print(f'Invalid country name. Valid Names include {list(lookup_df.Country)}')
    return None

def get_flag_filename(iso_code):
    """Converts an ISO Alpha-2 code to your specific file naming convention."""
    try:
        country = pycountry.countries.get(alpha_2=iso_code.upper())
        if country:
            # Image naming convention: "United States" -> "united-states.png"
            # Using common_name if available to avoid official names like "Korea, Republic of"
            name = getattr(country, 'common_name', country.name)            
            clean_name = name.lower().replace(',', '').replace(' ', '-')
            return f"{clean_name}.png"
        else:
            if iso_code == 'WO': return "world.png"
            if iso_code == 'EU': return "eu.png"
        return None

    except Exception:
        return None

def flagscatterplot(x, y, country_codes, ax=None, zoom=0.1, flag_dir=DEFAULT_FLAG_DIR, **kwargs):
    """
    Creates a scatterplot where points are replaced by circular country flags.
    
    Parameters:
    - x, y: Arrays of coordinates.
    - country_codes: Array of ISO Alpha-2 country codes (same length as x and y).
    - ax: Matplotlib axes object (uses current axes if None).
    - zoom: Scaling factor for the flag images.
    - flag_dir: Directory containing the .png flag images.
    - **kwargs: Standard matplotlib.pyplot.scatter arguments.
    """
    if ax is None:
        ax = plt.gca()

    # Plot invisible standard scatter to auto-scale the axes
    ax.scatter(x, y, alpha=0, **kwargs)

    for xi, yi, code in zip(x, y, country_codes):
        filename = get_flag_filename(code)
        
        if not filename:
            print(f"Warning: Could not resolve ISO code '{code}'. Skipping point.")
            continue
            
        filepath = os.path.join(flag_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: Image not found at {filepath}. Skipping point.")
            continue

        try:
            img = mpimg.imread(filepath)            
            imagebox = OffsetImage(img, zoom=zoom)
            ab = AnnotationBbox(imagebox, (xi, yi), frameon=False, pad=0.0)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Error loading flag for {code}: {e}")

    return ax