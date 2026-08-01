# -*- coding: utf-8 -*-
"""Nature Publishing Group (NPG) figure design system."""
import os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle

OUT = r'E:\综述\外科\投稿版本\新建文件夹\figures_V2\nature'
PDFDIR = os.path.join(OUT, 'pdf')
os.makedirs(OUT, exist_ok=True)
os.makedirs(PDFDIR, exist_ok=True)
IMG = os.path.expanduser(r'~/.scratch/fig3_images')

# ---- NPG palette (ggsci "npg") ----
NPG_RED    = '#E64B35'
NPG_BLUE   = '#4DBBD5'
NPG_GREEN  = '#00A087'
NPG_NAVY   = '#3C5488'
NPG_SALMON = '#F39B7F'
NPG_LAV    = '#8491B4'
NPG_MINT   = '#91D1C2'
NPG_BRED   = '#DC0000'
NPG_BROWN  = '#7E6148'
INK        = '#1A1A1A'
GREY       = '#666666'
LGREY      = '#999999'
BORDER     = '#BBBBBB'
PANEL_BG   = '#F7F7F7'
WHITE      = '#FFFFFF'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'text.color': INK,
    'axes.edgecolor': BORDER, 'axes.labelcolor': INK,
    'xtick.color': INK, 'ytick.color': INK,
    'axes.linewidth': 0.8,
})

# ---- global font scale: one size up everywhere (text/title/label/legend/ticks) ----
FS = 1.18
from matplotlib.text import Text as _MText
_orig_text_init = _MText.__init__
def _scaled_text_init(self, *a, **k):
    _orig_text_init(self, *a, **k)
    self.set_size(self.get_size() * FS)
_MText.__init__ = _scaled_text_init

def newfig(w=7.2, h=5.0):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=WHITE, ec='none', zorder=0))
    return fig, ax

def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=600, facecolor='white', bbox_inches='tight')
    fig.savefig(os.path.join(PDFDIR, name + '.pdf'), facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print('saved', name)

def plabel(ax, letter, x=0.012, y=0.985, fs=10):
    """Nature bold lowercase panel letter."""
    ax.text(x, y, letter, fontsize=fs, fontweight='bold', color=INK, va='top', ha='left', zorder=10)

def panel(ax, x, y, w, h, title=None, ec=BORDER, fc=PANEL_BG, lw=0.8, title_color=INK,
          title_fs=7.5, z=2, rounded=True):
    style = 'round,pad=0.004,rounding_size=0.008' if rounded else 'square,pad=0.004'
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, zorder=z))
    if title:
        ax.text(x + 0.008, y + h - 0.010, title, fontsize=title_fs, color=title_color,
                fontweight='bold', va='top', zorder=z + 2)

def card(ax, x, y, w, h, title=None, sub=None, ec=BORDER, fc=WHITE, accent=None,
         title_fs=8, sub_fs=6.5, z=3, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.004,rounding_size=0.006',
                                fc=fc, ec=ec, lw=lw, zorder=z))
    if accent:
        ax.add_patch(Rectangle((x, y + h - 0.012), w, 0.012, fc=accent, ec='none', zorder=z + 1))
    if title:
        ax.text(x + w / 2, y + h - 0.022, title, fontsize=title_fs, color=INK,
                ha='center', va='top', fontweight='bold', zorder=z + 2, linespacing=1.35)
    if sub:
        ax.text(x + w / 2, y + h * 0.36, sub, fontsize=sub_fs, color=GREY,
                ha='center', va='center', zorder=z + 2, linespacing=1.4)

def arrow(ax, p1, p2, color=INK, lw=1.1, ms=11, z=4, style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, zorder=z))

def hbar(ax, x, y, w, color, h=0.006, z=3):
    ax.add_patch(Rectangle((x, y), w, h, fc=color, ec='none', zorder=z))
