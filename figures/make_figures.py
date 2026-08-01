import os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Wedge
import matplotlib.patheffects as pe

OUT = r'E:\综述\外科\投稿版本\新建文件夹\figures_V2'
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.linewidth': 0.8})
C = {'blue': '#0072B2', 'orange': '#E69F00', 'green': '#009E73', 'red': '#D55E00',
     'purple': '#CC79A7', 'sky': '#56B4E9', 'yellow': '#F0E442', 'grey': '#666666'}

def box(ax, x, y, w, h, text, fc, fs=8, ec='black', tc='black', lw=1.0, rounding=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.008,rounding_size={rounding}",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, color=tc, wrap=True)

def arrow(ax, x1, y1, x2, y2, color='black', lw=1.4, style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=13,
                                 color=color, lw=lw, linestyle=ls))

def newfig(w=7.2, h=4.0):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    return fig, ax

PDFDIR = os.path.join(OUT, 'pdf')
os.makedirs(PDFDIR, exist_ok=True)
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(PDFDIR, name.replace('.png', '.pdf')), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('saved', name)

# ---------------- Figure 1: closed-loop control diagram ----------------
fig, ax = newfig(7.2, 4.2)
box(ax, 0.03, 0.42, 0.16, 0.22, 'PATIENT\n(physical plant)\nstate s$_t$', '#F5F5F5', fs=9)
box(ax, 0.27, 0.70, 0.20, 0.20, 'Imaging & biosensing\ny$_t$ = H(s$_t$) + v$_t$', C['sky'], fs=8)
box(ax, 0.27, 0.10, 0.20, 0.20, 'Data assimilation\nposterior p(s,θ|y$_{1:t}$)', C['sky'], fs=8)
box(ax, 0.55, 0.40, 0.20, 0.22, 'DIGITAL TWIN\nforward model f$_θ$\nŝ$_{t+1}$ = f$_θ$(s$_t$, a)', C['blue'], fs=8, tc='white')
box(ax, 0.82, 0.40, 0.16, 0.22, 'Intervention\noptimization\na* = argmin E[L]', C['green'], fs=8)
arrow(ax, 0.19, 0.58, 0.27, 0.80)                     # patient -> imaging
arrow(ax, 0.37, 0.70, 0.37, 0.32)                     # imaging -> assimilation
arrow(ax, 0.47, 0.20, 0.60, 0.40)                     # assimilation -> twin
arrow(ax, 0.75, 0.51, 0.82, 0.51)                     # twin -> optimizer
arrow(ax, 0.90, 0.40, 0.90, 0.06, color=C['green'])   # optimizer down
arrow(ax, 0.90, 0.06, 0.11, 0.06, color=C['green'])   # to patient level
arrow(ax, 0.11, 0.06, 0.11, 0.42, color=C['green'])   # apply to patient
ax.text(0.50, 0.005, 'execute intervention a$_t$ on patient → new observations', fontsize=8, ha='center', color=C['green'])
ax.text(0.50, 0.96, 'Preoperative (days–hours)  •  Intraoperative (minutes–seconds)  •  Postoperative (weeks–months)',
        fontsize=8, ha='center', color=C['grey'])
ax.set_ylim(-0.03, 1.0)
save(fig, 'fig1_closed_loop.png')

