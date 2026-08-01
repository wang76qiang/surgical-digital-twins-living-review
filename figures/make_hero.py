import os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Polygon, Rectangle
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

OUT = r'E:\综述\外科\投稿版本\新建文件夹\figures_V2'
IMG = os.path.expanduser(r'~/.scratch/fig3_images')
os.makedirs(OUT, exist_ok=True)

# ---------------- palette (deep-navy holographic, colorblind-aware) ----------------
BG      = '#0A1728'
PANEL   = '#0F2438'
EDGE    = '#1E4E70'
CYAN    = '#39C6F3'
CYAN_D  = '#1E8FBF'
ORANGE  = '#F2A93B'
GREEN   = '#3BDC97'
PURPLE  = '#B57EDC'
RED     = '#F26D6D'
TXT     = '#E8F4FB'
SUB     = '#9DC4DA'
DIM     = '#5E87A0'

plt.rcParams.update({'font.family': 'DejaVu Sans'})

def glow_line(ax, xs, ys, color, lw=2.2, n=3, alpha=0.5):
    for i in range(n, 0, -1):
        ax.plot(xs, ys, color=color, lw=lw * (1 + i * 1.6), alpha=alpha / (i * 1.8),
                solid_capstyle='round', zorder=2)
    ax.plot(xs, ys, color=color, lw=lw, zorder=3, solid_capstyle='round')

def panel(ax, x, y, w, h, title=None, edge=EDGE, fc=PANEL, title_color=SUB, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.006,rounding_size=0.012',
                                fc=fc, ec=edge, lw=lw, zorder=2))
    if title:
        ax.text(x + 0.012, y + h - 0.016, title, fontsize=8.5, color=title_color,
                fontweight='bold', va='top', zorder=4)

def chip(ax, x, y, w, h, text, color, fs=7.5, tc=None, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.004,rounding_size=0.008',
                                fc=color, ec='none', zorder=3))
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs,
            color=tc or '#0A1728', fontweight='bold', zorder=4)

fig = plt.figure(figsize=(12.4, 12.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec='none', zorder=0))
# subtle radial glow at center
for r_, a_ in zip(np.linspace(0.46, 0.10, 18), np.linspace(0.015, 0.10, 18)):
    ax.add_patch(Circle((0.5, 0.60), r_, fc='#12304A', ec='none', alpha=a_, zorder=1))

# ============================ TITLE ============================
ax.text(0.5, 0.982, 'THE SURGICAL DIGITAL TWIN', ha='center', fontsize=21, color=TXT,
        fontweight='bold', zorder=5)
ax.text(0.5, 0.956, 'From Pixels to Decisions — Patient-Specific Modeling, Virtual Iteration, and Closed-Loop Optimization',
        ha='center', fontsize=10, color=CYAN, zorder=5)
ax.plot([0.30, 0.70], [0.943, 0.943], color=EDGE, lw=1.0)

# ============================ CENTRAL LOOP ============================
cx, cy, R = 0.5, 0.63, 0.185
arcs = [  # (start_deg, end_deg, color, label, sub)
    (115, 245, CYAN,   'PREOPERATIVE', 'days–hours\nplan optimization'),
    (245, 335, ORANGE, 'INTRAOPERATIVE', 'minutes–seconds\nonline updating'),
    (335, 475, GREEN,  'POSTOPERATIVE', 'weeks–months\nlongitudinal iteration'),
]
for a0, a1, col, lab, sub in arcs:
    th = np.linspace(np.deg2rad(a0), np.deg2rad(a1), 100)
    glow_line(ax, cx + R * np.cos(th), cy + R * np.sin(th), col, lw=3.2)
    # arrowhead at arc end (clockwise)
    t_mid_arrow = np.deg2rad(a1 - 4)
    t_end_arrow = np.deg2rad(a1 - 0.5)
    ax.add_patch(FancyArrowPatch((cx + R * np.cos(t_mid_arrow), cy + R * np.sin(t_mid_arrow)),
                                 (cx + R * np.cos(t_end_arrow), cy + R * np.sin(t_end_arrow)),
                                 arrowstyle='-|>', mutation_scale=26, color=col, lw=3.2, zorder=5))
    mid = np.deg2rad((a0 + a1) / 2)
    lx, ly = cx + (R + 0.043) * np.cos(mid), cy + (R + 0.043) * np.sin(mid)
    if lab == 'PREOPERATIVE':
        lx += 0.028
    ax.text(lx, ly, lab, ha='center', va='center', fontsize=8.2, color=col, fontweight='bold', zorder=6)
    sx, sy = cx + (R + 0.043) * np.cos(mid), cy + (R + 0.043) * np.sin(mid) - 0.024
    ax.text(sx, sy, sub, ha='center', va='center', fontsize=6.4, color=SUB, zorder=4)

