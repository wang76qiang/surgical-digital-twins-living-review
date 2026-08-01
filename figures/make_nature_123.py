# -*- coding: utf-8 -*-
"""fig1-3 in NPG style: closed-loop control, PRISMA flow, image-to-simulation workflow."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from nature_style import *

# ============================ FIG 1: closed-loop control ============================
fig, ax = newfig(7.2, 5.4)

# nodes
card(ax, 0.045, 0.42, 0.17, 0.20, 'Patient', 'physical plant\nstate s$_t$', accent=NPG_BLUE, title_fs=9)
card(ax, 0.28, 0.68, 0.24, 0.17, 'Imaging & biosensing', 'y$_t$ = H(s$_t$) + v$_t$', accent=NPG_BLUE, title_fs=8)
card(ax, 0.30, 0.16, 0.20, 0.17, 'Data assimilation', 'posterior p(s, θ | y$_{1:t}$)', accent=NPG_GREEN, title_fs=8)
card(ax, 0.58, 0.42, 0.20, 0.20, 'Digital twin', 'forward model f$_\\theta$\nŝ$_{t+1}$ = f$_\\theta$(s$_t$, a)', accent=NPG_LAV, title_fs=9)
card(ax, 0.84, 0.42, 0.15, 0.20, 'Intervention\noptimization', 'a* = argmin E[L]', accent=NPG_SALMON, title_fs=8)

arrow(ax, (0.215, 0.57), (0.28, 0.72), NPG_NAVY)
arrow(ax, (0.40, 0.68), (0.40, 0.335), NPG_NAVY)
arrow(ax, (0.50, 0.245), (0.58, 0.46), NPG_GREEN)
arrow(ax, (0.78, 0.52), (0.84, 0.52), NPG_NAVY)
# execution return loop
ax.plot([0.915, 0.915, 0.13, 0.13], [0.42, 0.028, 0.028, 0.42], color=NPG_RED, lw=1.2, zorder=3)
arrow(ax, (0.13, 0.42), (0.13, 0.44), NPG_RED, lw=1.2)
ax.text(0.5, 0.035, 'execute intervention a$_t$ on patient → new observations', fontsize=7.5,
        color=NPG_RED, ha='center')
# time constants strip
for x, lab, col in [(0.18, 'preoperative · days–hours', NPG_BLUE),
                    (0.50, 'intraoperative · minutes–seconds', NPG_SALMON),
                    (0.82, 'postoperative · weeks–months', NPG_GREEN)]:
    ax.text(x, 0.945, lab, fontsize=7, color=col, ha='center', fontweight='bold')
ax.plot([0.05, 0.95], [0.915, 0.915], color=BORDER, lw=0.6)
save(fig, 'fig1_closed_loop')

# ============================ FIG 2: PRISMA ============================
fig, ax = newfig(7.2, 6.4)

flow = [
    ('619', 'Records identified', 'PubMed 539 · arXiv 80', NPG_NAVY),
    ('615', 'Records after deduplication', '4 duplicates removed', NPG_NAVY),
    ('615', 'Records screened (title/abstract)', 'documented exclusion rules', INK),
    ('482', 'Records assessed for eligibility', 'full-text review', INK),
    ('162', 'Studies included', '14 search · 144 hand-search/chasing · 4 anchors', NPG_GREEN),
]
fy, fh, fgap = 0.83, 0.105, 0.045
for i, (num, lab, sub, col) in enumerate(flow):
    bold = (i == len(flow) - 1)
    panel(ax, 0.05, fy, 0.55, fh, None, ec=col if bold else BORDER, fc=WHITE, lw=1.4 if bold else 0.8)
    ax.text(0.085, fy + fh / 2, num, fontsize=13, color=col, fontweight='bold', va='center')
    ax.text(0.165, fy + fh / 2 + 0.016, lab, fontsize=8, color=INK, va='center', fontweight='bold')
    ax.text(0.165, fy + fh / 2 - 0.018, sub, fontsize=6.5, color=GREY, va='center')
    if i < len(flow) - 1:
        arrow(ax, (0.325, fy - 0.004), (0.325, fy - fgap + 0.004), INK, lw=1.0)
    fy -= (fh + fgap)
# right cards
card(ax, 0.66, 0.53, 0.30, 0.13, None, None, ec=NPG_RED, lw=1.0)
ax.text(0.68, 0.635, '133', fontsize=11, color=NPG_RED, fontweight='bold')
ax.text(0.68, 0.575, 'excluded by rules:\nnon-medical domain 127\noff-topic 6', fontsize=7, color=INK, va='center', linespacing=1.5)
arrow(ax, (0.60, 0.582), (0.66, 0.585), NPG_RED, lw=1.0)
card(ax, 0.66, 0.20, 0.30, 0.13, None, None, ec=BORDER, lw=0.9)
ax.text(0.68, 0.305, 'S2', fontsize=11, color=GREY, fontweight='bold')
ax.text(0.68, 0.245, 'complete query logs, records\n& screening rules in repository', fontsize=7, color=INK, va='center', linespacing=1.5)
arrow(ax, (0.60, 0.282), (0.66, 0.255), GREY, lw=1.0)
save(fig, 'fig2_prisma')

# ============================ FIG 3: workflow ============================
fig = plt.figure(figsize=(7.2, 5.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 1, 1, fc=WHITE, ec='none'))

mods = [('CT-Thorax-5.0-B70f-Lungs.jpg', 'CT (thorax)'),
        ('AFIP-00405589-Glioblastoma-Radiology.jpg', 'MRI (glioblastoma)'),
        ('cardiac_mri_frame.png', 'Cine MRI (4-chamber)'),
        ('Transient Elastography (Fibroscan) of the Liver.jpg', 'US elastography')]
xw, gap = 0.219, 0.028
for i, (fn, lab) in enumerate(mods):
    x0 = 0.02 + i * (xw + gap)
    inset = ax.inset_axes([x0, 0.635, xw, 0.27])
    inset.imshow(mpimg.imread(os.path.join(IMG, fn)), cmap='gray', aspect='equal')
    inset.set_xticks([]); inset.set_yticks([])
    for sp in inset.spines.values():
        sp.set_edgecolor(BORDER); sp.set_linewidth(0.8)
    ax.text(x0 + xw / 2, 0.615, lab, fontsize=6.8, color=INK, ha='center')
ax.text(0.02, 0.945, 'real imaging inputs (Wikimedia Commons; credits in repository)',
        fontsize=7, color=GREY, fontweight='bold')
stages = [('Segmentation', 'nnU-Net · MedSAM\nTotalSegmentator', NPG_BLUE),
          ('Geometry & mesh', 'surface / volume\nFE-quality mesh', NPG_BLUE),
          ('Physics solvers', 'FEBio · SimVascular\nopenCARP', NPG_LAV),
          ('Acceleration', 'POD · neural ops.\n(378±280×)', NPG_SALMON),
          ('Decision', 'ranked plans\n+ uncertainty', NPG_GREEN)]
w, x, y0, h = 0.18, 0.02, 0.30, 0.21
for i, (t1, t2, col) in enumerate(stages):
    card(ax, x, y0, w, h, t1, t2, accent=col, title_fs=8.5, sub_fs=6.8)
    if i < 4:
        arrow(ax, (x + w + 0.003, y0 + h / 2), (x + w + 0.015, y0 + h / 2), INK, lw=1.1)
    x += w + 0.015
ax.text(0.02, 0.245, 'budgets:  segmentation seconds (GPU; VoxelMorph 0.37–0.55 s) · meshing minutes',
        fontsize=6.6, color=GREY)
ax.text(0.02, 0.213, 'full-order solve minutes–hours (ANTs CPU 9,059 s) · surrogate query ms–s',
        fontsize=6.6, color=GREY)
ax.text(0.02, 0.178, 'uncertainty cascade:  segmentation surface error → mesh / geometry error → parameter & boundary-condition error → prediction interval',
        fontsize=6.6, color=NPG_RED)
save(fig, 'fig3_workflow')
print('FIG1-3 NPG DONE')
