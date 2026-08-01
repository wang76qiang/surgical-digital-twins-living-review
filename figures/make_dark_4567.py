# -*- coding: utf-8 -*-
"""fig4-7: unified framework, taxonomy, case map, forest plot (Dark Lab)."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from dark_style import *

# ============================ FIG 4: unified framework ============================
fig, ax = newfig(12.4, 7.4, 'Figure 4  |  The Unified Image-Centric Framework',
                 'physical and virtual domains coupled through the virtual-iteration loop and data assimilation', PURPLE)
# lanes
panel(ax, 0.03, 0.56, 0.94, 0.30, 'PHYSICAL DOMAIN', edge=DIM, fc='#0C1E31')
panel(ax, 0.03, 0.10, 0.94, 0.40, 'VIRTUAL DOMAIN  (the twin)', edge=CYAN_D, fc=PANEL)
# physical nodes
phys = [('Patient', 'anatomy · physiology\npathology', CYAN),
        ('Imaging & sensors', 'CT · MRI · US · iCT/iUS\nwearables · EHR', CYAN),
        ('Surgery', 'intervention a$_t$\n(executed plan)', ORANGE)]
pw = 0.22
for i, (t, sub, col) in enumerate(phys):
    x = 0.06 + i * 0.33
    card(ax, x, 0.64, pw, 0.17, [], edge=col)
    ax.text(x + pw / 2, 0.775, t, fontsize=12, color=col, ha='center', fontweight='bold')
    ax.text(x + pw / 2, 0.70, sub, fontsize=8, color=SUB, ha='center', linespacing=1.5)
# virtual chain
chain = [('Segmentation &\nreconstruction', 'nnU-Net · MedSAM\nTotalSegmentator', CYAN_D),
         ('Fusion &\nregistration', 'VoxelMorph\nSynthMorph', CYAN_D),
         ('Functional\nmodeling', 'FEBio · SimVascular\nopenCARP · TumorTwin', PURPLE),
         ('Virtual\niteration', 'bilevel optimization\nunder uncertainty', ORANGE),
         ('Clinical\ndecision', 'ranked plans + UQ\nhuman-in-the-loop', GREEN)]
cw = 0.162
for i, (t, sub, col) in enumerate(chain):
    x = 0.045 + i * 0.187
    card(ax, x, 0.155, cw, 0.24, [t], edge=col, fs=10)
    ax.text(x + cw / 2, 0.225, sub, fontsize=7, color=SUB, ha='center', linespacing=1.45)
    if i < 4:
        arrow(ax, (x + cw + 0.003, 0.275), (x + cw + 0.022, 0.275), CYAN, lw=2.0, ms=15)
# couplings
arrow(ax, (0.39, 0.625), (0.24, 0.405), CYAN, lw=2.2)
ax.text(0.315, 0.50, 'observation y$_t$', fontsize=8, color=CYAN, rotation=63)
arrow(ax, (0.78, 0.405), (0.83, 0.625), ORANGE, lw=2.2)
ax.text(0.855, 0.50, 'decision\nexecuted a$_t$', fontsize=8, color=ORANGE, ha='left')
arrow(ax, (0.72, 0.625), (0.60, 0.405), GREEN, lw=2.2, ls='--')
ax.text(0.615, 0.50, 'post-op observations\n(data assimilation)', fontsize=8, color=GREEN, ha='right')
# stage ribbons
for x, lab, col in [(0.14, 'PREOPERATIVE', CYAN), (0.50, 'INTRAOPERATIVE', ORANGE), (0.84, 'POSTOPERATIVE', GREEN)]:
    chip(ax, x - 0.07, 0.862, 0.14, 0.042, lab, col, fs=7.2)
ax.text(0.5, 0.045, 'five computational stages: anatomical modeling → registration → functional modeling → dynamic updating → closed-loop iteration',
        fontsize=8, color=DIM, ha='center')
save(fig, 'fig4_framework')

# ============================ FIG 5: taxonomy ============================
fig, ax = newfig(12.0, 7.2, 'Figure 5  |  A Taxonomy of Virtual Iteration',
                 'every method in this review locates in the space of three orthogonal dimensions', ORANGE)
cols = [
    ('DRIVING PARADIGM', CYAN, [
        ('Physics-driven', 'FEA · CFD · FSI · EP\nFEBio · SimVascular · openCARP', CYAN_D),
        ('Data-driven', 'ML outcome predictors\nrisk & recovery models', ORANGE),
        ('Hybrid (physics-informed ML)', 'PINNs · neural operators\nVR-differentiable simulation', PURPLE)]),
    ('ITERATION TIMING', GREEN, [
        ('Offline', 'preoperative\nplan optimization', CYAN),
        ('Online', 'intraoperative re-planning\nseconds-scale', ORANGE),
        ('Longitudinal', 'postoperative healing\nrehabilitation · surveillance', GREEN)]),
    ('UPDATED OBJECT', PURPLE, [
        ('Structure', 'anatomy deforms / grows\nregistration · growth models', CYAN_D),
        ('Parameters', 'materials · boundary conditions\nBayesian / EnKF assimilation', PURPLE),
        ('Policy', 'the intervention itself\nBayesian opt. · RL · MPC', GREEN)]),
]
for ci, (title, tcol, leaves) in enumerate(cols):
    x0 = 0.04 + ci * 0.325
    chip(ax, x0, 0.855, 0.28, 0.05, title, tcol, fs=9)
    yy = 0.665
    for name, sub, col in leaves:
        card(ax, x0, yy, 0.28, 0.16, [], edge=col)
        ax.text(x0 + 0.14, yy + 0.115, name, fontsize=10, color=col, ha='center', fontweight='bold')
        ax.text(x0 + 0.14, yy + 0.048, sub, fontsize=7.2, color=SUB, ha='center', linespacing=1.4)
        arrow(ax, (x0 + 0.14, 0.855), (x0 + 0.14, yy + 0.165), tcol, lw=1.2, ms=10)
        yy -= 0.205
ax.text(0.5, 0.035, 'driving paradigm × iteration timing × updated object — the taxonomy is generative: 27 cells, each an identifiable research program',
        fontsize=8, color=DIM, ha='center')
save(fig, 'fig5_taxonomy')

# ============================ FIG 6: case map ============================
fig, ax = newfig(12.4, 7.6, 'Figure 6  |  Clinical Translation by Surgical Stage',
                 'representative studies with quantitative endpoints and CEBM evidence levels (full details in Table 10)', CYAN)
colnames = ['NEUROSURGERY & SPINE', 'ORTHOPEDIC', 'CARDIOTHORACIC']
rows = [
    ('PREOPERATIVE', CYAN, [
        ('VR planning + differentiable sim.\nTwin-S skull-base twin', 'evidence IV', CYAN_D),
        ('FEA screw-config optimization\nvertebroplasty twin', 'in silico, IV', CYAN_D),
        ('FSI valve sizing · ViV depth\nVT twins vs. invasive mapping', 'bench / IV', PURPLE)]),
    ('INTRAOPERATIVE', ORANGE, [
        ('iCT/iUS/AR guidance\nbrain shift TRE ≤17 mm', 'meta level III', ORANGE),
        ('navigation: perforation\n6% vs 15% · iCT −23 min', 'meta level III', ORANGE),
        ('ICG perfusion · echo-fluoro\nnephrectomy auto-registration', 'IV', PURPLE)]),
    ('POSTOPERATIVE', GREEN, [
        ('C5 palsy referral timing\nMoyamoya LDL risk model', 'IV', GREEN),
        ('FE healing twins · wearables\ncallus stiffness tracking', 'IV', GREEN),
        ('EP/hemodynamic follow-up\ntwin-adjusted therapy', 'IV', GREEN)]),
]
for j, cn in enumerate(colnames):
    chip(ax, 0.155 + j * 0.295, 0.860, 0.27, 0.048, cn, CYAN_D, tc=TXT, fs=8.5)
for i, (rn, rcol, cells) in enumerate(rows):
    yy = 0.60 - i * 0.265
    chip(ax, 0.025, yy + 0.06, 0.105, 0.09, rn, rcol, fs=7.2)
    for j, (txt, ev, col) in enumerate(cells):
        x = 0.155 + j * 0.295
        card(ax, x, yy, 0.27, 0.21, [], edge=col, fc=PANEL)
        ax.text(x + 0.135, yy + 0.135, txt, fontsize=8, color=TXT, ha='center', linespacing=1.5)
        chip(ax, x + 0.085, yy + 0.022, 0.10, 0.030, ev, col, tc=TXT if col != GREEN else '#0A1728', fs=6.8)
ax.text(0.5, 0.035, 'cell = representative methods (top) + key quantitative endpoint; badge = CEBM evidence level. Strongest domain (navigation) reaches level III only.',
        fontsize=8, color=DIM, ha='center')
save(fig, 'fig6_case_map')

# ============================ FIG 7: forest-style evidence ============================
fig = plt.figure(figsize=(12.0, 6.6))
axbg = fig.add_axes([0, 0, 1, 1]); axbg.axis('off')
axbg.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec='none'))
axbg.add_patch(Rectangle((0.018, 0.945), 0.006, 0.038, fc=GREEN, ec='none'))
axbg.text(0.032, 0.972, 'Figure 7  |  Meta-Analytic Evidence: Navigated vs. Conventional Pedicle Screws',
          fontsize=14, color=TXT, fontweight='bold', va='top')
axbg.text(0.032, 0.935, 'the strongest evidence domain in surgical twinning — and it is only CEBM level III',
          fontsize=9, color=SUB, va='top')

ax1 = fig.add_axes([0.07, 0.16, 0.40, 0.70], facecolor=PANEL)
ax2 = fig.add_axes([0.57, 0.16, 0.40, 0.70], facecolor=PANEL)
for a in (ax1, ax2):
    for sp in a.spines.values():
        sp.set_color(EDGE)
    a.tick_params(colors=SUB, labelsize=8)

def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z**2 / n
    ctr = (p + z**2 / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return p, ctr - half, ctr + half

arms = [('Navigated (Shin 2012)', 0.06, 4814, CYAN), ('Conventional (Shin 2012)', 0.15, 3725, RED)]
for i, (lab, p, n, c) in enumerate(arms):
    k = round(p * n)
    ph, lo, hi = wilson(k, n)
    ax1.errorbar(ph * 100, 1 - i, xerr=[[(ph - lo) * 100], [(hi - ph) * 100]],
                 fmt='s', color=c, ecolor=c, capsize=5, markersize=9, lw=2, mec=BG)
    ax1.text(hi * 100 + 0.8, 1 - i, f'{p*100:.0f}%  (n={n:,})', va='center', fontsize=8.5, color=TXT)
ax1.set_yticks([1, 0]); ax1.set_yticklabels([a[0] for a in arms], fontsize=8.5, color=TXT)
ax1.set_xlabel('pedicle perforation risk (%, 95% CI)', fontsize=8.5, color=SUB)
ax1.set_xlim(0, 20); ax1.set_ylim(-0.7, 1.7)
ax1.set_title('A. perforation risk (recomputed from reported aggregates)\n20 studies · 8,539 screws', fontsize=9, color=TXT)
ax1.text(6.2, 0.42, 'RR 0.39 (95% CI 0.32–0.47)\nfavors navigation', fontsize=8.5, color=GREEN,
         bbox=dict(boxstyle='round', fc=PANEL2, ec=GREEN, lw=1.0))

labels = ['Shin 2012\nperforation', 'Papalia 2024\nunacceptable placement']
nav = [6.0, 3.8]; conv = [15.0, 5.8]
x = np.arange(2); w = 0.30
b1 = ax2.bar(x - w / 2, nav, w, color=CYAN, label='Navigated')
b2 = ax2.bar(x + w / 2, conv, w, color=RED, label='Conventional')
for xi, v in zip(x - w / 2, nav): ax2.text(xi, v + 0.4, f'{v:.1f}%', ha='center', fontsize=8.5, color=CYAN, fontweight='bold')
for xi, v in zip(x + w / 2, conv): ax2.text(xi, v + 0.4, f'{v:.1f}%', ha='center', fontsize=8.5, color=RED, fontweight='bold')
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8.5, color=TXT)
ax2.set_ylabel('rate (%)', fontsize=8.5, color=SUB); ax2.set_ylim(0, 21)
ax2.legend(fontsize=8, frameon=False, labelcolor=TXT, loc='upper right')
ax2.set_title('B. independent meta-analytic estimates\n(Papalia: 30 studies · 24,600 screws)', fontsize=9, color=TXT)
ax2.text(0.5, 17.5, 'Staartjes 2018 (37 studies, 7,095 pts):\npost-op revision navigated OR 0.3 (95% CI 0.2–0.5), P<0.001',
         fontsize=7.5, color=GREEN, ha='center',
         bbox=dict(boxstyle='round', fc=PANEL2, ec=GREEN, lw=1.0))
fig.savefig(os.path.join(OUT, 'fig7_forest.png'), dpi=300, facecolor=BG, bbox_inches='tight')
fig.savefig(os.path.join(PDFDIR, 'fig7_forest.pdf'), facecolor=BG, bbox_inches='tight')
print('saved fig7_forest')
print('FIG4-7 DONE')
