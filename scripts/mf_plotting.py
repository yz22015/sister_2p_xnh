## plotting functions
#%% IMPORTS ----------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap

#%% UTILITIES - FORMATS -----------------------------------------------------------------------------------------------
def plot_format_xnhsister():
    """
    plot settings for xnhsister manuscript
    """
    # ensure texts objects can be edited in svg
    plt.rcParams['svg.fonttype'] = 'none'
    
    # font
    plt.rcParams.update({'font.size': 12})


#%% UTILITIES - COLOURS -----------------------------------------------------------------------------------------------
## pull out saved colourmaps
def get_saved_cmap(cmapName):
    """
    collect some cmaps here
    """
    if cmapName == 'corrM_red_green':
        cmap_this = sns.diverging_palette(h_neg = 150, h_pos = 20, s=100, l=65, sep=10, center='light', as_cmap=True)

    elif cmapName == 'corrM_pink_green':
        cmap_this = sns.diverging_palette(h_neg = 150, h_pos = 5, s=100, l=65, sep=10, center='light', as_cmap=True)
        
    elif cmapName == 'corrM_yellow_blue':
        c_hex = ['#5F9EA0', '#F5f5f5', '#FFA500'] # blue, grey, orange
        cmap_this = LinearSegmentedColormap.from_list('custom_colormap_hex', c_hex, N = 100)
    
    elif cmapName == 'corrM_orange_pink':
        c_hex = ['#BA55D3', '#DA70D6', '#FFFFFF', '#FFD700', '#FF8C00']
        cmap_this = LinearSegmentedColormap.from_list('custom_colormap_hex', c_hex, N = 100)
    
    elif cmapName == 'corrM_teal_pink':
        c_hex = ['#DB7093', '#FFC0CB', '#FFFFFF', '#008080', '#2F4F4F'] # teal, dark slate gray
        cmap_this = LinearSegmentedColormap.from_list('custom_colormap_hex', c_hex, N = 100)
    
    elif cmapName == 'cat3_yellow_grey_blue':
        c_hex = ['#5F9EA0', '#F5f5f5', '#FFA500'] # can specify >3 colorus!!
        cmap_this = LinearSegmentedColormap.from_list('custom_colormap_hex', c_hex, N = 3)
        
    elif cmapName == 'respM_orange_purple':
        cmap_this = sns.diverging_palette(h_neg = 275, h_pos = 50, s=200, l=65, sep=1, center='light', as_cmap=True)
    
    return cmap_this


#%% UTILISTIES - OUTLOOK -----------------------------------------------------------------------------------------------
def plot_outlook_odoPatch(xmin, xmax, ymin, ymax, c = 'grey', a = 0.2):
    """
    add to the plot odour presentation patch
    """
    w = xmax - xmin
    h = ymax - ymin
    oPatch = patches.Rectangle((xmin, ymin), w, h, facecolor = c, alpha = a)
    ax = plt.gca()
    ax.add_patch(oPatch)
    
    
def plot_outlook_boxOff(mode = 'topRight'):
    ax = plt.gca()
    if mode == 'topRight':
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    if mode == 'topRightBottom':
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
    if mode == 'topRightLeft':
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
    if mode == 'all':
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)


def plot_outlook_scalebarY(ymin, ymax, ypos, linewidth):
    """
    ymin, ymax: sets the size of scale bar
    ypos: sets the location in reference to data e.g. -2
    """
    plt.yticks([])
    ax = plt.gca()
    ax.spines['left'].set_bounds(ymin, ymax)
    ax.spines['left'].set_position(('data', ypos))
    ax.spines['left'].set_linewidth(linewidth)