# center panel: the mathematical core
panel(ax, cx - 0.145, cy - 0.115, 0.29, 0.23, edge=CYAN_D, fc='#0D2033')
ax.text(cx, cy + 0.092, 'VIRTUAL ITERATION', ha='center', fontsize=11.5, color=CYAN, fontweight='bold')
ax.text(cx, cy + 0.062, 'the computational core', ha='center', fontsize=7.5, color=SUB)
ax.text(cx, cy + 0.028, 'a* = argmin$_{a\\in A}$  E$_{p(s,\\theta|y)}$ [ L( f$_\\theta$(s, a), a ) ]',
        ha='center', fontsize=10.5, color=TXT)
ax.text(cx, cy + 0.000, 's.t.  g$_i$(a) ≤ 0   (clinical constraints)', ha='center', fontsize=7.8, color=ORANGE)
ax.plot([cx - 0.11, cx + 0.11], [cy - 0.018, cy - 0.018], color=EDGE, lw=0.8)
ax.text(cx, cy - 0.040, 'θ$_{t+1}$ = argmin$_\\theta$  d( f$_\\theta$(s$_t$, a$_t$), s$_{t+1}^{obs}$ )',
        ha='center', fontsize=9.5, color=GREEN)
ax.text(cx, cy - 0.066, 'bilevel loop: optimize the plan · recalibrate the model',
        ha='center', fontsize=7.2, color=SUB)
ax.text(cx, cy - 0.094, 'surgeon in the loop — ranked plans + uncertainty',
        ha='center', fontsize=7.2, color=PURPLE)

# ============================ LEFT: PHYSICAL WORLD ============================
LX, LY, LW, LH = 0.025, 0.44, 0.225, 0.42
panel(ax, LX, LY, LW, LH, 'PHYSICAL WORLD', edge=CYAN_D)
ax.text(LX + LW / 2, LY + LH - 0.045, 'patient · sensors · OR', fontsize=8, ha='center', color=SUB)
# patient glyph (supine on table)
px, py = LX + 0.052, LY + LH - 0.105
ax.add_patch(FancyBboxPatch((px - 0.038, py - 0.018), 0.118, 0.012, boxstyle='round,pad=0.002',
                            fc='#1A3A55', ec=CYAN_D, lw=0.8, zorder=3))
ax.add_patch(Circle((px - 0.014, py + 0.008), 0.011, fc=CYAN, ec='none', zorder=4))
ax.add_patch(FancyBboxPatch((px - 0.002, py - 0.001), 0.058, 0.017, boxstyle='round,pad=0.004,rounding_size=0.008',
                            fc=CYAN, ec='none', zorder=4))
ax.text(px + 0.10, py - 0.002, 'state s$_t$', fontsize=8, color=CYAN, ha='left')
# real modality images 2x2
mods = [('CT-Thorax-5.0-B70f-Lungs.jpg', 'CT'),
        ('AFIP-00405589-Glioblastoma-Radiology.jpg', 'MRI'),
        ('cardiac_mri_frame.png', 'cine MRI'),
        ('Transient Elastography (Fibroscan) of the Liver.jpg', 'US')]
