# -*- coding: utf-8 -*-
"""Dark-Lab design system for the 10 method figures (fig1-10)."""
import os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Polygon, Rectangle

OUT = r'E:\综述\外科\投稿版本\新建文件夹\figures_V2\dark'
PDFDIR = os.path.join(OUT, 'pdf')
os.makedirs(OUT, exist_ok=True)
os.makedirs(PDFDIR, exist_ok=True)
IMG = os.path.expanduser(r'~/.scratch/fig3_images')

BG      = '#0A1728'
PANEL   = '#0F2438'
PANEL2  = '#122B42'
EDGE    = '#1E4E70'
CYAN    = '#39C6F3'
CYAN_D  = '#1E8FBF'
ORANGE  = '#F2A93B'
GREEN   = '#3BDC97'
PURPLE  = '#B57EDC'
RED     = '#F26D6D'
YELLOW  = '#F2E35C'
TXT     = '#E8F4FB'
SUB     = '#9DC4DA'
DIM     = '#5E87A0'

plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': TXT,
                     'axes.edgecolor': EDGE, 'axes.labelcolor': SUB,
                     'xtick.color': SUB, 'ytick.color': SUB})

def newfig(w=12.0, h=7.0, title=None, subtitle=None, accent=CYAN):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec='none', zorder=0))
    if title:
        ax.add_patch(Rectangle((0.018, 0.945), 0.006, 0.038, fc=accent, ec='none'))
        ax.text(0.032, 0.972, title, fontsize=15, color=TXT, fontweight='bold', va='top')
        if subtitle:
            ax.text(0.032, 0.938, subtitle, fontsize=9, color=SUB, va='top')
    return fig, ax

def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=300, facecolor=BG, bbox_inches='tight')
    fig.savefig(os.path.join(PDFDIR, name + '.pdf'), facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print('saved', name)

def glow(ax, xs, ys, color, lw=2.0, n=3, alpha=0.55, z=2):
    for i in range(n, 0, -1):
        ax.plot(xs, ys, color=color, lw=lw * (1 + i * 1.5), alpha=alpha / (i * 1.8),
                solid_capstyle='round', zorder=z)
    ax.plot(xs, ys, color=color, lw=lw, zorder=z + 1, solid_capstyle='round')

def panel(ax, x, y, w, h, title=None, edge=EDGE, fc=PANEL, lw=1.1, title_color=None, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.005,rounding_size=0.010',
                                fc=fc, ec=edge, lw=lw, zorder=z))
    if title:
        ax.text(x + 0.010, y + h - 0.014, title, fontsize=9, color=title_color or SUB,
                fontweight='bold', va='top', zorder=z + 2)

def card(ax, x, y, w, h, lines, edge=EDGE, fc=PANEL, fs=8, tc=TXT, z=3, title=None,
         title_fs=8.5, lw=1.1, align='center'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.005,rounding_size=0.008',
                                fc=fc, ec=edge, lw=lw, zorder=z))
    if isinstance(lines, str):
        lines = [lines]
    if align == 'center':
        ax.text(x + w / 2, y + h / 2, '\n'.join(lines), ha='center', va='center',
                fontsize=fs, color=tc, zorder=z + 2, linespacing=1.45)
    else:
        ax.text(x + 0.010, y + h - 0.014, '\n'.join(lines), ha='left', va='top',
                fontsize=fs, color=tc, zorder=z + 2, linespacing=1.45)

def chip(ax, x, y, w, h, text, color, fs=7.5, tc='#0A1728', z=4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.004,rounding_size=0.007',
                                fc=color, ec='none', zorder=z))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', zorder=z + 1)

def arrow(ax, p1, p2, color=CYAN, lw=2.0, ms=18, z=4, style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, zorder=z))

def node(ax, x, y, r, text, color, fs=8, tc=TXT, z=4, ring=True):
    if ring:
        ax.add_patch(Circle((x, y), r * 1.25, fc='none', ec=color, lw=1.0, alpha=0.5, zorder=z))
    ax.add_patch(Circle((x, y), r, fc=color, ec='none', zorder=z))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=tc,
            fontweight='bold', zorder=z + 1, linespacing=1.3)