# ---------------- Figure 2: PRISMA flow (real executed search) ----------------
fig, ax = newfig(7.2, 5.0)
bx = dict(fs=8)
box(ax, 0.05, 0.80, 0.40, 0.16, '''Records identified (n = 619)
PubMed 539 · arXiv 80
(executed 29 Jul 2026)''', C['sky'], **bx)
box(ax, 0.05, 0.56, 0.40, 0.14, '''Records after duplicates removed
(n = 615)''', C['sky'], **bx)
box(ax, 0.05, 0.34, 0.40, 0.14, '''Records screened (title/abstract)
(n = 615)''', '#EAF3FA', **bx)
box(ax, 0.05, 0.12, 0.40, 0.14, '''Records assessed for eligibility
(n = 482)''', '#EAF3FA', **bx)
box(ax, 0.58, 0.80, 0.38, 0.12, '''Duplicate records removed
(n = 4)''', '#F2F2F2', **bx)
box(ax, 0.58, 0.54, 0.38, 0.14, '''Records excluded by documented rules
(n = 133): non-medical domain 127
off-topic 6''', '#F2F2F2', fs=7.5)
box(ax, 0.58, 0.10, 0.38, 0.16, '''Corpus completed by structured
hand-searching (MedIA, IEEE TMI,
MICCAI) and citation chasing (131)
+ methodological anchors (4)''', '#F2F2F2', fs=7.5)
arrow(ax, 0.25, 0.80, 0.25, 0.72); arrow(ax, 0.25, 0.56, 0.25, 0.50); arrow(ax, 0.25, 0.34, 0.25, 0.28)
arrow(ax, 0.45, 0.88, 0.58, 0.86); arrow(ax, 0.45, 0.41, 0.58, 0.61); arrow(ax, 0.45, 0.17, 0.58, 0.16)
box(ax, 0.05, -0.10, 0.40, 0.12, '''Studies included in review (n = 149):
14 reproducible search · 131 hand-search
/ citation chasing · 4 anchors''', C['green'], tc='white', fs=7.5)
arrow(ax, 0.25, 0.12, 0.25, 0.02)
ax.set_ylim(-0.14, 1.0)
save(fig, 'fig2_prisma.png')

# ---------------- Figure 3: image-to-simulation workflow (real imaging data) ----------------
import matplotlib.image as mpimg
IMG = 'C:\\Users\\fhj\\.scratch\\fig3_images'
fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15], hspace=0.06)
ax_img = fig.add_subplot(gs[0]); ax_img.axis("off")
ax_img.set_xlim(0, 1); ax_img.set_ylim(0, 1)
modality_imgs = [
    ("CT (thorax)", "CT-Thorax-5.0-B70f-Lungs.jpg", "CC BY-SA 4.0"),
    ("MRI (glioblastoma)", "AFIP-00405589-Glioblastoma-Radiology.jpg", "public domain"),
    ("Cine MRI (4-chamber)", "cardiac_mri_frame.png", "CC BY-SA 4.0"),
    ("US elastography", "Transient Elastography (Fibroscan) of the Liver.jpg", "CC BY-SA 4.0"),
]
xw = 0.235
for i, (label, fn, lic) in enumerate(modality_imgs):
    x0 = 0.012 + i * (xw + 0.017)
    im = mpimg.imread(os.path.join(IMG, fn))
    inset = ax_img.inset_axes([x0, 0.10, xw, 0.78])
    inset.imshow(im, cmap="gray", aspect="auto")
    inset.set_xticks([]); inset.set_yticks([])
    for sp in inset.spines.values(): sp.set_edgecolor("black"); sp.set_linewidth(0.8)
    ax_img.text(x0 + xw/2, 0.015, label, ha="center", fontsize=7.5)
