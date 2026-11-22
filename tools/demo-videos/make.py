import html, json, re, subprocess, sys, pathlib

R = pathlib.Path("/private/tmp/claude-501/hf/real")
W = pathlib.Path("/Volumes/MacMiniSSD/Portfolio Projects/website")
SHOT = pathlib.Path("/private/tmp/claude-501/shots")


def dims(p):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)], capture_output=True, text=True).stdout
    return int(out.split("pixelWidth:")[1].split()[0]), int(out.split("pixelHeight:")[1].split()[0])


def lines_of(path, a, b):
    return pathlib.Path(path).read_text().splitlines()[a - 1:b]


KW = r"\b(def|class|return|import|from|for|in|if|else|elif|await|async|with|as|not|and|or|None|True|False|dataclass|frozen|lambda|try|except|raise|while|yield)\b"


def hl(line):
    tok = re.compile(r"(#.*$|\"\"\".*?\"\"\"|\'(?:[^\'\\\\]|\\\\.)*\'|\"(?:[^\"\\\\]|\\\\.)*\")")
    out = []
    for p in tok.split(line):
        if not p:
            continue
        e = html.escape(p)
        if p.startswith("#"):
            out.append(f'<span class="cm">{e}</span>')
        elif p[0] in "\"'":
            out.append(f'<span class="st">{e}</span>')
        else:
            e = re.sub(KW, r'<span class="kw">\1</span>', e)
            e = re.sub(r"(?<![\w.&#;])(\d+\.?\d*)(?![\w;])", r'<span class="nm">\1</span>', e)
            e = re.sub(r"\b([a-zA-Z_]\w*)(?=\()", r'<span class="fn">\1</span>', e)
            out.append(e)
    return "".join(out) or "&nbsp;"


def spec_for(slug):
    S = {}
    S["speclane"] = dict(
        name="SpecLane", sub="Serving small hybrid-attention models under agent traffic",
        code_file="infer/profiles.py", code=lines_of("/Volumes/MacMiniSSD/Personal/Projects/1/Others/inference-engineering/infer/profiles.py", 67, 82),
        cmds=[("python3 -c \"import json,glob; [print(p['model'].ljust(16), p['profile'].ljust(20), [round(r['summary']['output_tokens_per_s'],1) for r in p['runs'] if r['workload']=='agent_sessions']) for f in sorted(glob.glob('infer/results/*.json')) for p in json.load(open(f)) if 'runs' in p]\"",
               (R / "speclane_out.txt").read_text().rstrip().splitlines(), ["+124%", "174.7", "mtp-3"])],
        shot="speclane-results", shot_url="aprameyacv.site/reports/speclane/", shot_cap="The published report, results table",
        metric="78 → 175", metric_sub="tokens per second, one request at a time (+124%)")
    S["hbc-rag"] = dict(
        name="HBC-RAG", sub="Hop-bounded agentic RAG for legal contract questions",
        code_file="packages/rag-core/src/hbc_rag/pipeline.py", code=lines_of("/Volumes/MacMiniSSD/Portfolio Projects/hbc-rag/packages/rag-core/src/hbc_rag/pipeline.py", 105, 124),
        cmds=[("python -m pytest -v --no-header", (R / "hbc_pytest.txt").read_text().rstrip().splitlines()[-6:], ["13 passed"]),
              ("python3 -c \"...\"  # summaries of the legal runs", (R / "hbc_summary.txt").read_text().rstrip().splitlines(), ["0.575", "0.469"])],
        shot="hbc-rag-report", shot_url="aprameyacv.site/reports/hbc-rag/legal.html", shot_cap="The study report generated from the saved runs",
        metric="47% → 58%", metric_sub="right clause found, four passages per hop (fine 0.469, coarse 0.575)")
    S["pramana"] = dict(
        name="Pramana", sub="Open-source decision models with calibrated confidence",
        code_file="hf/model_card_2b.md  (decide)", code=lines_of("/Volumes/MacMiniSSD/Personal/Projects/1/Pramana Decision Models/hf/model_card_2b.md", 150, 159),
        cmds=[("grep -n \"ECE\\|temperature\" FINDINGS.md | head -6", (R / "pramana_grep.txt").read_text().rstrip().splitlines(), ["ECE"])],
        shot_path=R / "hf_pramana.png", shot_url="huggingface.co/apracv/pramana-2b", shot_cap="The live model card on Hugging Face",
        metric="0.80", metric_sub="accuracy on 2,000 decisions, confidence gap down to 3.8 points")
    S["cg-bi"] = dict(
        name="CG-BI", sub="Confidence-gated cascade for wind turbine blade inspection",
        code_file="scripts/cascade.py", code=lines_of("/Volumes/MacMiniSSD/Portfolio Projects/grid-inspect/scripts/cascade.py", 14, 34),
        cmds=[("python scripts/cascade.py", [l[:118] for l in __import__('subprocess').run("cd /private/tmp/claude-501/hf/real/cg && PYTHONPATH=src '/Volumes/MacMiniSSD/Portfolio Projects/grid-inspect/.venv/bin/python' scripts/cascade.py", shell=True, capture_output=True, text=True).stdout.splitlines()], ["0.923", "1.728"])],
        shot="cg-bi-examples", shot_url="aprameyacv.site/reports/cg-bi/", shot_cap="Annotated cases from the 75-image evaluation",
        metric="92%", metric_sub="critical-defect recall at 47% of the strong model's cost")
    S["demand-forecasting"] = dict(
        name="Demand forecasting", sub="A forecasting platform that stays honest after deployment",
        code_file="src/demand_forecast/registry.py", code=lines_of("/Volumes/MacMiniSSD/Personal/Projects/1/demand-forecasting-platform/src/demand_forecast/registry.py", 120, 142),
        cmds=[("git log --oneline", (R / "demand_git.txt").read_text().rstrip().splitlines(), ["v1.0.0"])],
        shot="demand-dashboard", shot_url="aprameyacv.site/reports/demand-forecasting/dashboard/", shot_cap="The monitoring dashboard",
        metric="0.218", metric_sub="WAPE on a held-out window, 4.3 ms p99 serve latency")
    return S[slug]


