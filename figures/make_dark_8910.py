# -*- coding: utf-8 -*-
"""fig8-10: VVUQ pyramid, paradigm radar, research roadmap (Dark Lab)."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from dark_style import *

# ============================ FIG 8: VVUQ pyramid ============================
fig, ax = newfig(11.6, 7.4, 'Figure 8  |  The VVUQ Credibility Pyramid',
                 'ASME V&V 40 credibility activities mapped to the surgical-twin literature (status in Table 12)', ORANGE)
tiers = [
    ('Verification', 'code · calculation · regression testing', CYAN_D, 0.90),
    ('Geometric validation', 'Dice · HD95 · endpoint TRE', CYAN, 0.70),
    ('Physics validation', 'bench · in vivo measurement', ORANGE, 0.50),
    ('Clinical validation', 'RCTs · prospective · in silico trials', RED, 0.30),
]
pcx, base_y, th = 0.30, 0.155, 0.135
for name, sub, col, wf in tiers:
    w_ = wf * 0.42; x0 = pcx - w_ / 2
    w2_ = max(wf - 0.20, 0.12) * 0.42; x1 = pcx - w2_ / 2
    ax.add_patch(Polygon([(x0, base_y), (x0 + w_, base_y), (x1 + w2_, base_y + th), (x1, base_y + th)],
                         closed=True, fc=col, ec=BG, lw=1.2, alpha=0.95, zorder=3))
    ax.text(pcx, base_y + th / 2 + 0.012, name, ha='center', va='center', fontsize=10,
            color=TXT if col in (RED, CYAN_D) else '#0A1728', fontweight='bold', zorder=4)
    ax.text(pcx, base_y + th / 2 - 0.030, sub, ha='center', va='center', fontsize=7,
            color=TXT if col in (RED, CYAN_D) else '#0A1728', zorder=4, alpha=0.85)
    base_y += th + 0.012
ax.text(pcx, base_y + 0.01, 'credibility for the context of use', fontsize=9, color=ORANGE,
        ha='center', fontweight='bold')
# right: UQ panel
panel(ax, 0.58, 0.42, 0.385, 0.42, 'UNCERTAINTY QUANTIFICATION  (spans all levels)', edge=PURPLE)
uqs = [('segmentation error', 'surface error → geometry bias'),
       ('registration error', 'landmark TRE ≠ endpoint error'),
       ('parameter uncertainty', 'materials · boundary conditions'),
       ('model-form uncertainty', 'constitutive choice matters'),
       ('surrogate error', 'POD / neural-op extrapolation')]
yy = 0.76
for t, sub in uqs:
    ax.add_patch(Circle((0.605, yy + 0.008), 0.005, fc=PURPLE, ec='none'))
    ax.text(0.618, yy, t, fontsize=8.5, color=TXT, fontweight='bold', va='center')
    ax.text(0.618, yy - 0.026, sub, fontsize=7, color=SUB, va='center')
    yy -= 0.068
# right-bottom: applicability panel
panel(ax, 0.58, 0.155, 0.385, 0.22, 'APPLICABILITY ASSESSMENT', edge=GREEN)
ax.text(0.595, 0.315, 'does the evidence cover the context of use?', fontsize=8, color=TXT)
ax.text(0.595, 0.265, 'population · anatomy · pathology coverage\nmulti-center / domain-shift studies remain rare\n(M&Ms vendor shift · ABIDE cross-site)', fontsize=7.5,
        color=SUB, va='top', linespacing=1.6)
# left: literature status ribbon
panel(ax, 0.045, 0.155, 0.155, 0.42, 'LITERATURE STATUS', edge=DIM)
stats = [('strong', 'segmentation\n(in-distribution)', GREEN),
         ('sparse', 'physics validation\n(exemplary cases)', ORANGE),
         ('weak', 'endpoint error\ndomain shift', RED),
         ('nascent', 'UQ reporting\nprospective trials', RED)]
yy = 0.50
for t, sub, col in stats:
    ax.text(0.058, yy, t, fontsize=8.5, color=col, fontweight='bold')
    ax.text(0.058, yy - 0.030, sub, fontsize=6.8, color=SUB, va='top', linespacing=1.3)
    yy -= 0.093
ax.text(0.5, 0.045, 'a twin without an uncertainty statement is not yet a clinical device — prediction intervals are a minimal reporting standard',
        fontsize=8.5, color=RED, ha='center')
save(fig, 'fig8_vvuq')

# ============================ FIG 9: radar ============================
fig = plt.figure(figsize=(9.2, 7.6))
axbg = fig.add_axes([0, 0, 1, 1]); axbg.axis('off')
axbg.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec='none'))
axbg.add_patch(Rectangle((0.022, 0.945), 0.007, 0.038, fc=PURPLE, ec='none'))
axbg.text(0.038, 0.972, 'Figure 9  |  Three Ways to Drive the Loop', fontsize=15, color=TXT, fontweight='bold', va='top')
axbg.text(0.038, 0.935, 'physics-driven vs. data-driven vs. hybrid — a qualitative synthesis of Sections 3.2–3.4 (rubric in Supplementary Material)',
          fontsize=8.5, color=SUB, va='top')
ax = fig.add_axes([0.10, 0.06, 0.58, 0.78], polar=True, facecolor=PANEL)
criteria = ['per-query\ncompute cost', 'data\nrequirement', 'physical fidelity\n/ extrapolation', 'interpretability', 'validation\nmaturity']
data = {
    'Physics-driven': ([2, 5, 5, 4, 4], CYAN),
    'Data-driven': ([5, 2, 2, 2, 3], ORANGE),
    'Hybrid (physics-informed ML)': ([4, 3, 4, 3, 2], GREEN),
}
ang = np.linspace(0, 2 * np.pi, len(criteria), endpoint=False).tolist()
ang += ang[:1]
ax.set_facecolor(PANEL)
for name, (vals, c) in data.items():
    v = vals + vals[:1]
    ax.plot(ang, v, color=c, lw=2.4, label=name, zorder=4)
    ax.fill(ang, v, color=c, alpha=0.14, zorder=3)
    for ang_i, v_i in zip(ang, v):
        ax.plot(ang_i, v_i, 'o', color=c, markersize=5, zorder=5)
ax.set_xticks(ang[:-1])
ax.set_xticklabels(criteria, fontsize=9, color=TXT)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=7, color=SUB)
ax.set_ylim(0, 5)
ax.grid(color=EDGE, lw=0.7, alpha=0.7)
ax.spines['polar'].set_color(EDGE)
ax.legend(loc='center', bbox_to_anchor=(1.52, 0.5), fontsize=9, frameon=False, labelcolor=TXT)
axbg.text(0.5, 0.035, 'scores 1–5 per criterion: synthesis of Sections 3.2–3.4; scoring rubric archived in the living-review repository',
          fontsize=8, color=DIM, ha='center')
fig.savefig(os.path.join(OUT, 'fig9_radar.png'), dpi=300, facecolor=BG, bbox_inches='tight')
fig.savefig(os.path.join(PDFDIR, 'fig9_radar.pdf'), facecolor=BG, bbox_inches='tight')
print('saved fig9_radar')

# ============================ FIG 10: roadmap ============================
fig, ax = newfig(12.2, 7.4, 'Figure 10  |  Research Roadmap 2025–2030',
                 'five tracks with verifiable milestones — dependencies flow left to right', CYAN)
tracks = [
    ('Benchmarks & standards', CYAN, [(0.06, 0.30, 'surgical-twin\nbenchmark (Sec. 6.5)'), (0.46, 0.80, 'journal reporting\nguideline adopted')]),
    ('Neural-operator real-time sim.', PURPLE, [(0.12, 0.44, 'ms-level EP match\nto openCARP, <1 s'), (0.58, 0.92, 'intra-op re-simulation\nat navigation speed')]),
    ('Federated multi-center\nvalidation', CYAN_D, [(0.16, 0.52, 'cross-site twin\ncalibration studies'), (0.66, 0.96, 'federated twin\nvalidation network')]),
    ('Regulatory-grade\nin silico trials', RED, [(0.22, 0.58, 'V&V 40 credibility\ntemplates in use'), (0.72, 0.98, 'CM&S evidence in\ndevice submissions')]),
    ('Immersive human–twin\ninterfaces', GREEN, [(0.06, 0.34, 'interface-mediated\nplan iteration trials'), (0.52, 0.84, 'prospective evidence\nof changed plans')]),
]
yy = 0.72
for name, col, miles in tracks:
    ax.text(0.035, yy + 0.055, name, fontsize=9, color=TXT, fontweight='bold', va='center', linespacing=1.3)
    glow(ax, [0.05, 0.98], [yy, yy], col, lw=2.0, alpha=0.4)
    for x0, x1, lab in miles:
        bx0 = x0 + 0.15
        bw_ = min((x1 - x0) * 0.72, 0.965 - bx0)
        ax.add_patch(FancyBboxPatch((bx0, yy - 0.032), bw_, 0.064,
                                    boxstyle='round,pad=0.006', fc=col, ec='none', alpha=0.92, zorder=4))
        ax.text(bx0 + bw_ / 2, yy, lab, ha='center', va='center', fontsize=7,
                color='#0A1728' if col != CYAN_D else TXT, fontweight='bold', zorder=5, linespacing=1.3)
    yy -= 0.135
for year, x in zip(['2025', '2026', '2027', '2028', '2029', '2030'], np.linspace(0.08, 0.95, 6)):
    ax.text(x, 0.035, year, fontsize=9, color=SUB, ha='center')
    ax.plot([x, x], [0.055, 0.80], color=EDGE, lw=0.6, alpha=0.4, zorder=1)
save(fig, 'fig10_roadmap')
print('FIG8-10 DONE')