ax_img.text(0.012, 0.93, "Real imaging inputs (Wikimedia Commons, licenses as noted; credits in repository)", fontsize=7, color="#666666")
ax = fig.add_subplot(gs[1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
stages = [
    ("Segmentation\nnnU-Net \u00b7 MedSAM\nTotalSegmentator", C["sky"]),
    ("Geometry & mesh\nsurface/volume\nFE-quality mesh", C["sky"]),
    ("Physics solvers\nFEBio \u00b7 SimVascular\nopenCARP", C["blue"]),
    ("Acceleration\nPOD · neural ops.\n(378±280×)", C["purple"]),
    ("Decision\nranked plans +\nuncertainty", C["green"]),
]
w = 0.17; x = 0.02
for i, (txt, fc) in enumerate(stages):
    tc = "white" if fc in (C["blue"], C["green"], C["purple"]) else "black"
    box(ax, x, 0.42, w, 0.40, txt, fc, fs=7.2, tc=tc)
    if i < 4:
        arrow(ax, x + w + 0.008, 0.62, x + w + 0.028, 0.62)
    x += w + 0.03
ax.text(0.02, 0.22, "Typical budgets: segmentation seconds (GPU; VoxelMorph 0.37\u20130.55 s) \u00b7 meshing minutes \u00b7 full-order solve minutes\u2013hours (ANTs CPU 9,059 s) \u00b7 surrogate query milliseconds\u2013seconds",
        fontsize=7, color=C["grey"])
ax.text(0.02, 0.08, "Uncertainty entry points: segmentation surface error \u2192 mesh/geometry error \u2192 parameter & boundary-condition error \u2192 prediction interval",
        fontsize=7, color=C["red"])
save(fig, "fig3_workflow.png")

# ---------------- Figure 4: unified framework (two lanes) ----------------
fig, ax = newfig(7.2, 4.4)
ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.96, 0.42, boxstyle='round,pad=0.01', fc='#FBFBFB', ec=C['grey'], lw=0.8))
ax.add_patch(FancyBboxPatch((0.02, 0.03), 0.96, 0.48, boxstyle='round,pad=0.01', fc='#F7FBFD', ec=C['grey'], lw=0.8))
ax.text(0.04, 0.93, 'PHYSICAL DOMAIN', fontsize=9, fontweight='bold', color=C['grey'])
ax.text(0.04, 0.47, 'VIRTUAL DOMAIN (digital twin)', fontsize=9, fontweight='bold', color=C['blue'])
box(ax, 0.06, 0.62, 0.16, 0.22, 'Patient\nanatomy · physiology\npathology', '#F0F0F0', fs=8)
box(ax, 0.40, 0.62, 0.20, 0.22, 'Imaging & sensors\nCT · MRI · US · iCT/iUS\nwearables · EHR', '#F0F0F0', fs=7.5)
box(ax, 0.74, 0.62, 0.20, 0.22, 'Surgery\nintervention a$_t$\n(executed plan)', '#F0F0F0', fs=8)
lane = [
    ('Segmentation &\nreconstruction\nnnU-Net · TotalSeg.', C['sky']),
    ('Fusion &\nregistration\nVoxelMorph\nSynthMorph', C['sky']),
    ('Functional\nmodeling\nFEBio · SimVascular', C['blue']),
    ('Virtual\niteration\nbilevel optimization', C['green']),
    ('Clinical\ndecision\nplans + UQ', C['orange']),
]
x = 0.05
for i, (txt, fc) in enumerate(lane):
    tc = 'white' if fc in (C['blue'], C['green']) else 'black'
    box(ax, x, 0.09, 0.165, 0.28, txt, fc, fs=7.0, tc=tc)
    if i < 4:
        arrow(ax, x + 0.17, 0.23, x + 0.195, 0.23)
    x += 0.19
arrow(ax, 0.50, 0.62, 0.30, 0.40)   # imaging -> segmentation (down)
arrow(ax, 0.135, 0.09, 0.84, 0.62, color=C['green'], ls='--')  # decision -> surgery
ax.text(0.42, 0.50, 'decision executed', fontsize=7, color=C['green'], rotation=27)
arrow(ax, 0.84, 0.62, 0.62, 0.40, color=C['red'], ls='--')     # surgery -> functional model update
ax.text(0.635, 0.545, 'post-op observations\n(data assimilation)', fontsize=7, color=C['red'])
save(fig, 'fig4_framework.png')

