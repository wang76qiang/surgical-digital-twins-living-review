# -*- coding: utf-8 -*-
"""fig1-3: closed-loop control, PRISMA flow, image-to-simulation workflow (Dark Lab)."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from dark_style import *

# ============================ FIG 1: closed-loop control ============================
fig, ax = newfig(12.0, 7.4, 'Figure 1  |  The Surgical Digital Twin as a Closed-Loop Control System',
                 'one architecture, three time constants — preoperative · intraoperative · postoperative', CYAN)

# patient node (left)
card(ax, 0.04, 0.40, 0.15, 0.20, ['PATIENT', 'physical plant', 'state s$_t$'], edge=CYAN, fs=9)
# sensing (top mid-left)
card(ax, 0.27, 0.66, 0.17, 0.16, ['Imaging & biosensing', 'y$_t$ = H(s$_t$) + v$_t$'], edge=CYAN_D, fs=8.5)
# assimilation (bottom mid-left)
card(ax, 0.27, 0.20, 0.17, 0.16, ['Data assimilation', 'posterior p(s, θ | y$_{1:t}$)'], edge=GREEN, fs=8.5)
# twin (center-right)
card(ax, 0.52, 0.40, 0.19, 0.20, ['DIGITAL TWIN', 'forward model f$_\\theta$', 'ŝ$_{t+1}$ = f$_\\theta$(s$_t$, a)'],
     edge=PURPLE, fs=9)
# optimizer (right)
card(ax, 0.79, 0.40, 0.17, 0.20, ['Intervention', 'optimization', 'a* = argmin E[L]'], edge=ORANGE, fs=9)

arrow(ax, (0.19, 0.55), (0.27, 0.72), CYAN)
arrow(ax, (0.355, 0.66), (0.355, 0.38), CYAN_D)
arrow(ax, (0.44, 0.28), (0.55, 0.40), GREEN)
arrow(ax, (0.71, 0.50), (0.79, 0.50), PURPLE)
# execute path: optimizer -> patient (glowing outer loop)
xs = [0.875, 0.875, 0.115, 0.115]
ys = [0.40, 0.10, 0.10, 0.40]
glow(ax, xs, ys, ORANGE, lw=2.6)
arrow(ax, (0.115, 0.40), (0.115, 0.42), ORANGE, lw=2.6, ms=22)
ax.text(0.5, 0.085, 'execute intervention a$_t$ on patient  →  new observations', fontsize=9,
        color=ORANGE, ha='center', fontweight='bold')
# stage time constants
for x, lab, col in [(0.20, 'PREOP\ndays–hours', CYAN), (0.50, 'INTRAOP\nminutes–seconds', ORANGE), (0.80, 'POSTOP\nweeks–months', GREEN)]:
    chip(ax, x - 0.055, 0.862, 0.11, 0.050, lab, col, fs=7.5)
ax.text(0.5, 0.035, 'observation → estimation → prediction → action → observation', fontsize=8,
        color=DIM, ha='center')
save(fig, 'fig1_closed_loop')

# ============================ FIG 2: PRISMA flow ============================
fig, ax = newfig(11.0, 7.6, 'Figure 2  |  Study Selection (reproducible search, executed 29 Jul 2026)',
                 'PubMed + arXiv systematic stream, completed by structured hand-searching and citation chasing', CYAN)

flow = [
    ('619', 'Records identified', 'PubMed 539 · arXiv 80', CYAN),
    ('615', 'After deduplication', '4 duplicates removed', CYAN_D),
    ('615', 'Screened (title/abstract)', 'documented exclusion rules', SUB),
    ('482', 'Assessed for eligibility', 'full-text review', SUB),
    ('162', 'INCLUDED', '14 search · 144 hand-search/chasing · 4 anchors', GREEN),
]
fy, fh, fgap = 0.78, 0.115, 0.055
for i, (num, lab, sub, col) in enumerate(flow):
    bold = (i == len(flow) - 1)
    card(ax, 0.06, fy, 0.46, fh, [], edge=col, fc=PANEL2 if bold else PANEL, lw=1.6 if bold else 1.0)
    ax.text(0.125, fy + fh / 2, num, fontsize=17, color=col, fontweight='bold', va='center')
    ax.text(0.19, fy + fh / 2 + 0.018, lab, fontsize=9.5, color=TXT, va='center', fontweight='bold')
    ax.text(0.19, fy + fh / 2 - 0.020, sub, fontsize=7.5, color=SUB, va='center')
    if i < len(flow) - 1:
        arrow(ax, (0.29, fy - 0.005), (0.29, fy - fgap + 0.005), CYAN, lw=2.0)
    fy -= (fh + fgap)
# exclusions (right)
exc = [('133', 'excluded by rules:\nnon-medical domain 127\noff-topic 6', RED, 0.60),
       ('S2', 'complete query logs,\nrecords & screening rules\nin repository', DIM, 0.28)]
for num, txt, col, yy in exc:
    card(ax, 0.60, yy, 0.34, 0.13, txt.split('\n'), edge=col, fs=8)
    ax.text(0.615, yy + 0.115, num, fontsize=13, color=col, fontweight='bold', va='center')
arrow(ax, (0.52, 0.505), (0.60, 0.645), RED, lw=1.6)
arrow(ax, (0.52, 0.235), (0.60, 0.325), DIM, lw=1.6)
# composition bar
ax.text(0.06, 0.085, 'Corpus composition', fontsize=9, color=SUB, fontweight='bold')
bx, bw = 0.06, 0.88
parts = [(14/162, CYAN), (144/162, CYAN_D), (4/162, DIM)]
x = bx
for frac, col in parts:
    ax.add_patch(Rectangle((x, 0.030), bw * frac, 0.032, fc=col, ec='none'))
    x += bw * frac
ax.text(bx + 0.003, 0.014, '14 reproducible search', fontsize=7, color=CYAN)
ax.text(0.94, 0.014, '144 hand-search / citation chasing  ·  4 anchors', fontsize=7, color=SUB, ha='right')
save(fig, 'fig2_prisma')

# ============================ FIG 3: workflow with real images ============================
fig = plt.figure(figsize=(12.0, 7.6))
fig.add_axes([0, 0, 1, 1]).axis('off')
axt = fig.axes[0]; axt.set_xlim(0, 1); axt.set_ylim(0, 1)
axt.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec='none'))
axt.add_patch(Rectangle((0.018, 0.955), 0.006, 0.034, fc=CYAN, ec='none'))
axt.text(0.032, 0.982, 'Figure 3  |  From Medical Images to Surgical Decisions', fontsize=15, color=TXT, fontweight='bold', va='top')
axt.text(0.032, 0.948, 'the image-to-simulation pipeline with representative tools, budgets and uncertainty entry points', fontsize=9, color=SUB, va='top')

mods = [('CT-Thorax-5.0-B70f-Lungs.jpg', 'CT (thorax)', 'CC BY-SA 4.0'),
        ('AFIP-00405589-Glioblastoma-Radiology.jpg', 'MRI (glioblastoma)', 'public domain'),
        ('cardiac_mri_frame.png', 'Cine MRI (4-chamber)', 'CC BY-SA 4.0'),
        ('Transient Elastography (Fibroscan) of the Liver.jpg', 'US elastography', 'CC BY-SA 4.0')]
xw, gap = 0.175, 0.028
for i, (fn, lab, lic) in enumerate(mods):
    x0 = 0.055 + i * (xw + gap)
    inset = axt.inset_axes([x0, 0.615, xw, 0.27])
    inset.imshow(mpimg.imread(os.path.join(IMG, fn)), cmap='gray', aspect='auto')
    inset.set_xticks([]); inset.set_yticks([])
    for sp in inset.spines.values():
        sp.set_edgecolor(CYAN_D); sp.set_linewidth(1.4)
    axt.text(x0 + xw / 2, 0.588, lab, fontsize=8.5, color=TXT, ha='center')
    axt.text(x0 + xw / 2, 0.567, lic, fontsize=6.2, color=DIM, ha='center')
axt.text(0.055, 0.915, 'REAL IMAGING INPUTS (Wikimedia Commons; credits in repository)', fontsize=8, color=SUB, fontweight='bold')

ax = axt
stages = [('Segmentation', 'nnU-Net · MedSAM\nTotalSegmentator', CYAN_D),
          ('Geometry & mesh', 'surface / volume\nFE-quality mesh', CYAN_D),
          ('Physics solvers', 'FEBio · SimVascular\nopenCARP', PURPLE),
          ('Acceleration', 'POD · neural ops.\n(378±280×)', ORANGE),
          ('Decision', 'ranked plans\n+ uncertainty', GREEN)]
w, x, y0, h = 0.165, 0.055, 0.30, 0.20
for i, (t1, t2, col) in enumerate(stages):
    card(ax, x, y0, w, h, [], edge=col, fc=PANEL)
    ax.text(x + w / 2, y0 + h - 0.035, t1, fontsize=10, color=col, ha='center', fontweight='bold')
    ax.text(x + w / 2, y0 + h / 2 - 0.03, t2, fontsize=8, color=SUB, ha='center', linespacing=1.5)
    if i < 4:
        arrow(ax, (x + w + 0.004, y0 + h / 2), (x + w + 0.021, y0 + h / 2), CYAN, lw=2.2)
    x += w + 0.025
for i in range(4):
    arrow(ax, (0.055 + i * (xw + gap) + xw / 2, 0.615), (0.055 + i * (xw + gap) + xw / 2, 0.545), CYAN_D, lw=1.4, ms=12)
ax.plot([0.055 + xw / 2, 0.055 + 2 * (xw + gap) + xw / 2 - 0.30], [0.545, 0.545], color=CYAN_D, lw=1.2, alpha=0.6)
ax.text(0.055, 0.225, 'budgets:  segmentation seconds (GPU; VoxelMorph 0.37–0.55 s)  ·  meshing minutes  ·  full-order solve minutes–hours (ANTs CPU 9,059 s)  ·  surrogate query ms–s',
        fontsize=8, color=SUB)
ax.text(0.055, 0.185, 'uncertainty cascade:  segmentation surface error  →  mesh / geometry error  →  parameter & boundary-condition error  →  prediction interval',
        fontsize=8, color=RED)
ax.text(0.055, 0.120, 'validated anchors:  TotalSegmentator Dice 0.943 (1,204 CTs)  ·  BraTS WT Dice 0.927 (Swin UNETR)  ·  ACDC diagnosis accuracy 0.96',
        fontsize=8, color=GREEN)
ax.text(0.055, 0.060, 'images: CT thorax & glioblastoma MRI & 4-chamber cine MRI & US elastography (Wikimedia Commons) — illustrative modalities, not pipeline outputs',
        fontsize=6.8, color=DIM)
save(fig, 'fig3_workflow')
print('FIG1-3 DONE')