ix0, iy0, iw, gap = LX + 0.016, LY + 0.105, 0.088, 0.012
for i, (fn, lab) in enumerate(mods):
    xx = ix0 + (i % 2) * (iw + gap)
    yy = iy0 + (1 - i // 2) * (iw * 0.78 + gap)
    inset = ax.inset_axes([xx, yy, iw, iw * 0.78])
    inset.imshow(mpimg.imread(os.path.join(IMG, fn)), cmap='gray', aspect='auto')
    inset.set_xticks([]); inset.set_yticks([])
    for sp in inset.spines.values():
        sp.set_edgecolor(CYAN_D); sp.set_linewidth(1.0)
    ax.text(xx + iw / 2, yy - 0.012, lab, fontsize=7, color=SUB, ha='center')
ax.text(LX + LW / 2, LY + 0.030, 'observation  y$_t$ = H(s$_t$) + v$_t$', fontsize=8.5,
        color=CYAN, ha='center', fontweight='bold')
# arrow physical -> loop
arrow = FancyArrowPatch((LX + LW + 0.005, cy + 0.05), (cx - R - 0.012, cy + 0.05),
                        arrowstyle='-|>', mutation_scale=22, color=CYAN, lw=2.4, zorder=4)
ax.add_patch(arrow)

# ============================ RIGHT: VIRTUAL WORLD ============================
RX, RY, RW, RH = 0.75, 0.44, 0.225, 0.42
panel(ax, RX, RY, RW, RH, 'VIRTUAL WORLD  (the twin)', edge=PURPLE)
ax.text(RX + RW / 2, RY + RH - 0.045, 'geometry · physics · policy', fontsize=8, ha='center', color=SUB)
# wireframe "organ" mesh (warped sphere)
u = np.linspace(0, 2 * np.pi, 26); v = np.linspace(0, np.pi, 14)
uu, vv = np.meshgrid(u, v)
xs = np.sin(vv) * np.cos(uu); ys_ = np.cos(vv); zs = np.sin(vv) * np.sin(uu)
warp = 1 + 0.28 * ys_
mx, my = xs * warp, zs * 0.82
ox, oy, sc = RX + RW / 2, RY + RH - 0.185, 0.052
for j in range(0, len(v), 2):
    ax.plot(ox + sc * mx[j, :], oy + sc * my[j, :], color=CYAN, lw=0.55, alpha=0.75, zorder=3)
for j in range(0, len(u), 2):
    ax.plot(ox + sc * mx[:, j], oy + sc * my[:, j], color=CYAN, lw=0.55, alpha=0.75, zorder=3)
ax.text(ox, oy - 0.068, 'patient-specific mesh', fontsize=7, color=SUB, ha='center')
# solver chips
chip(ax, RX + 0.016, RY + 0.135, 0.062, 0.028, 'FEBio', CYAN_D, tc=TXT, fs=7.5)
chip(ax, RX + 0.084, RY + 0.135, 0.075, 0.028, 'SimVascular', CYAN_D, tc=TXT, fs=7.0)
chip(ax, RX + 0.165, RY + 0.135, 0.062, 0.028, 'openCARP', CYAN_D, tc=TXT, fs=7.0)
chip(ax, RX + 0.016, RY + 0.099, 0.108, 0.028, 'nnU-Net · MedSAM', EDGE, tc=TXT, fs=7.0)
chip(ax, RX + 0.130, RY + 0.099, 0.097, 0.028, 'POD 378±280×', PURPLE, tc='#0A1728', fs=7.0)
ax.text(RX + RW / 2, RY + 0.062, 'forward model  ŝ$_{t+1}$ = f$_\\theta$(s$_t$, a)',
        fontsize=8.5, color=PURPLE, ha='center', fontweight='bold')
ax.text(RX + RW / 2, RY + 0.030, 'biomechanics · hemodynamics · electrophysiology',
        fontsize=6.8, color=SUB, ha='center')
# arrow loop -> virtual & virtual -> loop (bidirectional)
ax.add_patch(FancyArrowPatch((cx + R + 0.012, cy + 0.05), (RX - 0.005, cy + 0.05),
                             arrowstyle='-|>', mutation_scale=22, color=PURPLE, lw=2.4, zorder=4))
ax.add_patch(FancyArrowPatch((RX - 0.005, cy - 0.02), (cx + R + 0.012, cy - 0.02),
                             arrowstyle='-|>', mutation_scale=22, color=GREEN, lw=2.4, zorder=4))
ax.text(cx + R + 0.052, cy - 0.055, 'assimilation', fontsize=6.6, color=GREEN, ha='left')

# ============================ BOTTOM: three pillar cards ============================
BY, BH = 0.035, 0.335
# ---- Card 1: EVIDENCE ----
c1x, c1w = 0.025, 0.30
panel(ax, c1x, BY, c1w, BH, 'EVIDENCE  (162-study corpus)', edge=CYAN_D)
ev = [
    ('RR 0.39', 'pedicle perforation, navigated vs.\nconventional (8,539 screws)', CYAN),
    ('0.943', 'TotalSegmentator mean Dice,\n104 structures (1,204 CTs)', GREEN),
    ('5.9→2.9 mm', 'brain-shift mTRE after deformable\nMR–iUS registration (13 cases)', ORANGE),
    ('378±280×', 'POD calibration speed-up,\nCCC 0.986 vs. full model', PURPLE),
]
ey = BY + BH - 0.058
for val, txt, col in ev:
    ax.text(c1x + 0.014, ey, val, fontsize=9.8, color=col, fontweight='bold', va='center')
    ax.text(c1x + 0.104, ey, txt, fontsize=6.6, color=SUB, va='center')
    ey -= 0.052
ax.text(c1x + 0.014, ey - 0.004, 'CEBM: strongest domain reaches level III only', fontsize=6.8,
        color=RED, va='center')

# ---- Card 2: CREDIBILITY (VVUQ) ----
c2x, c2w = 0.345, 0.30
panel(ax, c2x, BY, c2w, BH, 'CREDIBILITY  (ASME V&V 40)', edge=ORANGE)
tiers = [('Clinical validation', RED, 0.34), ('Physics validation', ORANGE, 0.52),
         ('Geometric validation', CYAN, 0.70), ('Verification', CYAN_D, 0.88)]
ty = BY + 0.205
for name, col, wf in tiers:
    w_ = wf * 0.16; x0 = c2x + 0.105 - w_ / 2
    w2_ = (wf - 0.14) * 0.16; x1 = c2x + 0.105 - w2_ / 2
    ax.add_patch(Polygon([(x0, ty), (x0 + w_, ty), (x1 + w2_, ty + 0.042), (x1, ty + 0.042)],
                         closed=True, fc=col, ec=BG, lw=0.8, alpha=0.95, zorder=3))
    ax.text(c2x + 0.105, ty + 0.021, name, ha='center', va='center', fontsize=6.4,
            color=TXT if col in (RED, CYAN_D) else '#0A1728', zorder=4, fontweight='bold')
    ty -= 0.047
ax.text(c2x + 0.215, BY + 0.155, 'UQ spans\nall levels:\n· segmentation\n· registration\n· parameters\n· model form\n· surrogate',
        fontsize=6.2, color=SUB, va='top')
ax.text(c2x + 0.014, BY + 0.040, 'credibility for the context of use —', fontsize=6.8, color=ORANGE)
ax.text(c2x + 0.014, BY + 0.018, 'risk-informed (V&V 40) · FDA CM&S 2023', fontsize=6.8, color=ORANGE)

# ---- Card 3: MATURITY ----
c3x, c3w = 0.665, 0.31
panel(ax, c3x, BY, c3w, BH, 'MATURITY  (where the field really is)', edge=GREEN)
lv = [('L1', 'static model'), ('L2', 'dynamic visualization'), ('L3', 'predictive\nsimulation'),
      ('L4', 'closed-loop\noptimization'), ('L5', 'autonomous\ntwin')]
lx0, lw_ = c3x + 0.016, 0.054
for i, (lab, name) in enumerate(lv):
    col = [DIM, CYAN_D, CYAN, ORANGE, '#23435C'][i]
    tc = TXT if i in (0, 1, 4) else '#0A1728'
    chip(ax, lx0 + i * (lw_ + 0.004), BY + 0.185, lw_, 0.034, lab, col, tc=tc, fs=8)
    ax.text(lx0 + i * (lw_ + 0.004) + lw_ / 2, BY + 0.168, name, fontsize=5.6, color=SUB, ha='center', va='top')
marks = [
    (1, 'deployed\n(Brainlab · Mako)', CYAN),
    (2, 'FFRct — only RCT-grade\npredictive twin (PLATFORM)', CYAN_D),
    (3, 'research demos\n(EP twins · differentiable sim.)', ORANGE),
    (4, 'none — no regulatory path\n(continuous learning)', RED),
]
my = BY + 0.130
for idx, txt, col in marks:
    ax.add_patch(Circle((lx0 + idx * (lw_ + 0.004) + lw_ / 2, my + 0.008), 0.006, fc=col, ec='none', zorder=4))
    ax.text(lx0 + 0.002, my, f'L{idx+1}', fontsize=7.5, color=col, fontweight='bold', va='center')
    ax.text(lx0 + 0.028, my, txt, fontsize=6.1, color=SUB, va='center')
    my -= 0.042

# ============================ FOOTER ============================
ax.plot([0.06, 0.94], [0.016, 0.016], color=EDGE, lw=0.8)
ax.text(0.5, 0.007, 'Image → Model → Simulation → Optimization → Decision → Observation — the loop closes at three time scales, and credibility decides how far it goes.',
        ha='center', fontsize=7.6, color=DIM)

png = os.path.join(OUT, 'graphical_abstract.png')
pdf = os.path.join(OUT, 'pdf', 'graphical_abstract.pdf')
fig.savefig(png, dpi=300, facecolor=BG, bbox_inches='tight')
fig.savefig(pdf, facecolor=BG, bbox_inches='tight')
print('saved', png)
print('saved', pdf)