# ---------------- Figure 5: taxonomy ----------------
fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.4))
for ax in axes:
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
titles = ['Driving paradigm', 'Iteration timing', 'Updated object']
roots = ['Simulation engine', 'Time constant', 'Loop target']
leaves = [
    [('Physics-driven\nFEA · CFD · FSI · EP', C['blue']), ('Data-driven\nML outcome models', C['orange']), ('Hybrid\nPINN · neural operators\ndifferentiable sim.', C['purple'])],
    [('Offline (pre-op)\nplan optimization', C['sky']), ('Online (intra-op)\nre-planning in seconds', C['green']), ('Longitudinal (post-op)\nhealing · rehabilitation', C['yellow'])],
    [('Structure\nregistration · growth', C['sky']), ('Parameters\nBayesian · EnKF\nassimilation', C['blue']), ('Policy\nBayesian opt. · RL\nMPC', C['green'])],
]
for ax, title, root, lv in zip(axes, titles, roots, leaves):
    ax.set_title(title, fontsize=10, fontweight='bold')
    box(ax, 0.15, 0.82, 0.7, 0.13, root, '#EFEFEF', fs=9)
    ys = [0.55, 0.30, 0.05]
    for (txt, fc), y in zip(lv, ys):
        tc = 'white' if fc in (C['blue'], C['green'], C['purple']) else 'black'
        box(ax, 0.05, y, 0.9, 0.17, txt, fc, fs=8, tc=tc)
        arrow(ax, 0.5, 0.82, 0.5, y + 0.17, lw=1.0)
save(fig, 'fig5_taxonomy.png')

# ---------------- Figure 6: case map ----------------
fig, ax = newfig(7.2, 4.4)
cols = ['Neurosurgery', 'Orthopedic surgery', 'Cardiothoracic surgery']
rows = ['Preoperative', 'Intraoperative', 'Postoperative']
cells = [
    [('VR planning; differentiable sim.\n(evidence IV)', 'Tumor twins; DTI constraints'),
     ('FEA screw-config optimization\n(in silico, IV)', 'Objective dominates optimum'),
     ('FSI valve sizing; ViV depth\n(bench, IV)', 'Gradients vs. position')],
    [('iCT/iUS/AR guidance\nbrain shift ≤2 cm (review)', 'MR–iUS deformable reg.'),
     ('Navigation: perf. 6% vs 15%\n(meta, level III)', 'iCT: −23 min, P=0.02'),
     ('ICG perfusion; echo-fluoro\nco-registration (IV)', 'Structural-heart navigation')],
    [('C5 palsy referral timing (IV)', 'Neuro recovery prediction'),
     ('FE healing twins; wearables (IV)', 'Callus stiffness trends'),
     ('EP/hemodynamic follow-up (IV)', 'Twin-adjusted therapy')],
]
for j, cname in enumerate(cols):
    ax.text(0.20 + j * 0.27, 0.96, cname, ha='center', fontsize=9, fontweight='bold')
for i, rname in enumerate(rows):
    ax.text(0.015, 0.74 - i * 0.30, rname, fontsize=9, fontweight='bold', rotation=90, va='center')
colors = [[C['sky'], C['blue'], C['purple']], [C['green'], C['green'], C['green']], [C['orange'], C['orange'], C['orange']]]
for i in range(3):
    for j in range(3):
        fc = colors[i][j]
        tc = 'white' if fc in (C['blue'], C['green'], C['purple']) else 'black'
        box(ax, 0.09 + j * 0.30, 0.62 - i * 0.30, 0.26, 0.24, cells[i][j][0] + '\n— ' + cells[i][j][1], fc, fs=6.8, tc=tc)
ax.text(0.09, 0.01, 'Cell content: representative methods — key quantitative endpoint (CEBM evidence level). Full details in Table 9.',
        fontsize=7.5, color=C['grey'])
save(fig, 'fig6_case_map.png')

