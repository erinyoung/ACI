import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from matplotlib.colors import LogNorm, Normalize
import logging
import copy

def natural_sort_key(s):
    """
    Sorts strings containing numbers naturally (e.g., 'Amp2' before 'Amp10').
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', str(s))]

def plot_heatmap(df, output_path, title, log_scale=True):
    """
    Generates a heatmap of coverage depth or efficiency.
    
    Args:
        df (pd.DataFrame): Data source.
        output_path (str): Output filename.
        title (str): Plot title.
        log_scale (bool): If True, use LogNorm and mask Zeros as white.
                          If False, use standard Linear scale.
    """
    # 1. Data Prep
    plot_df = df.copy()
    if "bam" in plot_df.columns:
        plot_df = plot_df.set_index("bam")
    
    # 2. Sort Columns
    try:
        sorted_cols = sorted(plot_df.columns, key=natural_sort_key)
        plot_df = plot_df[sorted_cols]
    except Exception as e:
        logging.warning(f"Could not sort amplicon columns naturally: {e}")

    # 3. Convert to numpy
    data = plot_df.values.astype(float)
    samples = plot_df.index
    amplicons = plot_df.columns

    # 4. Setup Plot
    height = max(6, len(samples) * 0.4)
    fig, ax = plt.subplots(figsize=(15, height))

    # 5. Color Mapping Logic
    my_cmap = copy.copy(plt.cm.viridis)
    
    if log_scale:
        # --- LOG SCALE (For Depth) ---
        # Zeros are errors ("Dropouts"), paint them white
        my_cmap.set_bad(color='white') 
        masked_data = np.ma.masked_where(data <= 0, data)
        
        # Avoid dynamic range issues with log(0)
        max_val = np.max(data) if np.max(data) > 0 else 10
        norm = LogNorm(vmin=1, vmax=max_val)
        cbar_label = 'Read Depth (Log Scale)'
        
        # Text annotation for dropouts
        ax.text(0.5, -0.15, "White cells indicate 0x coverage (Dropout)", 
                transform=ax.transAxes, ha="center", fontsize=10, color="gray")
        
        plot_data = masked_data
    else:
        # --- LINEAR SCALE (For Efficiency %) ---
        # Zeros are just 0%, paint them standard purple (bottom of viridis)
        # No masking needed
        norm = Normalize(vmin=0, vmax=np.max(data))
        cbar_label = 'Reads (%)'
        plot_data = data

    # Plot
    cax = ax.imshow(plot_data, aspect='auto', cmap=my_cmap, 
                    norm=norm, interpolation='nearest')

    # 6. Labels
    ax.set_xticks(np.arange(len(amplicons)))
    ax.set_xticklabels(amplicons, rotation=90, fontsize=8)
    
    ax.set_yticks(np.arange(len(samples)))
    ax.set_yticklabels(samples, fontsize=10)

    # 7. Colorbar
    cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(cbar_label)

    ax.set_title(title)
    ax.set_xlabel("Amplicons")
    ax.set_ylabel("Samples")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()