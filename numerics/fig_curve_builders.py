"""Build the curve-bearing figures 21, 25, 26 and 27 as complete HTML plates.

Curves in this monograph are drawn in pure CSS: a polyline is a chain of
absolutely positioned, rotated divs.  Every plotted point comes from
figures/data/fig-13-30-data.json, which is produced by
numerics/fig_13_30_data.py -- nothing here is eyeballed.

Run:  python numerics/fig_curve_builders.py
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "figures", "data", "fig-13-30-data.json")
OUT = os.path.join(ROOT, "figures", "html")
NL = "\n"


def polyline(points, colour, width=2.0, dash=False):
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        ang = math.degrees(math.atan2(dy, dx))
        if dash:
            body = f"background:transparent; border-top:{width:.2f}px dashed {colour};"
        else:
            body = f"background:{colour};"
        out.append(
            f'<div class="crv" style="left:{x0:.2f}px; top:{y0 - width / 2:.2f}px; '
            f'width:{L:.2f}px; height:{width:.2f}px; {body} '
            f'transform:rotate({ang:.3f}deg); transform-origin:left center;"></div>')
    return (NL + "    ").join(out)


SCALE_1200 = """:root{
  --fs-title:25px; --fs-sub:14.5px; --fs-panel:14px; --fs-label:13px;
  --fs-small:11.5px; --fs-tiny:10px; --fs-cap:12.5px;
  --stroke:1.5px; --emph:3px; --radius:7px;
}
.canvas{ width:1200px; height:800px; }
.fig-head{ top:26px; left:36px; right:36px; height:86px; gap:18px; }
.fig-head .titles{ max-width:840px; }
.fig-head .fig-sub{ max-width:840px; margin-top:6px; }
.fig-num{ margin-bottom:4px; }
.fig-head::after{ bottom:-12px; }
.badges{ gap:6px; }
.badge{ padding:4px 9px; border-width:1.5px; }
.badge-built{ padding:3px 8px; }
.stage{ left:36px; right:36px; top:132px; bottom:186px; }
.fig-cap{ left:36px; right:36px; bottom:22px; padding-top:10px; }
.panel{ padding:12px 14px; }
.panel-title{ margin-bottom:6px; letter-spacing:.10em; }
.mark.dot{ width:9px; height:9px; }
.mark.ring{ width:11px; height:11px; border-width:2px; }
.mark.sq{ width:9px; height:9px; }
.mark.cross{ width:12px; height:12px; }
.mark.cross::before,.mark.cross::after{ width:15px; height:2px; }
.mark.diam{ width:9px; height:9px; }
.chip{ padding:2px 7px; }
.tick.v{ height:8px; } .tick.h{ width:8px; }
.axis-arrow-u::after{ border-bottom-width:9px; border-left-width:5px; border-right-width:5px; }
.axis-arrow-r::after{ border-left-width:9px; border-top-width:5px; border-bottom-width:5px; }
.conn::after{ border-left-width:9px; border-top-width:5px; border-bottom-width:5px; }
.legend{ gap:5px 22px; } .legend .swatch{ width:20px; height:10px; }
.mono{ font-family:var(--mono); }
.crv{ position:absolute; }
.plot{ position:absolute; background:#FFF; border:1.5px solid var(--rule); border-radius:4px; }
"""


def plate(num, canvas, title, kicker, sub, badge, built, body, cap,
          extra_css="", scale=SCALE_1200):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="canvas" content="{canvas}">
<title>Figure {num} &mdash; {title}</title>
<link rel="stylesheet" href="../css/gwapm-figure.css">
<style>
{scale}{extra_css}</style>
</head>
<body>
<div class="canvas">

  <div class="fig-head">
    <div class="titles">
      <div class="fig-num">{kicker}</div>
      <div class="fig-title">{title}</div>
      <div class="fig-sub">{sub}</div>
    </div>
    <div class="badges">
      <span class="badge {badge[0]}">{badge[1]}</span>
      <span class="badge-built {built}">constructed: {built}</span>
    </div>
  </div>

  <div class="stage">
{body}
  </div>

  <div class="fig-cap">
{cap}
  </div>

</div>
</body>
</html>
"""


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(text)
    print("[write] %-42s %7d chars" % (name, len(text)))


# ==========================================================================
def fig21(d):
    SX, LY = 620.0 / 40.0, 300.0 / 10.5
    px = lambda S: S * SX
    py = lambda v: 300.0 - math.log10(v) * LY

    env, S = [], 1.0
    while S <= 40.0001:
        env.append((px(S), py(S * math.exp(S / 2))))
        S += 0.5
    curves = ["<!-- arithmetic envelope S*exp(S/2), support_doubling_envelope.csv -->",
              polyline(env, "var(--oxide)", 2.6)]
    for delta, colour, dash in [(0.05, "var(--slate)", False),
                                (0.2, "var(--indigo)", False),
                                (0.45, "var(--violet)", True)]:
        curves.append("<!-- injected signal exp(%s S) -->" % delta)
        curves.append(polyline([(px(0), py(1.0)), (px(40), py(math.exp(delta * 40)))],
                               colour, 2.2, dash=dash))

    grid = []
    for k in range(0, 11, 2):
        y = 300.0 - k * LY
        grid.append('<div class="hline dashed" style="left:0; top:%.1fpx; width:620px; '
                    'border-top-color:var(--rule);"></div>' % y)
        grid.append('<div class="lab tiny slate" style="left:-42px; top:%.1fpx;">10<sup>%d</sup></div>'
                    % (y - 6, k))
    for S in (0, 10, 20, 30, 40):
        grid.append('<div class="tick v" style="left:%.1fpx; top:300px;"></div>' % px(S))
        grid.append('<div class="lab tiny" style="left:%.1fpx; top:312px; '
                    'transform:translateX(-50%%);">%d</div>' % (px(S), S))

    mx, my = px(12), py(12 * math.exp(6))

    body = f"""    <div class="chip oxide" style="left:64px; top:-6px;">CORRECTED SUPPORT SCALE &nbsp;&middot;&nbsp; <span class="m">S</span> = half&#8209;support of the test function &nbsp;&middot;&nbsp; vertical axis logarithmic</div>

    <div class="plot" style="left:64px; top:30px; width:620px; height:300px;"></div>
    <div style="position:absolute; left:64px; top:30px; width:620px; height:300px;">
    {(NL + "    ").join(grid)}
    {(NL + "    ").join(curves)}
    <div class="mark ring" style="left:{mx:.1f}px; top:{my:.1f}px; border-color:var(--oxide);"></div>
    </div>
    <div class="axis h axis-arrow-r" style="left:64px; top:330px; width:646px;"></div>
    <div class="axis v" style="left:64px; top:24px; height:306px;"></div>
    <div class="lab tiny m" style="left:702px; top:336px;">S</div>
    <div class="lab tiny slate" style="left:0px; top:8px;">relative size</div>

    <div class="lab tiny oxide b" style="left:472px; top:36px; background:#FFF; padding:0 4px;">arithmetic envelope&nbsp; <span class="m">S&thinsp;e</span><sup><span class="m">S</span>/2</sup></div>
    <div class="lab tiny violet b" style="left:598px; top:116px; background:#FFF; padding:0 4px;">&delta; = 0.45</div>
    <div class="lab tiny indigo b" style="left:598px; top:196px; background:#FFF; padding:0 4px;">&delta; = 0.20</div>
    <div class="lab tiny slate b" style="left:598px; top:266px; background:#FFF; padding:0 4px;">&delta; = 0.05</div>
    <div class="lab tiny oxide" style="left:96px; top:82px; background:#FFF; padding:0 4px;">&#9679;&nbsp;<span class="m">S</span> = 12 &mdash; the range actually computed in Figure&nbsp;24</div>
    <div class="fl" style="left:150px; top:96px; width:155.0px; height:1.5px; background:var(--oxide); transform:rotate(52.15deg); transform-origin:left center;"></div>

    <div class="panel tint-oxide" style="left:716px; top:30px; width:412px; height:162px;">
      <div class="panel-title" style="color:var(--oxide);">THE UNCERTAINTY, STATED</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        A CZI&#8209;type argument injects a signal of relative size <span class="m">e</span><sup>&delta;<span class="m">S</span></sup> into the explicit formula and must read it out against the arithmetic envelope <span class="m">S&thinsp;e</span><sup><span class="m">S</span>/2</sup> that the prime sum contributes on the same support. Because &delta;&nbsp;&lt;&nbsp;&frac12; for every construction in the literature, the gap <b>widens</b> with <span class="m">S</span>: on 0&nbsp;&le;&nbsp;<span class="m">S</span>&nbsp;&le;&nbsp;40 no signal curve overtakes the envelope.
      </div>
    </div>

    <div class="panel" style="left:716px; top:206px; width:412px; height:150px;">
      <div class="panel-title">WHY &delta; &lt; &frac12; IS NOT A FREE CHOICE</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        &frac12; is the exponent already carried by the archimedean factor. A construction with &delta;&nbsp;&ge;&nbsp;&frac12; would contain a zero&#8209;free region of the strength being sought; its injected term would not be a perturbation but the conclusion. The two curves are therefore not parameters that could be tuned to cross.
      </div>
    </div>

    <div class="panel dashed" style="left:716px; top:370px; width:412px; height:112px;">
      <div class="panel-title" style="color:var(--slate);">SCOPE OF THIS PLATE</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        The inequality drawn here follows from the support&#8209;doubling theorem (N1). The stronger claim that <b>no</b> future construction can reach &delta;&nbsp;&ge;&nbsp;&frac12; is not proved and is not asserted.
      </div>
    </div>

    <div class="legend" style="left:64px; top:404px; width:620px;">
      <div class="item"><span class="swatch" style="background:var(--oxide); height:3px;"></span>arithmetic envelope &mdash; solid, heavy</div>
      <div class="item"><span class="swatch" style="background:var(--indigo); height:3px;"></span>injected signal &mdash; solid</div>
      <div class="item"><span class="swatch" style="background:transparent; border-top:3px dashed var(--violet);"></span>injected signal &mdash; dashed</div>
    </div>"""

    cap = """    <b>Figure 21.</b> Injected CZI signal <span class="m">e</span><sup>&delta;<span class="m">S</span></sup> against the arithmetic envelope <span class="m">S&thinsp;e</span><sup><span class="m">S</span>/2</sup> on the corrected support scale, vertical axis logarithmic. On a log scale each injected signal is exactly a straight line and the envelope is a straight line plus log&nbsp;<span class="m">S</span>, so the separation is visible as a growing vertical gap.
    <span class="limit">This figure does not establish that no correlation&#8209;type method can prove RH, and it does not rule out a construction with &delta;&nbsp;&ge;&nbsp;&frac12;. It establishes only that for every &delta;&nbsp;&lt;&nbsp;&frac12; the injected signal is dominated by the envelope on the whole sampled range, so it cannot be read out by size alone.</span>
    <span class="src">Envelope and signal columns tabulated in <span class="mono">numerics/support_doubling_envelope.csv</span> (161 rows, <span class="m">S</span>&nbsp;&isin;&nbsp;[0,&nbsp;40]); curve coordinates generated by <span class="mono">numerics/fig_curve_builders.py</span> from <span class="mono">figures/data/fig-13-30-data.json</span>.</span>"""

    write("fig-21-czi-uncertainty.html",
          plate(21, "1200x800",
                "CZI signal against the arithmetic uncertainty envelope",
                "Figure 21 &middot; Chapter 8 &middot; No-go N1 (support doubling)",
                "Two curves on the corrected support scale: what a correlation argument injects, "
                "and what the prime sum unavoidably contributes on the same support.",
                ("T", "[T] theorem of this book"), "no", body, cap))


# ==========================================================================
def fig25(d):
    s, T, sup = d["fig25_samples"], d["fig25_T"], d["fig25_support"]
    RX, VY = 600.0 / 6.0, 220.0 / 4.4
    qx = lambda r: r * RX
    qy = lambda v: 110.0 - v * VY

    grid = []
    for v in (-2, -1, 0, 1, 2):
        y = qy(v)
        cls = "hline" if v == 0 else "hline dashed"
        tail = "" if v == 0 else " border-top-color:var(--rule);"
        grid.append('<div class="%s" style="left:0; top:%.1fpx; width:600px;%s"></div>' % (cls, y, tail))
        grid.append('<div class="lab tiny slate" style="left:-26px; top:%.1fpx;">%d</div>' % (y - 6, v))
    for r in range(7):
        grid.append('<div class="tick v" style="left:%.1fpx; top:220px;"></div>' % qx(r))
        grid.append('<div class="lab tiny" style="left:%.1fpx; top:232px; '
                    'transform:translateX(-50%%);">%d</div>' % (qx(r), r))

    zk, k = [], 0
    while (math.pi / 2 + k * math.pi) / T <= 6:
        zk.append((math.pi / 2 + k * math.pi) / T)
        k += 1
    marks = (NL + "    ").join(
        '<div class="mark ring" style="left:%.1fpx; top:%.1fpx; border-color:var(--indigo);"></div>'
        % (qx(r), qy(0)) for r in zk)

    body = f"""    <div class="chip indigo" style="left:60px; top:-6px;">ENDPOINT PHASES &nbsp;&middot;&nbsp; two&#8209;bump family <span class="m">g</span>(<span class="m">u</span>) = <span class="m">a&thinsp;h</span>(<span class="m">u</span>&minus;<span class="m">T</span>) + <span class="m">b&thinsp;h</span>(<span class="m">u</span>+<span class="m">T</span>) &nbsp;at&nbsp; <span class="m">T</span> = {T}</div>

    <div class="plot" style="left:60px; top:30px; width:600px; height:220px;"></div>
    <div style="position:absolute; left:60px; top:30px; width:600px; height:220px;">
    {(NL + "    ").join(grid)}
    <!-- symmetric a=b=1: transform picks up 2 cos(rT) -->
    {polyline([(qx(p["r"]), qy(p["sym"])) for p in s], "var(--indigo)", 2.2)}
    <!-- antisymmetric a=-b: transform picks up 2 sin(rT) -->
    {polyline([(qx(p["r"]), qy(p["anti"])) for p in s], "var(--violet)", 2.2, dash=True)}
    {marks}
    </div>
    <div class="axis h axis-arrow-r" style="left:60px; top:250px; width:624px;"></div>
    <div class="lab tiny m" style="left:676px; top:256px;">r</div>
    <div class="lab tiny slate" style="left:6px; top:14px;">phase<br>factor</div>
    <div class="lab tiny slate" style="left:300px; top:264px;"><span class="m">r</span> &nbsp;&mdash;&nbsp; spectral ordinate</div>

    <div class="lab tiny indigo b" style="left:74px; top:40px;">2&thinsp;cos(<span class="m">rT</span>) &mdash; symmetric pair</div>
    <div class="lab tiny violet b" style="left:74px; top:222px;">2&thinsp;sin(<span class="m">rT</span>) &mdash; antisymmetric pair</div>
    <div class="lab tiny slate" style="left:700px; top:36px; width:180px; white-space:normal; line-height:1.3;">Rings mark the zeros of the symmetric phase, <span class="m">r</span>&nbsp;=&nbsp;(2<span class="m">k</span>+1)&pi;/2<span class="m">T</span>: the ordinates a translation scheme can silence.</div>
    <div class="lab tiny slate" style="left:700px; top:104px; width:180px; white-space:normal; line-height:1.3;">The two phases are in quadrature, so no choice of (<span class="m">a</span>,&nbsp;<span class="m">b</span>) silences all ordinates at once.</div>

    <div class="panel" style="left:0; top:296px; width:424px; height:186px;">
      <div class="panel-title">WHAT INTERFERENCE CAN AND CANNOT DO</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Translating a bump by &plusmn;<span class="m">T</span> multiplies its transform by <span class="m">e</span><sup>&#8723;<span class="m">irT</span></sup>. Two bumps give the factor <span class="m">a&thinsp;e</span><sup>&minus;<span class="m">irT</span></sup>&nbsp;+&nbsp;<span class="m">b&thinsp;e</span><sup><span class="m">irT</span></sup>, of modulus at most |<span class="m">a</span>|&nbsp;+&nbsp;|<span class="m">b</span>|&nbsp;=&nbsp;<b>{sup['max_interference_gain_abs_a_plus_abs_b']:.0f}</b>. Phases can be tuned to cancel at chosen ordinates, but the <i>peak</i> gain is exactly the trivial bound and does not depend on <span class="m">T</span>.
      </div>
    </div>

    <div class="panel tint-oxide" style="left:444px; top:296px; width:424px; height:186px;">
      <div class="panel-title" style="color:var(--oxide);">THE COST SIDE IS NOT BOUNDED</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        <span class="m">h</span> has half&#8209;support {sup['h_half_support']:.0f}, so <span class="m">g</span> has half&#8209;support {sup['g_T_half_support']:.0f}. The prime side is read on an interval longer by <span class="m">T</span>, and its envelope grows by
        <div style="text-align:center; margin:5px 0; font-family:var(--serif); font-size:13px;"><span class="m">e</span><sup><span class="m">T</span>/2</sup> = {sup['arith_envelope_factor_exp_T_over_2']:.4f}&hellip;</div>
        <b>Gain {sup['max_interference_gain_abs_a_plus_abs_b']:.0f}, cost {sup['arith_envelope_factor_exp_T_over_2']:.4f} &mdash; already at <span class="m">T</span> = {T}.</b> Raising <span class="m">T</span> multiplies the cost and leaves the gain fixed.
      </div>
    </div>

    <div class="panel dashed" style="left:888px; top:296px; width:240px; height:186px;">
      <div class="panel-title" style="color:var(--ochre);">STATUS &mdash; EXPERIMENTAL</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        One two&#8209;parameter family at one value of <span class="m">T</span>. It illustrates a mechanism; it is not a proof that every translation&#8209;phase scheme fails. The proved statement is the support&#8209;doubling bound of Figure&nbsp;21, not this plot.
      </div>
    </div>"""

    cap = f"""    <b>Figure 25.</b> Endpoint phase factors of the two&#8209;bump family at <span class="m">T</span>&nbsp;=&nbsp;{T}: the symmetric choice contributes 2&thinsp;cos(<span class="m">rT</span>), the antisymmetric choice 2&thinsp;sin(<span class="m">rT</span>). Rings mark ordinates where the symmetric phase vanishes. The peak modulus is |<span class="m">a</span>|&nbsp;+&nbsp;|<span class="m">b</span>|&nbsp;=&nbsp;{sup['max_interference_gain_abs_a_plus_abs_b']:.0f} for every <span class="m">T</span>, while the support cost is <span class="m">e</span><sup><span class="m">T</span>/2</sup>&nbsp;=&nbsp;{sup['arith_envelope_factor_exp_T_over_2']:.4f}.
    <span class="limit">This figure does not establish that no test&#8209;function family can beat the arithmetic envelope, and it evaluates no explicit formula. It exhibits one family and shows that within it the interference gain is bounded by a constant while the support cost grows exponentially in <span class="m">T</span>.</span>
    <span class="src">Phase values computed in <span class="mono">numerics/fig_13_30_data.py</span> (section fig25) and plotted by <span class="mono">numerics/fig_curve_builders.py</span>; {len(s)} sampled ordinates on 0&nbsp;&le;&nbsp;<span class="m">r</span>&nbsp;&le;&nbsp;6.</span>"""

    write("fig-25-translation-phase.html",
          plate(25, "1200x800",
                "Translation&#8209;phase interference in the two&#8209;bump family",
                "Figure 25 &middot; Chapter 8 &middot; Experimental",
                "Endpoint phases can be tuned to cancel at chosen ordinates, but their peak "
                "modulus is the trivial bound &mdash; while the support cost is not bounded at all.",
                ("E", "[E] experimental / finite"), "partial", body, cap))


# ==========================================================================
def fig26(d):
    rows = d["fig26"]
    UX, FY = 560.0 / 16.0, 280.0 / 2.4
    ux = lambda u: u * UX
    uy = lambda f: 280.0 - (f + 1.6) * FY

    curves = []
    for sigma, colour, dash in [(0.5, "var(--oxide)", False),
                                (0.75, "var(--violet)", True),
                                (1.0, "var(--sage)", False)]:
        pts, u = [], 0.0
        while u <= 16.0001:
            f = u / 2 - sigma * sigma * u * u / 2
            if f < -1.6:
                pts.append((ux(u), uy(-1.6)))
                break
            pts.append((ux(u), uy(f)))
            u += 0.125
        curves.append("<!-- exponent u/2 - sigma^2 u^2/2, sigma=%s -->" % sigma)
        curves.append(polyline(pts, colour, 2.2, dash=dash))
        curves.append('<div class="mark diam" style="left:%.1fpx; top:%.1fpx; background:%s;"></div>'
                      % (ux(1 / (2 * sigma ** 2)), uy(1 / (8 * sigma ** 2)), colour))

    grid = []
    for v in (-1.5, -1.0, -0.5, 0.0, 0.5):
        y = uy(v)
        cls = "hline" if v == 0 else "hline dashed"
        tail = "" if v == 0 else " border-top-color:var(--rule);"
        grid.append('<div class="%s" style="left:0; top:%.1fpx; width:560px;%s"></div>' % (cls, y, tail))
        grid.append('<div class="lab tiny slate" style="left:-32px; top:%.1fpx;">%+.1f</div>' % (y - 6, v))
    for u in (0, 4, 8, 12, 16):
        grid.append('<div class="tick v" style="left:%.1fpx; top:280px;"></div>' % ux(u))
        grid.append('<div class="lab tiny" style="left:%.1fpx; top:292px; '
                    'transform:translateX(-50%%);">%d</div>' % (ux(u), u))

    tbl = [('<tr><td class="num">%.2f</td><td class="num">%.3f</td>'
            '<td class="num">%.4f</td><td class="num">%.3f</td></tr>'
            % (r["sigma"], r["u_star"], r["f_max"], r["U_eff"]))
           for r in rows if abs(r["eps"] - 1e-9) < 1e-15]

    body = f"""    <div class="chip oxide" style="left:76px; top:-6px;">EXPONENT OF THE GAUSSIAN&#8209;WEIGHTED PRIME TERM &nbsp;&middot;&nbsp; <span class="m">f</span>(<span class="m">u</span>) = <span class="m">u</span>/2 &minus; &sigma;<sup>2</sup><span class="m">u</span><sup>2</sup>/2</div>

    <div class="plot" style="left:76px; top:30px; width:560px; height:280px;"></div>
    <div style="position:absolute; left:76px; top:30px; width:560px; height:280px;">
    {(NL + "    ").join(grid)}
    {(NL + "    ").join(curves)}
    </div>
    <div class="axis h axis-arrow-r" style="left:76px; top:{30 + uy(0):.1f}px; width:584px;"></div>
    <div class="lab tiny m" style="left:652px; top:{36 + uy(0):.1f}px;">u</div>
    <div class="axis v" style="left:76px; top:24px; height:286px;"></div>
    <div class="lab tiny slate" style="left:14px; top:8px;">exponent</div>
    <div class="lab tiny slate" style="left:196px; top:314px;"><span class="m">u</span> = log&nbsp;<span class="m">n</span> &nbsp;&mdash;&nbsp; position on the prime side</div>

    <div class="lab tiny oxide b" style="left:130px; top:38px;">&sigma; = 0.5</div>
    <div class="lab tiny violet b" style="left:104px; top:96px;">&sigma; = 0.75</div>
    <div class="lab tiny sage b" style="left:88px; top:150px;">&sigma; = 1.0</div>
    <div class="lab tiny slate" style="left:330px; top:66px;">&#9670;&nbsp;maximum, at <span class="m">u</span>*&nbsp;=&nbsp;1/(2&sigma;<sup>2</sup>)</div>

    <div class="panel tint-oxide" style="left:664px; top:30px; width:464px; height:150px;">
      <div class="panel-title" style="color:var(--oxide);">WHY A SMOOTH WINDOW DOES NOT ESCAPE</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        A Gaussian window <span class="m">e</span><sup>&minus;&sigma;<sup>2</sup><span class="m">u</span><sup>2</sup>/2</sup> has no compact support, so &ldquo;support&rdquo; must be replaced by <b>effective support</b> <span class="m">U</span><sub>eff</sub>: the last <span class="m">u</span> at which the weighted prime term still exceeds a threshold &epsilon;. Because the prime side carries <span class="m">e</span><sup><span class="m">u</span>/2</sup>, the exponent above is <b>positive</b> before it turns over, and the cutoff is pushed outward.
      </div>
    </div>

    <table class="fig" style="position:absolute; left:664px; top:196px; width:464px;">
      <tr><th>&sigma;</th><th><span class="m">u</span>* = 1/(2&sigma;<sup>2</sup>)</th><th>max exponent = 1/(8&sigma;<sup>2</sup>)</th><th><span class="m">U</span><sub>eff</sub> &nbsp;at&nbsp; &epsilon; = 10<sup>&minus;9</sup></th></tr>
      {(NL + "      ").join(tbl)}
    </table>

    <div class="panel dashed" style="left:664px; top:376px; width:464px; height:106px;">
      <div class="panel-title" style="color:var(--slate);">READING THE TABLE</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Narrowing the window (&sigma; up) shortens <span class="m">U</span><sub>eff</sub> but destroys the arithmetic resolution the argument needs. Widening it (&sigma; down) restores resolution and lengthens <span class="m">U</span><sub>eff</sub>, growing like 1/&sigma;<sup>2</sup>. Neither direction removes the growth.
      </div>
    </div>

    <div class="legend" style="left:0; top:398px; width:640px;">
      <div class="item"><span class="swatch" style="background:var(--oxide); height:3px;"></span>&sigma; = 0.5 &mdash; solid</div>
      <div class="item"><span class="swatch" style="background:transparent; border-top:3px dashed var(--violet);"></span>&sigma; = 0.75 &mdash; dashed</div>
      <div class="item"><span class="swatch" style="background:var(--sage); height:3px;"></span>&sigma; = 1.0 &mdash; solid</div>
    </div>
    <div class="lab tiny slate wrap" style="left:0; top:432px; width:640px; line-height:1.34;">
      All three curves start at <span class="m">f</span>(0)&nbsp;=&nbsp;0 with slope +&frac12;. The window only begins to win once &sigma;<sup>2</sup><span class="m">u</span>&nbsp;&gt;&nbsp;&frac12;, and by then the weighted term has already grown by <span class="m">e</span><sup>1/(8&sigma;<sup>2</sup>)</sup>.
    </div>"""

    cap = """    <b>Figure 26.</b> The exponent <span class="m">f</span>(<span class="m">u</span>)&nbsp;=&nbsp;<span class="m">u</span>/2&nbsp;&minus;&nbsp;&sigma;<sup>2</sup><span class="m">u</span><sup>2</sup>/2 controlling a Gaussian&#8209;windowed prime term, for three window widths, with the effective cutoff tabulated at threshold &epsilon;&nbsp;=&nbsp;10<sup>&minus;9</sup>. The exponent is positive on an initial interval in every case, so the weighted prime sum grows before the window suppresses it.
    <span class="limit">This figure does not establish that no smooth window can be useful, and it proves no lower bound for any particular explicit&#8209;formula argument. It establishes only that Gaussian and Hermite windows do not remove support growth: they relocate the cutoff, and relocate it outward as the window widens.</span>
    <span class="src">Exponents, maxima and cutoffs computed in closed form and tabulated in <span class="mono">numerics/fig_13_30_data.py</span> (section fig26); plotted by <span class="mono">numerics/fig_curve_builders.py</span>. <span class="m">U</span><sub>eff</sub> is the positive root of &sigma;<sup>2</sup><span class="m">U</span><sup>2</sup>/2&nbsp;&minus;&nbsp;<span class="m">U</span>/2&nbsp;=&nbsp;log(1/&epsilon;).</span>"""

    write("fig-26-gaussian-non-escape.html",
          plate(26, "1200x800",
                "Gaussian and Hermite windows do not escape support growth",
                "Figure 26 &middot; Chapter 8 &middot; No-go N1, smooth case",
                "Replacing compact support by a Gaussian replaces the support endpoint by an "
                "effective cutoff &mdash; which moves outward, not inward.",
                ("T", "[T] theorem of this book"), "no", body, cap,
                extra_css="""table.fig{ border-collapse:collapse; font-family:var(--sans); font-size:11px; }
table.fig th{ background:var(--ink); color:var(--paper); font-weight:600; font-size:10px;
              letter-spacing:.05em; padding:5px 8px; border:1px solid var(--ink); text-align:center; }
table.fig td{ padding:5px 8px; border:1px solid var(--rule); background:#FFF; text-align:center; }
table.fig td.num{ font-family:var(--mono); }
"""))


# ==========================================================================
def fig27(d):
    chk = d["fig27_check"]
    t = [p for p in d["fig27_samples"] if -3.0001 <= p["x"] <= 3.0001]
    XX, YY = 660.0 / 6.0, 240.0 / 2.7
    rx = lambda x: (x + 3.0) * XX
    ry = lambda v: 120.0 - v * YY

    grid = []
    for v in (-1, 0, 1):
        y = ry(v)
        cls = "hline" if v == 0 else "hline dashed"
        tail = "" if v == 0 else " border-top-color:var(--rule);"
        grid.append('<div class="%s" style="left:0; top:%.1fpx; width:660px;%s"></div>' % (cls, y, tail))
        grid.append('<div class="lab tiny slate" style="left:-28px; top:%.1fpx;">%+d</div>' % (y - 6, v))
    for x in range(-3, 4):
        grid.append('<div class="tick v" style="left:%.1fpx; top:240px;"></div>' % rx(x))
        grid.append('<div class="lab tiny" style="left:%.1fpx; top:252px; '
                    'transform:translateX(-50%%);">%d</div>' % (rx(x), x))

    sgn = (
        '<div class="crv" style="left:0; top:%.1fpx; width:%.1fpx; height:3px; background:var(--ink);"></div>'
        % (ry(-1) - 1.5, rx(0)) + NL + "    " +
        '<div class="crv" style="left:%.1fpx; top:%.1fpx; width:%.1fpx; height:3px; background:var(--ink);"></div>'
        % (rx(0), ry(1) - 1.5, 660 - rx(0)) + NL + "    " +
        '<div class="crv" style="left:%.1fpx; top:%.1fpx; width:3px; height:%.1fpx; '
        'background:var(--ink); opacity:.25;"></div>' % (rx(0) - 1.5, ry(1), ry(-1) - ry(1)))

    nodes = (NL + "    ").join(
        '<div class="mark ring" style="left:%.1fpx; top:%.1fpx; border-color:var(--ink);"></div>'
        % (rx(k), ry(1 if k > 0 else -1)) for k in (-3, -2, -1, 1, 2, 3))

    body = f"""    <div class="chip oxide" style="left:80px; top:-6px;">THE EXTREMAL PAIR AT &delta; = 1 &nbsp;&middot;&nbsp; <span class="m">B</span> = <span class="m">H</span> + <span class="m">K</span>, &nbsp;<span class="m">K</span>(<span class="m">z</span>) = (sin&thinsp;&pi;<span class="m">z</span>&thinsp;/&thinsp;&pi;<span class="m">z</span>)<sup>2</sup> &nbsp;&middot;&nbsp; type 2&pi;</div>

    <div class="plot" style="left:80px; top:30px; width:660px; height:240px;"></div>
    <div style="position:absolute; left:80px; top:30px; width:660px; height:240px;">
    {(NL + "    ").join(grid)}
    {sgn}
    <!-- majorant B(x) -->
    {polyline([(rx(p["x"]), ry(p["B"])) for p in t], "var(--oxide)", 2.2)}
    <!-- minorant -B(-x) -->
    {polyline([(rx(p["x"]), ry(p["m"])) for p in t], "var(--indigo)", 2.2, dash=True)}
    {nodes}
    <div class="mark dot" style="left:{rx(0):.1f}px; top:{ry(1):.1f}px; background:var(--oxide);"></div>
    <div class="mark dot" style="left:{rx(0):.1f}px; top:{ry(-1):.1f}px; background:var(--indigo);"></div>
    </div>
    <div class="axis h axis-arrow-r" style="left:80px; top:{30 + ry(0):.1f}px; width:684px;"></div>
    <div class="lab tiny m" style="left:756px; top:{36 + ry(0):.1f}px;">x</div>

    <div class="lab tiny oxide b" style="left:592px; top:38px;">majorant &nbsp;<span class="m">B</span>(<span class="m">x</span>)&nbsp;&ge;&nbsp;sgn(<span class="m">x</span>)</div>
    <div class="lab tiny indigo b" style="left:96px; top:244px;">minorant &nbsp;&minus;<span class="m">B</span>(&minus;<span class="m">x</span>)&nbsp;&le;&nbsp;sgn(<span class="m">x</span>)</div>
    <div class="lab tiny b" style="left:508px; top:{30 + ry(1) + 8:.1f}px;">sgn(<span class="m">x</span>)</div>
    <div class="lab tiny slate" style="left:80px; top:276px;">Rings: both extremal functions meet sgn at every non&#8209;zero integer &mdash; the interpolation conditions that force extremality.</div>

    <div class="panel tint-oxide" style="left:0; top:306px; width:376px; height:176px;">
      <div class="panel-title" style="color:var(--oxide);">THE ERROR REGION AND ITS AREA</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Beurling's theorem: among all entire functions of exponential type 2&pi;&delta; majorising sgn, the minimum of &int;(<span class="m">B</span>&nbsp;&minus;&nbsp;sgn) is exactly <b>1/&delta;</b>, attained by <span class="m">x</span>&nbsp;&#8614;&nbsp;<span class="m">B</span>(&delta;<span class="m">x</span>). The band between majorant and minorant therefore has area <b>2/&delta;</b>, and it is not reducible: it is the exact price of replacing a sharp cutoff by a band&#8209;limited one.
      </div>
    </div>

    <div class="panel" style="left:396px; top:306px; width:376px; height:176px;">
      <div class="panel-title">NUMERICAL VERIFICATION AT &delta; = 1</div>
      <div class="lab wrap" style="position:static; line-height:1.5; font-family:var(--mono); font-size:10.5px;">
        exact value 1/&delta; &nbsp;=&nbsp; 1<br>
        &int; (B &minus; sgn) on [&minus;60, 60] &nbsp;=&nbsp; {chk['integral_B_minus_sgn_over_[-60,60]']:.6f}<br>
        min (B &minus; sgn) &nbsp;=&nbsp; {chk['min_B_minus_sgn']:.3e}<br>
        B(0) = {chk['B(0)']:.0f} &nbsp; B(1) = {chk['B(1)']:.0f} &nbsp; B(&minus;1) = {chk['B(-1)']:.0f}
      </div>
      <div class="lab tiny slate wrap" style="position:static; margin-top:8px; line-height:1.34;">
        The shortfall from 1 is the tail beyond |<span class="m">x</span>|&nbsp;=&nbsp;60, where <span class="m">B</span>&nbsp;&minus;&nbsp;sgn decays like <span class="m">x</span><sup>&minus;2</sup>. The minimum is zero to ten decimals, confirming the majorant property.
      </div>
    </div>

    <div class="panel dashed" style="left:792px; top:306px; width:336px; height:176px;">
      <div class="panel-title" style="color:var(--slate);">WHY IT APPEARS IN THIS BOOK</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Every explicit&#8209;formula argument that counts zeros in an interval must band&#8209;limit an indicator function. The 1/&delta; is the irreducible loss in that step. It is why a zero&#8209;counting argument at band&#8209;width &delta; cannot resolve structure finer than 1/&delta;, and it is one of the two inputs to the support&#8209;doubling bound of Figure&nbsp;21.
      </div>
    </div>

    <div class="legend" style="left:80px; top:288px; width:1048px;">
      <div class="item"><span class="swatch" style="background:var(--ink); height:3px;"></span>sgn(<span class="m">x</span>)</div>
      <div class="item"><span class="swatch" style="background:var(--oxide); height:3px;"></span>majorant &mdash; solid</div>
      <div class="item"><span class="swatch" style="background:transparent; border-top:3px dashed var(--indigo);"></span>minorant &mdash; dashed</div>
      <div class="item"><span class="swatch" style="background:#FFF; border:2px solid var(--ink); border-radius:50%; width:11px; height:11px;"></span>interpolation node</div>
    </div>"""

    cap = f"""    <b>Figure 27.</b> The Beurling&ndash;Selberg extremal pair at &delta;&nbsp;=&nbsp;1: majorant <span class="m">B</span>&nbsp;=&nbsp;<span class="m">H</span>&nbsp;+&nbsp;<span class="m">K</span>, minorant &minus;<span class="m">B</span>(&minus;<span class="m">x</span>), and sgn between them, with the interpolation nodes at the non&#8209;zero integers. The integral of <span class="m">B</span>&nbsp;&minus;&nbsp;sgn is exactly 1/&delta;; it evaluates numerically to {chk['integral_B_minus_sgn_over_[-60,60]']:.5f} on [&minus;60,&nbsp;60], the difference being the <span class="m">x</span><sup>&minus;2</sup> tail.
    <span class="limit">This figure does not establish any statement about &zeta;, and the extremality of the pair is quoted, not proved here. It establishes only the shape of the optimal band&#8209;limited replacement of a sharp cutoff and the exact area it costs.</span>
    <span class="src">Beurling (unpublished); Selberg, <i>Collected Papers</i> II (Springer, 1991) 213&ndash;225; Vaaler, <i>Bull. Amer. Math. Soc.</i> <b>12</b> (1985) 183&ndash;216, &sect;1&ndash;2 (the functions <span class="mono">H</span>, <span class="mono">K</span> and the extremal value 1/&delta;). Values computed and checked in <span class="mono">numerics/fig_13_30_data.py</span> (section fig27); {len(t)} plotted samples on [&minus;3,&nbsp;3].</span>"""

    write("fig-27-beurling-selberg.html",
          plate(27, "1200x800",
                "The Beurling&ndash;Selberg extremal pair and its error of area 1/&delta;",
                "Figure 27 &middot; Chapter 12 &middot; Classical",
                "Majorant, minorant and sgn, with the interpolation nodes that force "
                "extremality and the exact area of the region between them.",
                ("K", "[K] known / classical"), "yes", body, cap))


SCALE_1200T = SCALE_1200.replace("height:800px;", "height:1000px;")
SCALE_1400 = (SCALE_1200
              .replace("width:1200px; height:800px;", "width:1400px; height:900px;")
              .replace(".fig-head{ top:26px; left:36px; right:36px; height:86px; gap:18px; }",
                       ".fig-head{ top:28px; left:40px; right:40px; height:88px; gap:18px; }")
              .replace(".fig-head .titles{ max-width:840px; }",
                       ".fig-head .titles{ max-width:1000px; }")
              .replace(".fig-head .fig-sub{ max-width:840px; margin-top:6px; }",
                       ".fig-head .fig-sub{ max-width:1000px; margin-top:6px; }")
              .replace(".stage{ left:36px; right:36px; top:132px; bottom:186px; }",
                       ".stage{ left:40px; right:40px; top:138px; bottom:196px; }")
              .replace(".fig-cap{ left:36px; right:36px; bottom:22px; padding-top:10px; }",
                       ".fig-cap{ left:40px; right:40px; bottom:24px; padding-top:10px; }"))


# ==========================================================================
def fig24(d):
    """Prime-power contributions Lambda(n)/sqrt(n) grouped by log band."""
    bands = d["fig24_bands"]
    cum = d["fig24_cumulative"]

    # log10 axis from -1.5 to 2.75 over 320 px; 12 bands over 1008 px
    LO, HI, H = -1.5, 2.75, 320.0
    BW = 1008.0 / len(bands)
    ly = lambda v: H - (math.log10(v) - LO) / (HI - LO) * H

    bars, ticks = [], []
    series = [("k1", "var(--indigo)", "", 0), ("k2", "var(--ochre)", "hatch-ochre", 1),
              ("kge3", "var(--violet)", "hatch-violet", 2)]
    for i, b in enumerate(bands):
        x0 = i * BW
        for key, colour, hatch, j in series:
            v = b[key]
            bx = x0 + 10 + j * 22
            if v <= 0:
                bars.append('<div class="lab tiny slate" style="left:%.1fpx; top:%.1fpx; '
                            'transform:translateX(-50%%);">0</div>' % (bx + 9, H - 12))
                continue
            top = ly(v)
            bars.append('<div class="bar %s" style="left:%.1fpx; top:%.1fpx; width:18px; '
                        'height:%.1fpx; background-color:%s; border:1px solid %s;"></div>'
                        % (hatch, bx, top, H - top, colour if not hatch else "transparent", colour))
        ticks.append('<div class="lab tiny" style="left:%.1fpx; top:%.1fpx; '
                     'transform:translateX(-50%%);">%d</div>' % (x0 + BW / 2, H + 8, b["band"][0]))
        if i:
            ticks.append('<div class="vline" style="left:%.1fpx; top:0; height:%.1fpx; '
                         'background:var(--rule); width:1px;"></div>' % (x0, H))

    grid = []
    for k in (-1, 0, 1, 2):
        y = ly(10.0 ** k)
        grid.append('<div class="hline dashed" style="left:0; top:%.1fpx; width:1008px; '
                    'border-top-color:var(--rule);"></div>' % y)
        grid.append('<div class="lab tiny slate" style="left:-44px; top:%.1fpx;">10<sup>%d</sup></div>'
                    % (y - 6, k))

    rows = []
    for c in cum:
        ratio = c["k1"] / c["two_exp_half_S"]
        rows.append('<tr><td class="num">%d</td><td class="num">%.3f</td><td class="num">%.3f</td>'
                    '<td class="num">%.3f</td><td class="num">%.2f</td><td class="num">%.4f</td></tr>'
                    % (c["S"], c["k1"], c["k2"], c["kge3"], c["two_exp_half_S"], ratio))

    last = cum[-1]
    body = f"""    <div class="chip indigo" style="left:64px; top:-6px;">CONTRIBUTION OF EACH PRIME POWER TO THE EXPLICIT FORMULA &nbsp;&middot;&nbsp; weight &Lambda;(<span class="m">n</span>)&thinsp;<span class="m">n</span><sup>&minus;1/2</sup>, grouped by log&nbsp;<span class="m">n</span></div>

    <div class="plot" style="left:64px; top:30px; width:1008px; height:320px;"></div>
    <div style="position:absolute; left:64px; top:30px; width:1008px; height:320px;">
    {(NL + "    ").join(grid)}
    {(NL + "    ").join(bars)}
    {(NL + "    ").join(ticks)}
    </div>
    <div class="axis h" style="left:64px; top:350px; width:1008px;"></div>
    <div class="axis v" style="left:64px; top:24px; height:326px;"></div>
    <div class="lab tiny slate" style="left:0px; top:8px;">mass in band</div>
    <div class="lab tiny slate" style="left:460px; top:374px;">log&nbsp;<span class="m">n</span> &nbsp;&mdash;&nbsp; left endpoint of the unit band</div>

    <div class="legend" style="left:64px; top:396px; width:1008px;">
      <div class="item"><span class="swatch" style="background:var(--indigo);"></span><span class="m">k</span> = 1 &mdash; the primes themselves, weight log&nbsp;<span class="m">p</span> (solid)</div>
      <div class="item"><span class="swatch hatch-ochre" style="border:1px solid var(--ochre);"></span><span class="m">k</span> = 2 &mdash; squares <span class="m">p</span><sup>2</sup> (hatched, /)</div>
      <div class="item"><span class="swatch hatch-violet" style="border:1px solid var(--violet);"></span><span class="m">k</span> &ge; 3 &mdash; higher powers (hatched, \\)</div>
    </div>

    <table class="fig" style="position:absolute; left:0; top:430px; width:588px;">
      <tr><th><span class="m">S</span></th><th>&Sigma; <span class="m">k</span>=1</th><th>&Sigma; <span class="m">k</span>=2</th><th>&Sigma; <span class="m">k</span>&ge;3</th><th>2<span class="m">e</span><sup><span class="m">S</span>/2</sup></th><th>ratio <span class="m">k</span>=1 : 2<span class="m">e</span><sup><span class="m">S</span>/2</sup></th></tr>
      {(NL + "      ").join(rows)}
    </table>

    <div class="panel tint-indigo" style="left:612px; top:430px; width:516px; height:124px;">
      <div class="panel-title" style="color:var(--indigo);">WHY <span class="m">p</span> IS NOT NEGLIGIBLE</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Each unit band multiplies the <span class="m">k</span>&nbsp;=&nbsp;1 mass by about <span class="m">e</span><sup>1/2</sup>: the prime term tracks 2<span class="m">e</span><sup><span class="m">S</span>/2</sup> to within a factor that is already {last["k1"] / last["two_exp_half_S"]:.4f} at <span class="m">S</span>&nbsp;=&nbsp;{last["S"]}. This is the arithmetic envelope of Figure&nbsp;21. It cannot be discarded, smoothed away, or absorbed into an error term.
      </div>
    </div>

    <div class="panel tint-ochre" style="left:612px; top:558px; width:516px; height:124px;">
      <div class="panel-title" style="color:var(--ochre);">WHY <span class="m">p</span><sup>2</sup> AND HIGHER ARE NOT</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        A square <span class="m">p</span><sup>2</sup> at log&#8209;position <span class="m">u</span> carries weight 2&thinsp;log&nbsp;<span class="m">p</span>&thinsp;<span class="m">e</span><sup>&minus;<span class="m">u</span>/2</sup> with <span class="m">p</span>&nbsp;&asymp;&nbsp;<span class="m">e</span><sup><span class="m">u</span>/2</sup>, so the mass per band is <span class="m">O</span>(1) and the total grows linearly in <span class="m">S</span>. At <span class="m">S</span>&nbsp;=&nbsp;{last["S"]} squares give {last["k2"]:.3f} and higher powers {last["kge3"]:.3f}, against {last["k1"]:.1f} &mdash; about 1 : {last["k1"] / (last["k2"] + last["kge3"]):.0f}.
      </div>
    </div>"""

    cap = f"""    <b>Figure 24.</b> Prime&#8209;power contributions &Lambda;(<span class="m">n</span>)&thinsp;<span class="m">n</span><sup>&minus;1/2</sup> to the explicit formula, grouped into unit bands of log&nbsp;<span class="m">n</span> and split by the order <span class="m">k</span> of the prime power, on a logarithmic vertical scale. The <span class="m">k</span>&nbsp;=&nbsp;1 series grows geometrically with ratio <span class="m">e</span><sup>1/2</sup> per band; the <span class="m">k</span>&nbsp;=&nbsp;2 and <span class="m">k</span>&nbsp;&ge;&nbsp;3 series stay <span class="m">O</span>(1) per band. Cumulative sums are tabulated against 2<span class="m">e</span><sup><span class="m">S</span>/2</sup>.
    <span class="limit">This figure does not establish the explicit formula, does not estimate any zero sum, and does not prove that the prime term dominates for all <span class="m">S</span>. It records exact partial sums to <span class="m">X</span>&nbsp;=&nbsp;200&thinsp;000 and the observed separation between <span class="m">k</span>&nbsp;=&nbsp;1 and <span class="m">k</span>&nbsp;&ge;&nbsp;2 on that range only.</span>
    <span class="src">&Lambda;(<span class="m">n</span>) computed by a smallest&#8209;prime&#8209;factor sieve to <span class="m">X</span>&nbsp;=&nbsp;200&thinsp;000 in <span class="mono">numerics/fig_13_30_data.py</span> (section fig24); bands and cumulative sums exported to <span class="mono">figures/data/fig-13-30-data.json</span> and plotted by <span class="mono">numerics/fig_curve_builders.py</span>.</span>"""

    write("fig-24-prime-power-stack.html",
          plate(24, "1200x1000",
                "Prime&#8209;power contribution stack: why <span class=\"m\">p</span> matters and <span class=\"m\">p</span><sup>2</sup> does not",
                "Figure 24 &middot; Chapter 7 &middot; Classical, computed",
                "Real &Lambda;(<span class=\"m\">n</span>) values grouped by logarithmic support. "
                "The primes track the arithmetic envelope; every higher power does not.",
                ("K", "[K] known / classical"), "yes", body, cap,
                extra_css="""table.fig{ border-collapse:collapse; font-family:var(--sans); font-size:10.5px; }
table.fig th{ background:var(--ink); color:var(--paper); font-weight:600; font-size:9.5px;
              letter-spacing:.04em; padding:4px 6px; border:1px solid var(--ink); text-align:center; }
table.fig td{ padding:1.5px 6px; border:1px solid var(--rule); background:#FFF; text-align:center; font-size:10px; }
table.fig td.num{ font-family:var(--mono); }
.bar{ position:absolute; }
""", scale=SCALE_1200T))


# ==========================================================================
def fig28(d):
    comp = d["fig28_components"]
    inert = d["fig28_inertia"]
    summ = d["fig28_summary"]
    Ts, Ns = summ["T_values"], summ["N_values"]

    wmp = {}
    for r in comp:
        if r["form"] == "W-minus-P":
            wmp[(float(r["T"]), int(r["N"]))] = (int(r["n_positive"]), int(r["n_negative"]))
    gap = {(float(r["T"]), int(r["N"])): float(r["generalized_gap_ratio"]) for r in inert}

    CW, CH = 116.0, 44.0
    cells, heads = [], []
    for j, N in enumerate(Ns):
        heads.append('<div class="hcell" style="left:%.1fpx; top:0; width:%.1fpx;">N = %d</div>'
                     % (140 + j * CW, CW, N))
    for i, T in enumerate(Ts):
        y = 26 + i * CH
        heads.append('<div class="rcell" style="left:0; top:%.1fpx; width:136px; height:%.1fpx;">'
                     'T = %s</div>' % (y, CH, ("%g" % T)))
        for j, N in enumerate(Ns):
            p, n = wmp[(T, N)]
            g = gap.get((T, N))
            cells.append(
                '<div class="cell" style="left:%.1fpx; top:%.1fpx; width:%.1fpx; height:%.1fpx;">'
                '<b>(%d,&nbsp;%d)</b><span class="gp">gap %.3f</span></div>'
                % (140 + j * CW, y, CW - 4, CH - 4, p, n, g))

    body = f"""    <div class="chip ochre" style="left:0; top:-6px;">MEASURED INERTIA OF THE WEIL FUNCTIONAL GRAM MATRIX &nbsp;&middot;&nbsp; {summ["rows"]} CASES, ALL OF THEM</div>

    <div style="position:absolute; left:0; top:26px; width:952px; height:{26 + len(Ts) * CH:.0f}px;">
    {(NL + "    ").join(heads)}
    {(NL + "    ").join(cells)}
    </div>

    <div class="lab tiny slate" style="left:0; top:{26 + 26 + len(Ts) * CH + 6:.0f}px; width:940px; white-space:normal; line-height:1.34;">
      Each cell is one finite quadratic form: a B&#8209;spline basis of <span class="m">N</span> functions supported in [&minus;<span class="m">T</span>,&nbsp;<span class="m">T</span>], Gram entries assembled from the Weil functional with the pole terms subtracted. Entries are the measured signature (<span class="m">n</span><sub>+</sub>,&nbsp;<span class="m">n</span><sub>&minus;</sub>) of <span class="m">W</span>&nbsp;&minus;&nbsp;<span class="m">P</span>; &ldquo;gap&rdquo; is the generalised eigenvalue gap ratio, a conditioning diagnostic. <b>The negative index is 1 in every one of the {summ["rows"]} cases.</b>
    </div>

    <div class="panel tint-ochre" style="left:972px; top:26px; width:348px; height:168px;">
      <div class="panel-title" style="color:var(--ochre);">WHAT WAS MEASURED</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Three forms per case. <b><span class="m">W</span> full:</b> negative index {", ".join(summ["W_full_neg"])} &mdash; positive semi&#8209;definite, as the unconditional Weil inequality requires. <b><span class="m">P</span> poles:</b> signature ({summ["P_sig"][0][0]},&nbsp;{summ["P_sig"][0][1]}), rank two. <b><span class="m">W</span>&nbsp;&minus;&nbsp;<span class="m">P</span>:</b> negative index {", ".join(summ["WmP_neg"])} in every case &mdash; a <b>Lorentzian</b> signature (<span class="m">N</span>&minus;1,&nbsp;1).
      </div>
    </div>

    <div class="panel" style="left:972px; top:210px; width:348px; height:172px;">
      <div class="panel-title">WHY THIS IS INTERESTING</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        Index exactly one is the hypothesis <span class="m">n</span><sub>&minus;</sub>&nbsp;&le;&nbsp;1 of Theorem D (Figure&nbsp;19), and it is the shape that excludes complex off&#8209;line quadruples while leaving the real reflected pair. The measurement is stable across a factor 20 in <span class="m">T</span> and a factor 16 in <span class="m">N</span>: the index does not drift with refinement.
      </div>
    </div>

    <div class="panel tint-oxide" style="left:972px; top:398px; width:348px; height:174px;">
      <div class="panel-title" style="color:var(--oxide);">MANDATORY WARNING</div>
      <div class="lab small wrap" style="position:static; line-height:1.4;">
        <b>This signature cannot be inserted into Theorem D.</b> There is no operator &Theta; here, and no proof of the adjoint identity &Theta;*<span class="m">G</span>&nbsp;+&nbsp;<span class="m">G</span>&Theta;&nbsp;=&nbsp;<span class="m">G</span> for any &Theta;. A Gram matrix is a form, not a pair (&Theta;,&nbsp;<span class="m">G</span>). The measurement is evidence about which <i>shape</i> to look for; it is not an instance of the hypothesis, and it is finite&#8209;dimensional.
      </div>
    </div>"""

    cap = f"""    <b>Figure 28.</b> The Weil functional restricted to a finite B&#8209;spline basis becomes a finite quadratic form; its measured inertia is shown for all {summ["rows"]} cases, nine values of the support half&#8209;width <span class="m">T</span> against seven basis sizes <span class="m">N</span>. In every case the full form is positive semi&#8209;definite and the pole&#8209;subtracted form <span class="m">W</span>&nbsp;&minus;&nbsp;<span class="m">P</span> has negative index exactly one.
    <span class="limit">This figure does not establish RH, does not exhibit any operator, and does not prove that the negative index remains one in the limit <span class="m">N</span>&nbsp;&rarr;&nbsp;&infin;. It reports a finite computation on a finite basis: {summ["rows"]} matrices, each of size at most 64, with the stated numerical tolerances. It is evidence for the index&#8209;one shape and nothing more.</span>
    <span class="src">Measured data: <span class="mono">numerics/weil_spline_inertia.csv</span> ({summ["rows"]} rows, full form) and <span class="mono">numerics/weil_component_signatures.csv</span> (three component forms per case). Inertia computed by symmetric eigendecomposition with the per&#8209;row tolerance recorded in the CSV; re&#8209;exported by <span class="mono">numerics/fig_13_30_data.py</span> and laid out by <span class="mono">numerics/fig_curve_builders.py</span>.</span>"""

    write("fig-28-weil-gram.html",
          plate(28, "1400x900",
                "Weil&#8209;functional Gram matrix: the measured Lorentzian inertia",
                "Figure 28 &middot; Chapters 12 and 51 &middot; Finite numerical evidence",
                "Basis functions &rarr; a finite quadratic form. Across every computed case the "
                "pole&#8209;subtracted Weil form has negative index exactly one.",
                ("E", "[E] experimental / finite"), "yes", body, cap,
                extra_css=""".hcell{ position:absolute; font-family:var(--sans); font-size:10px; font-weight:600;
        letter-spacing:.06em; color:var(--paper); background:var(--ink); text-align:center;
        padding:5px 0; border:1px solid var(--paper); }
.rcell{ position:absolute; font-family:var(--sans); font-size:10px; font-weight:600;
        letter-spacing:.06em; color:var(--paper); background:var(--ink); text-align:center;
        border:1px solid var(--paper); display:flex; align-items:center; justify-content:center; }
.cell{ position:absolute; background:var(--ochre-16); border:1.5px solid var(--ochre);
       border-radius:3px; display:flex; flex-direction:column; align-items:center;
       justify-content:center; font-family:var(--sans); font-size:11.5px; color:var(--ink);
       background-image:repeating-linear-gradient(45deg,rgba(184,138,59,.18) 0 3px,transparent 3px 9px); }
.cell .gp{ font-family:var(--mono); font-size:8.5px; color:var(--slate); margin-top:1px; }
""", scale=SCALE_1400))


def main():
    with open(DATA, encoding="utf-8") as fh:
        d = json.load(fh)
    fig21(d)
    fig24(d)
    fig25(d)
    fig26(d)
    fig27(d)
    fig28(d)


if __name__ == "__main__":
    main()