# ---------------- Figure 7: forest-style evidence plot ----------------
from scipy import stats
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), gridspec_kw={'width_ratios': [1.15, 1]})
# Panel A: perforation rates with Wilson CIs
def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z**2 / n
    ctr = (p + z**2 / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return p, ctr - half, ctr + half
arms = [('Navigated\n(Shin 2012)', 0.06, 4814, C['blue']), ('Conventional\n(Shin 2012)', 0.15, 3725, C['red'])]
for i, (lab, p, n, c) in enumerate(arms):
    k = round(p * n)
    ph, lo, hi = wilson(k, n)
    ax1.errorbar(ph * 100, 1 - i, xerr=[[(ph - lo) * 100], [(hi - ph) * 100]],
                 fmt='s', color=c, capsize=4, markersize=8, lw=1.5)
    ax1.text(hi * 100 + 0.8, 1 - i, f'{p*100:.0f}%  (n={n:,})', va='center', fontsize=8)
ax1.set_yticks([1, 0]); ax1.set_yticklabels([a[0] for a in arms], fontsize=8)
ax1.set_xlabel('Pedicle perforation risk (%, 95% CI)', fontsize=8)
ax1.set_xlim(0, 20); ax1.set_ylim(-0.6, 1.6)
ax1.set_title('A. Perforation risk (recomputed from\nreported aggregates; 20 studies, 8,539 screws)', fontsize=8)
ax1.text(7.3, 0.5, 'RR 0.39 (95% CI 0.32–0.47)\nfavors navigation', fontsize=8,
         bbox=dict(boxstyle='round', fc='#F0F0F0', ec=C['grey']))
# Panel B: independent meta-analyses pooled estimates
labels = ['Shin 2012\nperforation', 'Papalia 2024\nunacceptable placement']
nav = [6.0, 3.8]; conv = [15.0, 5.8]
x = np.arange(2); w = 0.32
ax2.bar(x - w/2, nav, w, color=C['blue'], label='Navigated')
ax2.bar(x + w/2, conv, w, color=C['red'], label='Conventional')
for xi, v in zip(x - w/2, nav): ax2.text(xi, v + 0.3, f'{v:.1f}%', ha='center', fontsize=8)
for xi, v in zip(x + w/2, conv): ax2.text(xi, v + 0.3, f'{v:.1f}%', ha='center', fontsize=8)
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8)
ax2.set_ylabel('Rate (%)', fontsize=8); ax2.set_ylim(0, 18)
ax2.legend(fontsize=8, frameon=False)
ax2.set_title('B. Independent meta-analytic estimates\n(Papalia: 30 studies, 24,600 screws)', fontsize=8)
ax2.text(0.5, 16.6, 'Staartjes 2018 (37 studies, 7,095 pts): post-op revision\nnavigated OR 0.3 (95% CI 0.2–0.5), P<0.001', fontsize=7, ha='center', bbox=dict(boxstyle='round', fc='#F0F0F0', ec='#666666'))
for a in (ax1, ax2):
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
fig.tight_layout()
save(fig, 'fig7_forest.png')

# ---------------- Figure 8: VVUQ pyramid ----------------
fig, ax = newfig(7.2, 4.4)
tiers = [
    ('Clinical\nvalidation', C['red'], 0.34),
    ('Physics validation\n(bench · in vivo)', C['orange'], 0.55),
    ('Geometric validation\n(Dice · HD95 · endpoint TRE)', C['sky'], 0.76),
    ('Verification\n(code · calculation · regression testing)', C['blue'], 0.97),
]
y = 0.78
for txt, fc, wfrac in tiers:
    w = wfrac * 0.62; x0 = 0.32 - w / 2
    w2 = (wfrac - 0.18) * 0.62; x1 = 0.32 - w2 / 2
    ax.add_patch(Polygon([(x0, y), (x0 + w, y), (x1 + w2, y + 0.20), (x1, y + 0.20)],
                          closed=True, fc=fc, ec='black', lw=0.8, alpha=0.92))
    ax.text(0.32, y + 0.10, txt, ha='center', va='center', fontsize=7.5,
            color='white' if fc in (C['blue'], C['red']) else 'black')
    y -= 0.21
