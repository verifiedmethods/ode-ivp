"""Write the verification report as a self-contained HTML file and as JSON."""

from __future__ import annotations

import base64
import html
import io
import json
import math

from . import UNIT_ID, UNIT_TITLE, __version__
from .checks import METHODS, ORDER_TOL
from .problems import PROBLEMS

# Categorical slots 1 to 3 of the reference palette (validated all-pairs on white;
# aqua is below 3:1 contrast, so every line is also direct-labelled and the
# numbers are in the tables).
SERIES = {
    "euler": ("#2a78d6", "o"),
    "heun": ("#eb6834", "s"),
    "rk4": ("#1baf7a", "^"),
}
INK, INK_2, INK_3, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"

STATEMENT = (
    "This report shows that the code with the student-code fingerprint above passed the gates marked PASS, "
    "using the check suite with the check-suite fingerprint above. It does not show who wrote the code."
)
SUPERVISOR_CHECK = (
    "To confirm it, copy the student's <code>student</code> folder into your own fresh copy of this unit and run "
    "<code>python verify.py</code>. Your report should show the same gates, and the check-suite fingerprint should "
    "match the one published for this release on the unit's page at verifiedmethods.github.io."
)

CSS = """
:root { --ink:#0b0b0b; --ink2:#52514e; --ink3:#8a8984; --line:#dcdad4; --bg:#ffffff; --soft:#f6f5f2;
        --pass-bg:#e5f3e8; --pass:#1d6b33; --fail-bg:#fbe6e4; --fail:#a3271f; --na-bg:#efeeea; --na:#52514e; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
main { max-width: 920px; margin: 0 auto; padding: 28px 16px 48px; }
h1 { font-size: 26px; margin: 0 0 2px; }
h2 { font-size: 19px; margin: 34px 0 10px; padding-top: 6px; border-top: 1px solid var(--line); }
h3 { font-size: 16px; margin: 22px 0 8px; }
.sub { color: var(--ink2); margin: 0 0 18px; }
.grid { display: grid; grid-template-columns: max-content 1fr; gap: 4px 16px; background: var(--soft);
        border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; }
.grid dt { color: var(--ink2); }
.grid dd { margin: 0; overflow-wrap: anywhere; }
code, .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 4px; font-size: 14px; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--ink2); font-weight: 600; background: var(--soft); }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.wrap { overflow-x: auto; }
.badge { display: inline-block; padding: 1px 8px; border-radius: 999px; font-size: 12px; font-weight: 700;
         letter-spacing: .02em; white-space: nowrap; }
.pass { background: var(--pass-bg); color: var(--pass); }
.fail { background: var(--fail-bg); color: var(--fail); }
.na { background: var(--na-bg); color: var(--na); }
.hint { color: var(--fail); font-size: 13px; margin-top: 4px; }
.reason { color: var(--ink2); font-size: 13px; }
.note { color: var(--ink2); font-size: 13px; }
.statement { border-left: 4px solid var(--ink); background: var(--soft); padding: 10px 14px; border-radius: 0 8px 8px 0; }
figure { margin: 10px 0 18px; }
figure img { width: 100%; max-width: 760px; height: auto; display: block; }
figcaption { color: var(--ink2); font-size: 13px; margin-top: 4px; }
table.narrow { width: auto; min-width: 50%; }
td.order { color: var(--ink2); }
footer { margin-top: 36px; color: var(--ink3); font-size: 12px; }
.block { break-inside: avoid; }
@media print { body { font-size: 12px; } main { padding: 0; } h2, h3 { break-after: avoid; }
               .block, figure, table, .statement { break-inside: avoid; }
               figure img { max-width: 470px; } }
"""


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def _fmt(x, digits=2) -> str:
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "n/a"
    return f"{x:.{digits}e}"


def _badge(passed) -> str:
    if passed is True:
        return '<span class="badge pass">PASS</span>'
    if passed is False:
        return '<span class="badge fail">FAIL</span>'
    return '<span class="badge na">NOT RUN</span>'


# --------------------------------------------------------------------------- plots


