# -*- coding: utf-8 -*-
"""fig8-10 in NPG style: VVUQ pyramid, radar, roadmap."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from nature_style import *

# ============================ FIG 8: VVUQ pyramid ============================
fig, ax = newfig(7.2, 5.4)

tiers = [
    ('Verification', 'code · calculation · regression testing', NPG_BLUE, 0.90),
    ('Geometric validation', 'Dice · HD95 · endpoint TRE', NPG_MINT, 0.72),
    ('Physics validation', 'bench · in vivo measurement', NPG_SALMON, 0.55),
    ('Clinical validation', 'RCTs · prospective · in silico trials', NPG_RED, 0.40),
]
pcx, base_y, th = 0.26, 0.135, 0.145
for name, sub, col, wf in tiers:
    w_ = wf * 0.40; x0 = pcx - w_ / 2
    w2_ = max(wf - 0.17, 0.16) * 0.40; x1 = pcx - w2_ / 2
    ax.add_patch(Polygon([(x0, base_y), (x0 + w_, base_y), (x1 + w2_, base_y + th), (x1, base_y + th)],
                         closed=True, fc=col, ec='white', lw=1.0, zorder=3))
    if wf > 0.6:
        ax.text(pcx, base_y + th / 2 + 0.016, name, ha='center', va='center',
                fontsize=7.2, color='white', fontweight='bold', zorder=4)
        ax.text(pcx, base_y + th / 2 - 0.026, sub, ha='center', va='center', fontsize=5.8,
                color='white', zorder=4, alpha=0.95)
    else:
        two = name.replace(' validation', '\nvalidation')
        ax.text(pcx, base_y + th / 2, two, ha='center', va='center',
                fontsize=6.5, color='white', fontweight='bold', zorder=4, linespacing=1.25)
    base_y += th + 0.012
ax.text(pcx, base_y + 0.012, 'credibility for the context of use', fontsize=8, color=INK,
        ha='center', fontweight='bold')
# right panels
panel(ax, 0.545, 0.42, 0.425, 0.46, 'UNCERTAINTY QUANTIFICATION\n(spans all levels)', fc=WHITE, ec=NPG_LAV)
uqs = [('segmentation error', 'surface error → geometry bias'),
       ('registration error', 'landmark TRE ≠ endpoint error'),
       ('parameter uncertainty', 'materials · boundary conditions'),
       ('model-form uncertainty', 'constitutive choice matters'),
       ('surrogate error', 'POD / neural-op extrapolation')]
yy = 0.795
for t, sub in uqs:
    ax.plot(0.565, yy, 'o', color=NPG_LAV, markersize=3)
    ax.text(0.575, yy, t, fontsize=7.5, color=INK, fontweight='bold', va='center')
    ax.text(0.575, yy - 0.027, sub, fontsize=6.5, color=GREY, va='center')
    yy -= 0.072
panel(ax, 0.545, 0.135, 0.425, 0.24, 'APPLICABILITY ASSESSMENT', fc=WHITE, ec=NPG_GREEN)
ax.text(0.56, 0.315, 'does the evidence cover the context of use?', fontsize=7.5, color=INK)
ax.text(0.56, 0.265, 'population · anatomy · pathology —\nmulti-center / domain-shift studies remain rare', fontsize=6.8,
        color=GREY, va='top', linespacing=1.6)
panel(ax, 0.007, 0.135, 0.183, 0.42, 'LITERATURE', fc=PANEL_BG, ec=BORDER)
stats = [('strong', 'segmentation', NPG_GREEN),
         ('sparse', 'physics validation', NPG_SALMON),
         ('weak', 'endpoint error', NPG_RED),
         ('nascent', 'UQ reporting', NPG_RED)]
yy = 0.49
for t, sub, col in stats:
    ax.text(0.015, yy, t, fontsize=7.5, color=col, fontweight='bold')
    ax.text(0.015, yy - 0.030, sub, fontsize=6.2, color=GREY, va='top', linespacing=1.35)
    yy -= 0.095
save(fig, 'fig8_vvuq')

# ============================ FIG 9: radar ============================
fig = plt.figure(figsize=(6.6, 5.4))
axbg = fig.add_axes([0, 0, 1, 1]); axbg.axis('off')
ax = fig.add_axes([0.14, 0.10, 0.56, 0.78], polar=True)

criteria = ['per-query\ncompute cost', 'data\nrequirement', 'physical fidelity\n/ extrapolation', 'interpretability', 'validation\nmaturity']
data = {
    'Physics-driven': ([2, 5, 5, 4, 4], NPG_BLUE),
    'Data-driven': ([5, 2, 2, 2, 3], NPG_RED),
    'Hybrid (physics-informed ML)': ([4, 3, 4, 3, 2], NPG_GREEN),
}
ang = np.linspace(0, 2 * np.pi, len(criteria), endpoint=False).tolist()
ang += ang[:1]
ax.set_facecolor('white')
for name, (vals, c) in data.items():
    v = vals + vals[:1]
    ax.plot(ang, v, color=c, lw=1.6, label=name, zorder=4)
    ax.fill(ang, v, color=c, alpha=0.10, zorder=3)
    for ang_i, v_i in zip(ang, v):
        ax.plot(ang_i, v_i, 'o', color=c, markersize=3.5, zorder=5)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(criteria, fontsize=7, color=INK)
ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=6, color=GREY)
ax.set_ylim(0, 5)
ax.grid(color='#DDDDDD', lw=0.6)
ax.spines['polar'].set_color(BORDER)
ax.legend(loc='center', bbox_to_anchor=(1.48, 0.5), fontsize=7.5, frameon=False)
axbg.text(0.735, 0.30, 'scores 1–5\n5 = most favorable', fontsize=6, color=GREY, va='top', linespacing=1.4)
fig.savefig(os.path.join(OUT, 'fig9_radar.png'), dpi=600, facecolor='white', bbox_inches='tight')
fig.savefig(os.path.join(PDFDIR, 'fig9_radar.pdf'), facecolor='white', bbox_inches='tight')
print('saved fig9_radar')

# ============================ FIG 10: roadmap ============================
fig, ax = newfig(7.2, 5.2)

tracks = [
    ('Benchmarks & standards', NPG_BLUE, [(0.06, 0.30, 'surgical-twin\nbenchmark (Sec. 6.5)'), (0.46, 0.80, 'journal reporting\nguideline adopted')]),
    ('Neural-operator real-time sim.', NPG_LAV, [(0.12, 0.44, 'ms-level EP match\nto openCARP, <1 s'), (0.58, 0.92, 'intra-op re-simulation\nat navigation speed')]),
    ('Federated multi-center validation', NPG_MINT, [(0.16, 0.52, 'cross-site twin\ncalibration studies'), (0.66, 0.96, 'federated twin\nvalidation network')]),
    ('Regulatory-grade in silico trials', NPG_RED, [(0.22, 0.58, 'V&V 40 credibility\ntemplates in use'), (0.62, 0.84, 'CM&S evidence in\ndevice submissions')]),
    ('Immersive human–twin interfaces', NPG_GREEN, [(0.06, 0.34, 'interface-mediated\nplan iteration trials'), (0.52, 0.84, 'prospective evidence\nof changed plans')]),
]
yy = 0.76
for name, col, miles in tracks:
    ax.text(0.035, yy + 0.052, name, fontsize=7.5, color=INK, fontweight='bold', va='center')
    ax.plot([0.05, 0.97], [yy, yy], color='#DDDDDD', lw=1.0, zorder=1)
    for x0, x1, lab in miles:
        bx0 = x0 + 0.15
        bw_ = min((x1 - x0) * 0.72, 0.955 - bx0)
        ax.add_patch(FancyBboxPatch((bx0, yy - 0.026), bw_, 0.052,
                                    boxstyle='round,pad=0.005', fc=col, ec='none', alpha=0.92, zorder=3))
        ax.text(bx0 + bw_ / 2, yy, lab, ha='center', va='center', fontsize=6,
                color='white', fontweight='bold', zorder=4, linespacing=1.3)
    yy -= 0.145
for year, x in zip(['2025', '2026', '2027', '2028', '2029', '2030'], np.linspace(0.08, 0.93, 6)):
    ax.text(x, 0.035, year, fontsize=7.5, color=GREY, ha='center')
    ax.plot([x, x], [0.06, 0.84], color='#EEEEEE', lw=0.6, zorder=0)
save(fig, 'fig10_roadmap')
print('FIG8-10 NPG DONE')
