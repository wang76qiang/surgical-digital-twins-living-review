# -*- coding: utf-8 -*-
"""fig4-7 in NPG style: framework, taxonomy, case map, forest plot."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.scratch'))
from nature_style import *

# ============================ FIG 4: unified framework ============================
fig, ax = newfig(7.2, 5.0)

panel(ax, 0.03, 0.56, 0.94, 0.30, 'PHYSICAL DOMAIN', fc=PANEL_BG, ec=BORDER)
panel(ax, 0.03, 0.10, 0.94, 0.38, 'VIRTUAL DOMAIN  (the twin)', fc=WHITE, ec=NPG_LAV, lw=1.0)
phys = [('Patient', 'anatomy · physiology\npathology', NPG_BLUE),
        ('Imaging & sensors', 'CT · MRI · US · iCT/iUS\nwearables · EHR', NPG_BLUE),
        ('Surgery', 'intervention a$_t$\n(executed plan)', NPG_SALMON)]
pw = 0.26
for i, (t, sub, col) in enumerate(phys):
    x = 0.06 + i * 0.31
    card(ax, x, 0.615, pw, 0.185, t, sub, accent=col, title_fs=9, sub_fs=6.8)
chain = [('Segmentation &\nreconstruction', 'nnU-Net · MedSAM\nTotalSegmentator', NPG_BLUE),
         ('Fusion &\nregistration', 'VoxelMorph\nSynthMorph', NPG_BLUE),
         ('Functional\nmodeling', 'FEBio · SimVascular\nopenCARP · TumorTwin', NPG_LAV),
         ('Virtual\niteration', 'bilevel optimization\nunder uncertainty', NPG_SALMON),
         ('Clinical\ndecision', 'ranked plans + UQ\nhuman-in-the-loop', NPG_GREEN)]
cw = 0.168
for i, (t, sub, col) in enumerate(chain):
    x = 0.045 + i * 0.185
    card(ax, x, 0.145, cw, 0.235, t, sub, accent=col, title_fs=8, sub_fs=6.2)
    if i < 4:
        arrow(ax, (x + cw + 0.0035, 0.262), (x + cw + 0.0165, 0.262), INK, lw=1.0, ms=9)
# couplings
arrow(ax, (0.50, 0.615), (0.24, 0.385), NPG_NAVY, lw=1.2)
ax.text(0.36, 0.50, 'observation y$_t$', fontsize=7, color=NPG_NAVY, rotation=42)
arrow(ax, (0.87, 0.385), (0.81, 0.615), NPG_RED, lw=1.2)
ax.text(0.87, 0.523, 'decision\nexecuted a$_t$', fontsize=7, color=NPG_RED, va='center')
arrow(ax, (0.85, 0.615), (0.58, 0.385), NPG_GREEN, lw=1.2, ls='--')
ax.text(0.70, 0.523, 'post-op observations\n(data assimilation)', fontsize=7, color=NPG_GREEN, ha='right', va='center')
for x, lab, col in [(0.17, 'PREOPERATIVE', NPG_BLUE), (0.50, 'INTRAOPERATIVE', NPG_SALMON), (0.83, 'POSTOPERATIVE', NPG_GREEN)]:
    ax.text(x, 0.925, lab, fontsize=7.5, color=col, ha='center', fontweight='bold')
save(fig, 'fig4_framework')

# ============================ FIG 5: taxonomy ============================
fig, ax = newfig(7.2, 5.2)

cols = [
    ('Driving paradigm', NPG_BLUE, [
        ('Physics-driven', 'FEA · CFD · FSI · EP\nFEBio · SimVascular · openCARP', NPG_BLUE),
        ('Data-driven', 'ML outcome predictors\nrisk & recovery models', NPG_SALMON),
        ('Hybrid (physics-informed ML)', 'PINNs · neural operators\nVR-differentiable simulation', NPG_LAV)]),
    ('Iteration timing', NPG_GREEN, [
        ('Offline', 'preoperative\nplan optimization', NPG_BLUE),
        ('Online', 'intraoperative re-planning\nseconds-scale', NPG_SALMON),
        ('Longitudinal', 'postoperative healing\nrehabilitation · surveillance', NPG_GREEN)]),
    ('Updated object', NPG_LAV, [
        ('Structure', 'anatomy deforms / grows\nregistration · growth models', NPG_BLUE),
        ('Parameters', 'materials · boundary conditions\nBayesian / EnKF assimilation', NPG_LAV),
        ('Policy', 'the intervention itself\nBayesian opt. · RL · MPC', NPG_GREEN)]),
]
for ci, (title, tcol, leaves) in enumerate(cols):
    x0 = 0.04 + ci * 0.325
    ax.add_patch(Rectangle((x0, 0.885), 0.28, 0.004, fc=tcol, ec='none'))
    ax.text(x0 + 0.14, 0.905, title, fontsize=9, color=INK, ha='center', fontweight='bold')
    yy = 0.645
    for name, sub, col in leaves:
        tfs = 7.5 if name.startswith('Hybrid') else 8.5
        card(ax, x0, yy, 0.28, 0.185, name, sub, accent=col, title_fs=tfs, sub_fs=6.5)
        arrow(ax, (x0 + 0.14, 0.885), (x0 + 0.14, yy + 0.19), BORDER, lw=0.8, ms=8)
        yy -= 0.235
save(fig, 'fig5_taxonomy')

# ============================ FIG 6: case map ============================
fig, ax = newfig(7.2, 5.6)

colnames = ['NEUROSURGERY & SPINE', 'ORTHOPEDIC', 'CARDIOTHORACIC']
rows = [
    ('PREOP', NPG_BLUE, [
        ('VR planning + differentiable sim.\nTwin-S skull-base twin', 'IV', NPG_BLUE),
        ('FEA screw-config optimization\nvertebroplasty twin', 'in silico · IV', NPG_BLUE),
        ('FSI valve sizing · ViV depth\nVT twins vs. invasive mapping', 'bench · IV', NPG_LAV)]),
    ('INTRAOP', NPG_SALMON, [
        ('iCT/iUS/AR guidance\nbrain shift TRE ≤17 mm', 'meta · III', NPG_SALMON),
        ('navigation: perforation\n6% vs 15% · iCT −23 min', 'meta · III', NPG_SALMON),
        ('ICG perfusion · echo-fluoro\nnephrectomy auto-registration', 'IV', NPG_LAV)]),
    ('POSTOP', NPG_GREEN, [
        ('C5 palsy referral timing\nMoyamoya LDL risk model', 'IV', NPG_GREEN),
        ('FE healing twins · wearables\ncallus stiffness tracking', 'IV', NPG_GREEN),
        ('EP/hemodynamic follow-up\ntwin-adjusted therapy', 'IV', NPG_GREEN)]),
]
for j, cn in enumerate(colnames):
    ax.text(0.2825 + j * 0.285, 0.925, cn, fontsize=7.5, color=INK, ha='center', fontweight='bold')
    ax.add_patch(Rectangle((0.155 + j * 0.285, 0.908), 0.255, 0.003, fc=INK, ec='none'))
for i, (rn, rcol, cells) in enumerate(rows):
    yy = 0.615 - i * 0.29
    ax.add_patch(FancyBboxPatch((0.025, yy + 0.075), 0.105, 0.09, boxstyle='round,pad=0.004',
                                fc=rcol, ec='none'))
    ax.text(0.0775, yy + 0.12, rn, fontsize=7, color=WHITE, ha='center', va='center', fontweight='bold')
    for j, (txt, ev, col) in enumerate(cells):
        x = 0.155 + j * 0.285
        card(ax, x, yy, 0.255, 0.24, None, None, accent=col)
        ax.text(x + 0.1275, yy + 0.155, txt, fontsize=7, color=INK, ha='center', linespacing=1.5)
        ax.add_patch(FancyBboxPatch((x + 0.0875, yy + 0.025), 0.08, 0.032, boxstyle='round,pad=0.003',
                                    fc=PANEL_BG, ec=col, lw=0.8))
        ax.text(x + 0.1275, yy + 0.041, ev, fontsize=6, color=col, ha='center', va='center', fontweight='bold')
save(fig, 'fig6_case_map')

# ============================ FIG 7: forest-style evidence ============================
fig = plt.figure(figsize=(7.2, 4.6))
axbg = fig.add_axes([0, 0, 1, 1]); axbg.axis('off')
ax1 = fig.add_axes([0.10, 0.17, 0.37, 0.70])
ax2 = fig.add_axes([0.62, 0.17, 0.34, 0.70])
for a, letter in [(ax1, 'a'), (ax2, 'b')]:
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
    a.spines['left'].set_color(BORDER); a.spines['bottom'].set_color(BORDER)
    a.tick_params(colors=INK, labelsize=7)
    a.text(-0.14, 1.04, letter, transform=a.transAxes, fontsize=10, fontweight='bold', color=INK)

def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z**2 / n
    ctr = (p + z**2 / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return p, ctr - half, ctr + half

arms = [('Navigated (Shin 2012)', 0.06, 4814, NPG_BLUE), ('Conventional (Shin 2012)', 0.15, 3725, NPG_RED)]
for i, (lab, p, n, c) in enumerate(arms):
    k = round(p * n)
    ph, lo, hi = wilson(k, n)
    ax1.errorbar(ph * 100, 1 - i, xerr=[[(ph - lo) * 100], [(hi - ph) * 100]],
                 fmt='s', color=c, ecolor=c, capsize=3, markersize=6, lw=1.4, mec='white')
    ax1.text(hi * 100 + 0.8, 1 - i, f'{p*100:.0f}%  (n={n:,})', va='center', fontsize=7, color=INK)
ax1.set_yticks([1, 0]); ax1.set_yticklabels([a[0] for a in arms], fontsize=7.5)
ax1.set_xlabel('pedicle perforation risk (%, 95% CI)', fontsize=7.5)
ax1.set_xlim(0, 20); ax1.set_ylim(-0.7, 1.7)
ax1.set_title('perforation risk (20 studies · 8,539 screws)', fontsize=7.5, color=INK)
ax1.text(6.4, 0.45, 'RR 0.39 (95% CI 0.32–0.47)\nfavors navigation', fontsize=7, color=NPG_GREEN,
         bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=NPG_GREEN, lw=0.8))
labels = ['Shin 2012\nperforation', 'Papalia 2024\nunacceptable placement']
nav = [6.0, 3.8]; conv = [15.0, 5.8]
x = np.arange(2); w = 0.30
ax2.bar(x - w / 2, nav, w, color=NPG_BLUE, label='Navigated')
ax2.bar(x + w / 2, conv, w, color=NPG_RED, label='Conventional')
for xi, v in zip(x - w / 2, nav): ax2.text(xi, v + 0.4, f'{v:.1f}%', ha='center', fontsize=7, color=NPG_BLUE, fontweight='bold')
for xi, v in zip(x + w / 2, conv): ax2.text(xi, v + 0.4, f'{v:.1f}%', ha='center', fontsize=7, color=NPG_RED, fontweight='bold')
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=7)
ax2.set_ylabel('rate (%)', fontsize=7.5); ax2.set_ylim(0, 23.5)
ax2.legend(fontsize=7, frameon=False, loc='upper right')
ax2.set_title('independent estimates', fontsize=7.5, color=INK)
ax2.text(0.5, 17.9, 'Staartjes 2018 (37 studies, 7,095 pts):\npost-op revision navigated\nOR 0.3 (95% CI 0.2–0.5), P<0.001',
         fontsize=6.3, color=NPG_GREEN, ha='center',
         bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=NPG_GREEN, lw=0.8))
fig.savefig(os.path.join(OUT, 'fig7_forest.png'), dpi=600, facecolor='white', bbox_inches='tight')
fig.savefig(os.path.join(PDFDIR, 'fig7_forest.pdf'), facecolor='white', bbox_inches='tight')
print('saved fig7_forest')
print('FIG4-7 NPG DONE')