def _figures(results):
    """Return (convergence_png_b64, cost_png_b64), or (None, None) if nothing can be plotted."""
    series = []
    for r in results:
        tab = r.reported.get("error_tables", {})
        rows = tab.get("P2", {}).get("rows") if isinstance(tab, dict) else None
        if rows and all(math.isfinite(x["error"]) and x["error"] > 0 for x in rows):
            series.append((r.spec, rows))
    if not series:
        return None, None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None, None

    def style(ax, xlabel, ylabel):
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(xlabel, color=INK_2)
        ax.set_ylabel(ylabel, color=INK_2)
        ax.grid(True, which="major", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(INK_3)
        ax.tick_params(colors=INK_2, labelsize=9)

    out = []
    for kind in ("convergence", "cost"):
        fig, ax = plt.subplots(figsize=(6.6, 4.2), dpi=150)
        for spec, rows in series:
            color, marker = SERIES[spec.key]
            xs = [r["h"] for r in rows] if kind == "convergence" else [r["evals"] for r in rows]
            ys = [r["error"] for r in rows]
            ax.plot(xs, ys, color=color, marker=marker, markersize=6, linewidth=2,
                    markeredgecolor="white", markeredgewidth=1.0, label=spec.name, zorder=3)
            # Direct label at the end of the line, in ink, not in the series colour.
            end = 0 if kind == "convergence" else -1
            ax.annotate(spec.name, (xs[end], ys[end]), xytext=(6, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=9, color=INK)
            if kind == "convergence":
                # Reference slope p, drawn through the middle point and shifted down by 3x.
                mid = len(xs) // 2
                x0, y0 = xs[mid], ys[mid] / 3.0
                xr = [xs[-1], xs[0]]
                yr = [y0 * (x / x0) ** spec.order for x in xr]
                ax.plot(xr, yr, color=INK_3, linestyle=(0, (4, 3)), linewidth=1.0, zorder=2)
                ax.annotate(f"slope {spec.order}", (xr[0], yr[0]), xytext=(-2, -10), textcoords="offset points",
                            ha="left", fontsize=8, color=INK_3)
        if kind == "convergence":
            style(ax, "step size h", "error at t = 2 (max norm)")
            ax.set_title("Convergence on P2: error against step size", loc="left", fontsize=11, color=INK)
            xmin, xmax = ax.get_xlim()
            ax.set_xlim(xmin / 1.6, xmax * 1.6)
            ymin, ymax = ax.get_ylim()
            ax.set_ylim(ymin / 8.0, ymax)  # room for the slope labels under the lowest reference line
        else:
            style(ax, "number of f-evaluations", "error at t = 2 (max norm)")
            ax.set_title("Cost on P2: error against work", loc="left", fontsize=11, color=INK)
            xmin, xmax = ax.get_xlim()
            ax.set_xlim(xmin / 1.3, xmax * 3.0)
        ax.legend(frameon=False, fontsize=9, loc="lower right" if kind == "convergence" else "lower left")
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        out.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    return out[0], out[1]


# --------------------------------------------------------------------------- HTML pieces


def _summary_table(results) -> str:
    rows = []
    for r in results:
        if r.status == "checked":
            status = _badge(r.all_passed)
            gates = f"{r.n_passed} / {len(r.gates)}"
            g4 = next((g for g in r.gates if g.id == "G4"), None)
            order = f"{g4.value:.3f}" if g4 is not None and g4.value is not None else "n/a"
        else:
            status = f'<span class="badge na">{_e(r.status.upper())}</span>'
            gates, order = "", ""
        rows.append(
            f"<tr><td>{_e(r.spec.name)} <span class='note mono'>{_e(r.spec.function)}</span></td>"
            f"<td>{status}</td><td class='num'>{gates}</td><td class='num'>{r.spec.order}</td><td class='num'>{order}</td></tr>"
        )
    return (
        "<div class='wrap'><table><thead><tr><th>Method</th><th>Result</th><th class='num'>Gates passed</th>"
        "<th class='num'>Theoretical order</th><th class='num'>Observed order (G4)</th></tr></thead><tbody>"
        + "".join(rows) + "</tbody></table></div>"
    )


def _gates_table(r) -> str:
    rows = []
    for g in r.gates:
        hint = f"<div class='hint'>{_e(g.hint)}</div>" if g.hint else ""
        rows.append(
            f"<tr><td class='mono'>{_e(g.id)}</td><td>{_e(g.title)}<div class='reason'>{_e(g.reason)}</div>{hint}</td>"
            f"<td>{_e(g.tolerance)}</td><td>{_e(g.measured)}</td><td>{_badge(g.passed)}</td></tr>"
        )
    return (
        "<div class='wrap'><table><thead><tr><th>#</th><th>Gate</th><th>Tolerance</th><th>Measured</th><th>Result</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def _error_tables(r) -> str:
    tabs = r.reported.get("error_tables")
    if not isinstance(tabs, dict):
        return ""
    if "error" in tabs:
        return f"<p class='hint'>{_e(tabs['error'])}</p>"
    pids = list(tabs)
    head = "".join(f"<th class='num'>{_e(pid)} error</th><th class='num'>order</th>" for pid in pids)
    body = []
    n_rows = len(tabs[pids[0]]["rows"])
    for i in range(n_rows):
        cells = [f"<td class='num'>{tabs[pids[0]]['rows'][i]['n']}</td>"]
        for pid in pids:
            row = tabs[pid]["rows"][i]
            o = tabs[pid]["orders"][i - 1] if i > 0 else None
            o_txt = f"{o:.3f}" if o is not None and math.isfinite(o) else ""
            cells.append(f"<td class='num'>{_fmt(row['error'])}</td><td class='num order'>{o_txt}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    legend = "; ".join(f"<strong>{_e(pid)}</strong> {_e(t['title'])}: <span class='mono'>{_e(t['equation'])}</span>"
                       for pid, t in tabs.items())
    return (
        "<div class='block'>"
        f"<h3>R1. Error against the exact solution (expected order {r.spec.order})</h3>"
        f"<p class='note'>Error at the end of each interval (max norm) with n equal steps, so h = (interval length)/n. "
        "<em>Order</em> is log(e<sub>previous</sub>/e)/log 2, since h halves between rows. "
        f"{legend}.</p>"
        "<div class='wrap'><table><thead><tr><th class='num'>n</th>" + head + "</tr></thead><tbody>"
        + "".join(body) + "</tbody></table></div></div>"
    )


def _scipy_table(r) -> str:
    s = r.reported.get("scipy_agreement")
    if not isinstance(s, dict):
        return ""
    if "error" in s:
        return f"<h3>R4. Agreement with SciPy on P5</h3><p class='hint'>{_e(s['error'])}</p>"
    body = "".join(
        f"<tr><td class='num'>{row['n']}</td><td class='num'>{row['h']:.4g}</td><td class='num'>{_fmt(row['relative_error'])}</td></tr>"
        for row in s["rows"]
    )
    return (
        "<div class='block'><h3>R4. Agreement with SciPy on P5 (Lotka–Volterra, no exact solution)</h3>"
        f"<p class='note'>Relative error at t = 15 against {_e(s['reference'])}.</p>"
        "<table class='narrow'><thead><tr><th class='num'>n</th><th class='num'>h</th><th class='num'>relative error</th></tr></thead>"
        f"<tbody>{body}</tbody></table></div>"
    )


def _stability_table(r) -> str:
    s = r.reported.get("stability")
    if not isinstance(s, dict):
        return ""
    if "error" in s:
        return f"<h3>R5. Stability on the stiff problem P6</h3><p class='hint'>{_e(s['error'])}</p>"
    body = "".join(
        f"<tr><td class='num'>{row['h']:.5f}</td><td class='num'>{row['h_over_limit']:.3f}</td>"
        f"<td class='num'>{_fmt(row['abs_y_end'])}</td><td>{_e(row['behaviour'])}</td></tr>"
        for row in s["rows"]
    )
    return (
        "<div class='block'><h3>R5. Stability on the stiff problem P6 (y' = −50y on [0, 4])</h3>"
        f"<p class='note'>Theory: {_e(s['theory'])}. The exact solution decays to 1.4e-87.</p>"
        "<table class='narrow'><thead><tr><th class='num'>h</th><th class='num'>h / limit</th><th class='num'>|y(4)|</th>"
        f"<th>behaviour</th></tr></thead><tbody>{body}</tbody></table></div>"
    )


def _method_section(r) -> str:
    head = f"<h2>{_e(r.spec.name)} <span class='note mono'>{_e(r.spec.function)}</span></h2>"
    if r.status != "checked":
        return f"<section>{head}<p>{_badge(None)} {_e(r.message)}</p></section>"
    return (
        f"<section>{head}<div class='block'><h3>Gates (must pass)</h3>{_gates_table(r)}</div>"
        "<p class='note'>Reported results below have no pass mark: interpret them in your write-up.</p>"
        f"{_error_tables(r)}{_scipy_table(r)}{_stability_table(r)}</section>"
    )


def build_html(results, meta) -> str:
    info = meta["student"]
    fp = meta["fingerprints"]
    env = meta["environment"]
    rows = [
        ("Student", info.get("name")),
        ("Matriculation number", info.get("matric_number")),
        ("Department", info.get("department")),
        ("Institution", info.get("institution")),
        ("Supervisor", info.get("supervisor")),
        ("Run", f"{meta['generated_at']} ({meta['mode_label']})"),
    ]
    if meta.get("ci"):
        ci = meta["ci"]
        rows.append(("Repository and commit", f"{ci.get('repository', '')} @ {ci.get('commit', '')}"))
        if ci.get("run_url"):
            rows.append(("CI run", ci["run_url"]))
    rows += [
        ("Student-code fingerprint", f"SHA-256 {fp['student_code']}"),
        ("Check-suite fingerprint", f"SHA-256 {fp['check_suite']}"),
        ("Environment", f"Python {env['python']}, NumPy {env['numpy']}, SciPy {env['scipy']}, "
                        f"Matplotlib {env['matplotlib']}, {env['os']}"),
    ]
    grid = "".join(
        f"<dt>{_e(k)}</dt><dd class='{'mono' if 'fingerprint' in k else ''}'>{_e(v if v else '(not given)')}</dd>"
        for k, v in rows
    )
    conv, cost = _figures(results)
    figs = ""
    if conv:
        figs = (
            "<h2>Comparing the methods</h2>"
            f"<figure><img alt='Log-log plot of error against step size on P2 for each implemented method, "
            f"with dashed reference lines of the theoretical slopes.' src='data:image/png;base64,{conv}'>"
            "<figcaption>R2. Each line should run parallel to its dashed reference slope. Numbers: table R1 for P2."
            "</figcaption></figure>"
            f"<figure><img alt='Log-log plot of error against number of f-evaluations on P2 for each implemented method.' "
            f"src='data:image/png;base64,{cost}'>"
            "<figcaption>R3. For a target error (a horizontal line), the method furthest left is the cheapest.</figcaption></figure>"
        )
    missing = [k for k in ("name", "matric_number", "institution", "supervisor", "ai_use") if not info.get(k)]
    warn = ""
    if missing:
        warn = ("<p class='hint'>Fill in student/student_info.txt (missing: "
                + _e(", ".join(missing)) + ") before you submit this report.</p>")
    ai = info.get("ai_use")
    title = f"Verification report: {info.get('name') or 'student'}, unit {UNIT_ID}"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title><style>{CSS}</style></head>
<body><main>
<h1>Verification report</h1>
<p class="sub">verifiedmethods · Unit {_e(UNIT_ID)}: {_e(UNIT_TITLE)} · version {_e(__version__)}</p>
<dl class="grid">{grid}</dl>
{warn}
<h2>Summary</h2>
{_summary_table(results)}
<p class="note">A method passes when all four gates pass. Gate G4 accepts an observed order within ±{ORDER_TOL} of the theoretical order. Details for each method follow the statement below.</p>
{figs}
<h2>AI-use disclosure</h2>
<p>{_e(ai) if ai else '(not given)'}</p>
<h2>What this report shows</h2>
<div class="statement"><p>{_e(STATEMENT)}</p><p>{SUPERVISOR_CHECK}</p></div>
{''.join(_method_section(r) for r in results)}
<footer>Generated by <code>verify.py</code>. The same results are in <code>verification-report.json</code>.
Test problems: {', '.join(f'{p.id} {p.title}' for p in PROBLEMS.values())}.</footer>
</main></body></html>
"""


def _clean(o):
    """Replace non-finite floats by None so the file is valid JSON."""
    if isinstance(o, float):
        return o if math.isfinite(o) else None
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def build_json(results, meta) -> str:
    data = dict(meta)
    data.pop("mode_label", None)
    data["results"] = [r.to_dict() for r in results]
    data["statement"] = STATEMENT
    data["methods"] = [m.key for m in METHODS]
    return json.dumps(_clean(data), indent=2, allow_nan=False, default=str)
