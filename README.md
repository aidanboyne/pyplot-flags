# PyPlotFlags

A python alternative for ggflags R package. Creates a scatterplot where points are replaced by circular country flags.

### Usasge

*Installation*

```
pip install pyplotflags
```

*Core Function*

```
flagscatterplot(x, y, country_codes, ax=None, zoom=0.1, flag_dir=DEFAULT_FLAG_DIR, **kwargs)
```

Parameters:
    - x, y: Arrays of coordinates.
    - country_codes: Array of ISO Alpha-2 country codes (same length as x and y).
    - ax: Matplotlib axes object (uses current axes if None).
    - zoom: Scaling factor for the flag images.
    - flag_dir: Directory containing the .png flag images.
    - **kwargs: Standard matplotlib keyword args for scatterplots