def build(slug):
    s = spec_for(slug)
    T = dict(title=(0, 2.8), code=(2.8, 9.4), term=(9.4, 17.8), shot=(17.8, 23.4), end=(23.4, 27.0))
    total = T["end"][1]
    # screenshot geometry
    img_path = s.get("shot_path") or (W / "assets" / "shots" / f"{s['shot']}.jpg")
    iw, ih = dims(img_path)
    vp_h = 690
    sc = 1500 / iw
    pan = max(0, ih * sc - vp_h)
    img_name = f"shot-{slug}.jpg"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", "-Z", "3000", str(img_path), "--out", f"/private/tmp/claude-501/hf/demos/assets/{img_name}"], capture_output=True)

    s["code"] = [(l if len(l) <= 74 else l[:73] + "\u2026") for l in s["code"]]
    s["cmds"] = [((c if len(c) <= 130 else c[:128] + " \u2026"), o, h) for c, o, h in s["cmds"]]
    code_html = "".join(f'<div class="ln" id="ln{i}"><span class="no">{i + 1}</span><span class="tx">{hl(l)}</span></div>' for i, l in enumerate(s["code"]))
    n_code = len(s["code"])

    js = []
    # scene fades
    for name, (a, b) in T.items():
        js.append(f'tl.fromTo("#s-{name}", {{opacity:0}}, {{opacity:1, duration:0.35, ease:"power2.out"}}, {a});')
        if name != "end":
            js.append(f'tl.to("#s-{name}", {{opacity:0, duration:0.3, ease:"power2.in"}}, {b - 0.32});')
    # title motion
    js.append('tl.fromTo("#t-name", {y:40, opacity:0}, {y:0, opacity:1, duration:0.7, ease:"power3.out"}, 0.15);')
    js.append('tl.fromTo("#t-sub", {y:24, opacity:0}, {y:0, opacity:1, duration:0.7, ease:"power3.out"}, 0.45);')
    js.append('tl.fromTo("#t-meta", {opacity:0}, {opacity:1, duration:0.6}, 0.9);')
    # code lines
    c0 = T["code"][0] + 0.6
    for i in range(n_code):
        js.append(f'tl.fromTo("#ln{i}", {{opacity:0, x:-14}}, {{opacity:1, x:0, duration:0.25, ease:"power2.out"}}, {c0 + i * 0.2:.2f});')
    # terminal
    term_html = ""
    t = T["term"][0] + 0.5
    blocks = []
    for bi, (cmd, out, hi) in enumerate(s["cmds"]):
        chars = "".join(f'<span class="ch" id="b{bi}c{j}">{html.escape(ch)}</span>' for j, ch in enumerate(cmd))
        outs = ""
        for k, l in enumerate(out):
            e = html.escape(l)
            for h in hi:
                e = e.replace(html.escape(h), f'<b class="hi">{html.escape(h)}</b>')
            outs += f'<div class="ol" id="b{bi}o{k}">{e or "&nbsp;"}</div>'
        term_html += f'<div class="cmd"><span class="pr">$</span> {chars}<span class="cur" id="cur{bi}"></span></div><div class="outs">{outs}</div>'
        speed = min(0.04, 2.6 / max(len(cmd), 1))
        for j in range(len(cmd)):
            js.append(f'tl.set("#b{bi}c{j}", {{opacity:1}}, {t + j * speed:.3f});')
        t += len(cmd) * speed + 0.25
        js.append(f'tl.set("#cur{bi}", {{opacity:0}}, {t:.2f});')
        step = min(0.3, 4.2 / max(len(out), 1))
        for k in range(len(out)):
            js.append(f'tl.set("#b{bi}o{k}", {{opacity:1}}, {t + k * step:.2f});')
        t += len(out) * step + 0.35
    # screenshot pan
    a = T["shot"][0]
    js.append(f'tl.fromTo("#pimg", {{y:0}}, {{y:-{pan:.0f}, duration:4.1, ease:"power1.inOut"}}, {a + 0.5});')
    js.append(f'tl.fromTo("#shot-cap", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:0.5}}, {a + 0.4});')
    # end
    e0 = T["end"][0]
    js.append(f'tl.fromTo("#e-metric", {{y:40, opacity:0}}, {{y:0, opacity:1, duration:0.7, ease:"power3.out"}}, {e0 + 0.2});')
    js.append(f'tl.fromTo("#e-sub", {{opacity:0}}, {{opacity:1, duration:0.6}}, {e0 + 0.6});')
    js.append(f'tl.fromTo("#e-url", {{opacity:0}}, {{opacity:1, duration:0.6}}, {e0 + 1.0});')

    def clip(name, extra=""):
        a, b = T[name]
        return f'class="clip scene" id="s-{name}" data-start="{a}" data-duration="{b - a}" data-track-index="{list(T).index(name)}"'

    doc = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root {{ --paper:#f3f1eb; --ink:#14140f; --muted:#5d5a50; --accent:#1e4b3d; --win:#14160f; --line:#2a2d27; --txt:#e8e5da; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1920px; height:1080px; overflow:hidden; background:var(--paper); font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; color:var(--ink); }}
#root {{ position:relative; width:1920px; height:1080px; background:var(--paper); }}
.scene {{ position:absolute; inset:0; }}
.mono {{ font-family: Menlo, Monaco, "SF Mono", monospace; }}
.bar {{ position:absolute; left:0; right:0; top:0; height:10px; background:var(--accent); }}
/* title */
#t-name {{ position:absolute; left:150px; top:340px; font-size:150px; font-weight:500; letter-spacing:-0.05em; line-height:1; }}
#t-sub {{ position:absolute; left:154px; top:530px; font-size:48px; color:var(--muted); letter-spacing:-0.02em; max-width:1400px; line-height:1.25; }}
#t-meta {{ position:absolute; left:154px; bottom:120px; font-size:28px; color:var(--accent); letter-spacing:0.02em; }}
/* windows */
.win {{ position:absolute; left:210px; top:140px; width:1500px; height:800px; background:var(--win); border-radius:20px; box-shadow:0 40px 80px -40px rgba(20,20,15,0.55); overflow:hidden; }}
.tb {{ height:62px; background:#1c1f1a; display:flex; align-items:center; gap:10px; padding:0 22px; border-bottom:1px solid var(--line); }}
.tb i {{ width:14px; height:14px; border-radius:50%; background:#3a3e36; display:block; }}
.tb .lbl {{ margin-left:18px; font-size:28px; color:#a9a698; }}
.label {{ position:absolute; left:210px; top:62px; font-size:28px; color:var(--muted); letter-spacing:0.06em; text-transform:uppercase; }}
.code {{ padding:22px 0 0 0; font-size:28px; line-height:1.5; color:var(--txt); }}
.ln {{ display:flex; white-space:pre; padding-right:30px; }}
.ln .no {{ width:90px; text-align:right; padding-right:28px; color:#8a8f81; }}
.kw {{ color:#8fc4a8; }} .st {{ color:#dcbc8a; }} .cm {{ color:#7b8176; }} .nm {{ color:#d49b9b; }} .fn {{ color:#f0ede2; font-weight:600; }}
.term {{ padding:28px 40px; font-size:28px; line-height:1.5; color:var(--txt); }}
.cmd {{ white-space:pre-wrap; word-break:break-all; margin-top:10px; }}
.pr {{ color:#8fc4a8; }}
.ch {{ opacity:0; }}
.cur {{ display:inline-block; width:14px; height:28px; background:#e8e5da; vertical-align:-5px; margin-left:3px; }}
.outs {{ margin-top:14px; }}
.ol {{ opacity:0; white-space:pre-wrap; word-break:break-all; color:#cfcbbd; }}
.hi {{ color:#9be0b4; font-weight:700; }}
/* browser */
.chrome {{ position:absolute; left:210px; top:140px; width:1500px; height:790px; background:#ece8dc; border-radius:20px; overflow:hidden; box-shadow:0 40px 80px -40px rgba(20,20,15,0.45); border:1px solid #d8d3c6; }}
.chrome .tb2 {{ height:64px; display:flex; align-items:center; gap:10px; padding:0 22px; background:#ece8dc; border-bottom:1px solid #d8d3c6; }}
.chrome .tb2 i {{ width:14px; height:14px; border-radius:50%; background:#cfc9ba; display:block; }}
.chrome .url {{ margin-left:20px; font-size:28px; color:#5d5a50; background:#faf9f5; border:1px solid #e1ddd0; border-radius:999px; padding:6px 22px; }}
.vp {{ position:absolute; left:0; top:64px; width:1500px; height:{vp_h}px; overflow:hidden; background:#fff; }}
#pimg {{ position:absolute; left:0; top:0; width:1500px; display:block; }}
#shot-cap {{ position:absolute; left:210px; bottom:80px; font-size:28px; color:var(--muted); }}
/* end */
#e-metric {{ position:absolute; left:150px; top:330px; font-size:210px; font-weight:500; letter-spacing:-0.06em; color:var(--accent); line-height:1; }}
#e-sub {{ position:absolute; left:156px; top:600px; font-size:46px; color:var(--ink); letter-spacing:-0.02em; max-width:1500px; line-height:1.3; }}
#e-url {{ position:absolute; left:156px; bottom:120px; font-size:32px; color:var(--muted); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
  <div class="bar"></div>
  <div {clip("title")}>
    <div id="t-name">{html.escape(s['name'])}</div>
    <div id="t-sub">{html.escape(s['sub'])}</div>
    <div id="t-meta" class="mono">Aprameya C V &middot; real source, real terminal, real results</div>
  </div>
  <div {clip("code")}>
    <div class="label mono">Source &middot; {html.escape(s['code_file'])}</div>
    <div class="win"><div class="tb"><i></i><i></i><i></i><span class="lbl mono">{html.escape(s['code_file'])}</span></div>
      <div class="code mono">{code_html}</div></div>
  </div>
  <div {clip("term")}>
    <div class="label mono">Terminal &middot; run on this machine</div>
    <div class="win"><div class="tb"><i></i><i></i><i></i><span class="lbl mono">zsh</span></div>
      <div class="term mono">{term_html}</div></div>
  </div>
  <div {clip("shot")}>
    <div class="label mono">Live page</div>
    <div class="chrome"><div class="tb2"><i></i><i></i><i></i><span class="url mono">{html.escape(s['shot_url'])}</span></div>
      <div class="vp"><img id="pimg" src="assets/{img_name}" /></div></div>
    <div id="shot-cap">{html.escape(s['shot_cap'])}</div>
  </div>
  <div {clip("end")}>
    <div id="e-metric">{html.escape(s['metric'])}</div>
    <div id="e-sub">{html.escape(s['metric_sub'])}</div>
    <div id="e-url" class="mono">aprameyacv.site/work/{slug}</div>
  </div>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
    out = pathlib.Path("/private/tmp/claude-501/hf/demos/index.html")
    out.write_text(doc)
    return total


if __name__ == "__main__":
    print(build(sys.argv[1]))