ax.text(0.32, 0.99, 'ASME V&V 40 credibility hierarchy', ha='center', fontsize=9, fontweight='bold')
unc = ['Segmentation error', 'Registration error', 'Parameter uncertainty', 'Model-form uncertainty', 'Surrogate error']
box(ax, 0.68, 0.30, 0.30, 0.52, 'Uncertainty quantification\n(spans all levels):\n\n' + '\n'.join('· ' + u for u in unc) + '\n\nApplicability assessment\n(context of use)', '#F5F5F5', fs=7.5)
arrow(ax, 0.68, 0.56, 0.60, 0.56, color=C['grey'], ls='--')
save(fig, 'fig8_vvuq.png')

# ---------------- Figure 9: radar chart ----------------
fig = plt.figure(figsize=(6.4, 4.6))
ax = fig.add_subplot(111, polar=True)
criteria = ['Per-query\ncompute cost', 'Data\nrequirement', 'Physical fidelity\n/ extrapolation', 'Interpretability', 'Validation\nmaturity']
data = {
    'Physics-driven': ([2, 5, 5, 4, 4], C['blue']),
    'Data-driven': ([5, 2, 2, 2, 3], C['orange']),
    'Hybrid (physics-informed ML)': ([4, 3, 4, 3, 2], C['green']),
}
ang = np.linspace(0, 2 * np.pi, len(criteria), endpoint=False).tolist()
ang += ang[:1]
for name, (vals, c) in data.items():
    v = vals + vals[:1]
    ax.plot(ang, v, color=c, lw=2, label=name)
    ax.fill(ang, v, color=c, alpha=0.12)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(criteria, fontsize=8)
ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=7)
ax.set_ylim(0, 5)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=8, frameon=False)
save(fig, 'fig9_radar.png')

# ---------------- Figure 10: roadmap ----------------
fig, ax = newfig(7.2, 4.0)
tracks = [
    ('Benchmarks & reporting standards', [(0.05, 0.30, 'Surgical-twin\nbenchmark (Sec. 6.5)'), (0.45, 0.80, 'Journal reporting\nguideline adopted')], C['blue']),
    ('Neural-operator real-time simulation', [(0.10, 0.45, 'ms-level EP match\nto openCARP, <1 s'), (0.60, 0.95, 'Intra-op re-simulation\nat navigation speed')], C['purple']),
    ('Federated multi-center validation', [(0.15, 0.55, 'Cross-site twin\ncalibration studies'), (0.70, 1.0, 'Federated twin\nvalidation network')], C['sky']),
    ('Regulatory-grade in silico trials', [(0.20, 0.60, 'V&V 40 credibility\ntemplates in use'), (0.75, 1.0, 'CM&S evidence in\ndevice submissions')], C['red']),
    ('Human–twin immersive interfaces', [(0.05, 0.35, 'Interface-mediated\nplan iteration trials'), (0.55, 0.85, 'Prospective evidence\nof changed plans')], C['green']),
]
y = 0.86
for name, miles, c in tracks:
    ax.text(0.01, y + 0.05, name, fontsize=8, fontweight='bold')
    ax.plot([0.05, 0.98], [y, y], color=c, lw=2, alpha=0.5)
    for x0, x1, lab in miles:
        ax.add_patch(FancyBboxPatch((x0, y - 0.045), x1 - x0, 0.09, boxstyle='round,pad=0.006',
                                    fc=c, ec='black', lw=0.7, alpha=0.9))
        ax.text((x0 + x1) / 2, y, lab, ha='center', va='center', fontsize=6.6, color='white')
    y -= 0.175
for year, x in zip(['2025', '2026', '2027', '2028', '2029', '2030'], np.linspace(0.05, 0.98, 6)):
    ax.text(x, 0.02, year, fontsize=8, ha='center', color=C['grey'])
save(fig, 'fig10_roadmap.png')

print('ALL FIGURES DONE')
