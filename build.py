#!/usr/bin/env python3
"""Static site builder for aprameyacv.site.

Pages are generated so the head, nav and footer stay identical everywhere.
Run: python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent

SITE = "https://aprameyacv.site"
EMAIL = "aprameyacv01@gmail.com"
GH = "https://github.com/Aprameya-C-V"
HF = "https://huggingface.co/apracv"
LI = "https://www.linkedin.com/in/aprameyacv/"


def head(title, desc, base):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/">
<meta name="theme-color" content="#f3f1eb">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<nav class="nav" aria-label="Primary">
  <a class="mark" href="{base}index.html">Aprameya C V</a>
  <a class="link" href="{base}index.html#work">Work</a>
  <a class="link hide-sm" href="{base}index.html#about">About</a>
  <a class="link" href="{base}index.html#contact">Contact</a>
  <a class="pill" href="{base}resume.pdf" target="_blank" rel="noreferrer">Resume <span class="arrow">&#8599;</span></a>
</nav>
<main id="main">
"""


def foot(base):
    return f"""</main>
<footer>
  <div class="wrap foot">
    <span>&copy; <span data-year>2026</span> Aprameya C V &middot; Bengaluru, India</span>
    <span>Hand-written HTML &middot; no framework</span>
  </div>
</footer>
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""


PROJECTS = [
    {
        "slug": "pramana",
        "metric_short": "0.80",
        "metric_note": "accuracy",
        "idx": "01",
        "title": "Pramana",
        "tagline": "Open-source decision models with calibrated confidence",
        "row": "2B and 0.8B models that return a probability per option plus a confidence score.",
        "stack": "LoRA &middot; Hugging Face &middot; PyTorch",
        "metric": "80%",
        "metric_label": "accuracy across 2,000 decisions",
        "stats": [
            ("0.800", "accuracy, 2,000 decisions"),
            ("0.038", "confidence calibration error"),
            ("1 in 3", "decisions settled by the 0.8B"),
            ("0.076", "KL divergence, best fine-tuned entry"),
        ],
        "kicker": "Selected work &middot; 01",
        "sub": "Small open models that answer a structured question with a probability for every option, and say how much to trust that answer.",
        "tags": ["Python", "LoRA", "Hugging Face", "A100"],
        "sections": [
            ("What it is", """<p>Pramana takes one piece of unstructured state and a typed question, and returns a probability over every option rather than a single label. Each answer carries two outputs from the same logits: a calibrated probability, and a separate confidence score that tracks whether the top answer is actually right.</p>
<p>Two models ship: Pramana-2B and Pramana-0.8B, both trained from Qwen bases and published on Hugging Face with their calibration files and predictions.</p>"""),
            ("How it works", """<ul>
<li><strong>Soft gold training.</strong> Fine-tuned with LoRA against soft labels and a Brier term, so the probabilities come out calibrated without a post-hoc temperature. The fitted temperature lands between 1.00 and 1.05.</li>
<li><strong>Decoupled calibration.</strong> One set of logits, two temperatures: one fitted to the soft gold for KL and Brier, one fitted to the hard label for expected calibration error and deferral.</li>
<li><strong>A 0.8B to 2B cascade.</strong> The small model answers whenever its top probability clears 0.68, chosen on holdout; the rest go to the 2B. One decision in three never reaches the larger model and accuracy holds.</li>
</ul>"""),
            ("What it measured", """<table>
<thead><tr><th>Model</th><th class="num">Params</th><th class="num">Accuracy</th><th class="num">KL</th><th class="num">Brier</th><th class="num">Confidence ECE</th></tr></thead>
<tbody>
<tr><td><strong>Pramana-2B</strong></td><td class="num">2.3B</td><td class="num">0.8005</td><td class="num">0.0755</td><td class="num">0.0415</td><td class="num">0.0379</td></tr>
<tr><td><strong>Pramana-0.8B</strong></td><td class="num">0.8B</td><td class="num">0.7970</td><td class="num">0.0819</td><td class="num">0.0446</td><td class="num">0.0249</td></tr>
<tr><td>Board, 3-4B entries</td><td class="num">3-4B</td><td class="num">0.808-0.8205</td><td class="num">0.077-0.301</td><td class="num">0.042-0.132</td><td class="num">-</td></tr>
</tbody>
</table>
<p class="small" style="margin-top:12px">Typed Decisions benchmark: 400 test cases, 2,000 decisions, four workflows. Pramana is trained on the train split, so it is compared with other fine-tuned entries, not zero-shot rows.</p>"""),
            ("What it does not claim", """<p>The 3-4B board entries still edge out Pramana on raw accuracy. The claim here is calibration and cost, not a state-of-the-art score: the lowest KL and Brier of any fine-tuned entry listed, with a cascade that keeps accuracy while leaving the larger model idle for a third of decisions.</p>"""),
        ],
        "links": [("Repository", GH + "/pramana", True), ("Model cards", HF, True), ("Full report", "reports/pramana/index.html", False)],
    },
    {
        "slug": "hbc-rag",
        "metric_short": "47&rarr;58%",
        "metric_note": "clause hit",
        "idx": "02",
        "title": "HBC-RAG",
        "tagline": "Agentic retrieval for legal contract questions",
        "row": "A planner and verifier agent under a hop cap, tuned on passages per hop.",
        "stack": "pgvector &middot; Postgres &middot; FastAPI",
        "metric": "47 &rarr; 58%",
        "metric_label": "clause hit rate, four passages per hop",
        "stats": [
            ("47 &rarr; 58%", "clauses found"),
            ("8.9 &rarr; 4.2 s", "median latency"),
            ("+12 pts", "character recall"),
            ("&minus;26%", "cost per question"),
        ],
        "kicker": "Selected work &middot; 02",
        "sub": "Does fetching more passages per step make an agent find better evidence? On legal contracts, yes, and it is also faster.",
        "tags": ["Python", "Postgres", "pgvector", "agents"],
        "sections": [
            ("What it is", """<p>An agent that answers questions over legal contracts by planning a search, retrieving evidence, and verifying its answer against what it retrieved. A hop cap stops it looping. The study question is narrow: holding the model, prompt and corpus fixed, does retrieving four passages per step instead of one change quality, cost or latency?</p>"""),
            ("How it works", """<ul>
<li><strong>Hybrid retrieval.</strong> pgvector HNSW for dense search plus Postgres full-text search, fused by reciprocal rank fusion, in a Neon Postgres database.</li>
<li><strong>One protocol, two policies.</strong> Fine fetches one passage per hop, coarse fetches four. Everything else is identical, so the difference is attributable to hop size.</li>
<li><strong>Scored against human labels.</strong> 468 contracts and privacy policies from LegalBench-RAG, split into 13,962 passages, with 140 questions scored by character span against the benchmark's labelled evidence, plus paired bootstrap intervals.</li>
</ul>"""),
            ("What it measured", """<table>
<thead><tr><th>DeepSeek, 140 questions</th><th class="num">Clause hit</th><th class="num">Char recall</th><th class="num">Char precision</th><th class="num">Median</th><th class="num">Cost</th></tr></thead>
<tbody>
<tr><td>One passage per hop</td><td class="num">0.469</td><td class="num">0.423</td><td class="num">0.120</td><td class="num">8.9 s</td><td class="num">$0.063</td></tr>
<tr><td><strong>Four passages per hop</strong></td><td class="num"><strong>0.575</strong></td><td class="num"><strong>0.547</strong></td><td class="num">0.065</td><td class="num"><strong>4.2 s</strong></td><td class="num"><strong>$0.047</strong></td></tr>
</tbody>
</table>
<p style="margin-top:14px">Clause hit rises 10.6 points (95% CI +4.6 to +16.6) and character recall 12.4 points, both excluding zero. Precision falls, which is the expected cost of returning more text, and is reported rather than hidden. A second model family reproduces the recall gain; its clause-hit gain is not distinguishable from zero.</p>"""),
            ("What it does not claim", """<p>The evidence in LegalBench-RAG sits inside a single document, so this measures retrieval granularity within one contract, not multi-document reasoning. The benchmark has no gold answers, so no answer-accuracy claim is made. One seed per model; MAUD merger agreements were excluded to fit a free database tier.</p>"""),
        ],
        "links": [("Repository", GH + "/hbc-rag", True), ("Full report", "reports/hbc-rag/index.html", False)],
    },
    {
        "slug": "speclane",
        "metric_short": "+124%",
        "metric_note": "tokens/s, c=1",
        "idx": "03",
        "title": "SpecLane",
        "tagline": "Serving small models under agent traffic",
        "row": "A reproducible vLLM profile for two open models, one change at a time.",
        "stack": "vLLM &middot; H100 / L40S &middot; Modal",
        "metric": "+124%",
        "metric_label": "throughput at concurrency 1",
        "stats": [
            ("78 &rarr; 175", "tokens/s at concurrency 1"),
            ("800 &rarr; 1199", "tokens/s at concurrency 16"),
            ("1.09 &rarr; 0.94 s", "p99 time to first token"),
            ("0.940 &rarr; 0.935", "GSM8K, unchanged"),
        ],
        "kicker": "Selected work &middot; 03",
        "sub": "Existing vLLM flags, an honest baseline, and a measurement of which one actually matters when the traffic looks like an agent loop.",
        "tags": ["vLLM", "CUDA", "H100", "L40S"],
        "sections": [
            ("What it is", """<p>A serving configuration for two open models, Qwen3.8-27B-FP8 on one H100 and Qwen3.5-9B on one L40S, built around agent-shaped traffic: long shared system prompts and multi-turn sessions. It defines a vanilla baseline, a recommended profile, and one change at a time on top of it, with every number generated from the saved run files.</p>"""),
            ("How it works", """<ul>
<li><strong>A baseline you can reproduce.</strong> Engine defaults plus only the flags needed to start, fixed 16,384-token context.</li>
<li><strong>Two workloads.</strong> <span class="mono">shared_prefix</span> and <span class="mono">agent_sessions</span>, swept at concurrency 1 and 16 through a closed-loop load generator that records TTFT, TPOT and throughput.</li>
<li><strong>A quality guard.</strong> 200 fixed GSM8K questions, temperature 0, exact match, so a throughput win cannot hide an accuracy loss.</li>
</ul>"""),
            ("What it measured", """<table>
<thead><tr><th>Profile</th><th class="num">c = 1</th><th class="num">c = 16</th><th class="num">p99 TTFT</th></tr></thead>
<tbody>
<tr><td>27B, baseline</td><td class="num">78</td><td class="num">800</td><td class="num">1.09 s</td></tr>
<tr><td>27B, <strong>multi-token prediction</strong></td><td class="num"><strong>175 (+124%)</strong></td><td class="num"><strong>1199 (+50%)</strong></td><td class="num"><strong>0.94 s</strong></td></tr>
<tr><td>27B, FP8 KV cache only</td><td class="num">76 (&minus;2%)</td><td class="num">684 (&minus;14%)</td><td class="num">1.46 s</td></tr>
<tr><td>9B, baseline</td><td class="num">43</td><td class="num">475</td><td class="num">0.95 s</td></tr>
<tr><td>9B, <strong>multi-token prediction</strong></td><td class="num"><strong>75 (+77%)</strong></td><td class="num"><strong>753 (+59%)</strong></td><td class="num"><strong>0.74 s</strong></td></tr>
</tbody>
</table>
<p style="margin-top:14px">The models' built-in multi-token-prediction head is the lever. The FP8 KV cache, which is usually recommended, reduced throughput and raised tail latency at this scale. Quality moved by one and two questions out of 200, inside noise.</p>"""),
            ("A failure worth keeping", """<p>Vanilla vLLM cannot start the 27B on an H100: the default <span class="mono">max_num_seqs</span> of 1024 exceeds the 745 recurrent-state cache blocks that fit beside the weights. Setting it to 512 resolves it and became part of the baseline. An earlier agent-harness pilot that scored zero was traced to a missing tool-calling flag, not to the model, and is written up as a withdrawn result.</p>"""),
        ],
        "links": [("Repository", GH + "/speclane", True), ("Full report", "reports/speclane/index.html", False)],
    },
    {
        "slug": "cg-bi",
        "metric_short": "92.3%",
        "metric_note": "critical recall",
        "idx": "04",
        "title": "CG-BI",
        "tagline": "Confidence-gated triage for blade inspection",
        "row": "A cheap model reviews every drone image; uncertain ones escalate.",
        "stack": "Multimodal LLMs &middot; Python",
        "metric": "92%",
        "metric_label": "critical-defect recall at 47% of cost",
        "stats": [
            ("92.3%", "critical-defect recall"),
            ("47%", "of the strong tier's cost"),
            ("25.3%", "exact match, best of any tier"),
            ("0.424", "class F1"),
        ],
        "kicker": "Selected work &middot; 04",
        "sub": "Routing, not tier choice, is the lever: a two-tier cascade beats both of its own models on quality and lands between them on cost.",
        "tags": ["Multimodal", "Python", "cost control"],
        "sections": [
            ("What it is", """<p>A drone captures hundreds of blade images per turbine, and an engineer still writes a finding for each one: defect type, severity, location, action. This measures whether a multimodal model can draft that finding, and what a two-tier routing policy buys over picking a single model.</p>"""),
            ("How it works", """<ul>
<li><strong>75 real drone images</strong> across a fixed six-class taxonomy, one call per image unless escalated.</li>
<li><strong>A confidence gate.</strong> A cheap multimodal model labels every image; anything below 0.9 confidence, 36% of the set, goes to a stronger model.</li>
<li><strong>Costed per thousand images</strong>, with p50 latency, so a quality win that nobody can afford shows up as one.</li>
</ul>"""),
            ("What it measured", """<table>
<thead><tr><th>Tier</th><th class="num">Exact set</th><th class="num">Class F1</th><th class="num">Critical recall</th><th class="num">Cost / 1,000</th></tr></thead>
<tbody>
<tr><td>Cheap model alone</td><td class="num">17.3%</td><td class="num">0.323</td><td class="num">50.0%</td><td class="num">$0.43</td></tr>
<tr><td>Strong model alone</td><td class="num">14.7%</td><td class="num">0.417</td><td class="num">96.2%</td><td class="num">$3.64</td></tr>
<tr><td><strong>Routed cascade</strong></td><td class="num"><strong>25.3%</strong></td><td class="num"><strong>0.424</strong></td><td class="num"><strong>92.3%</strong></td><td class="num"><strong>$1.73</strong></td></tr>
</tbody>
</table>
<p style="margin-top:14px">The cascade beats both single tiers on exact match and F1, holds 92% critical-defect recall, and costs 47% of the strong tier alone. The strong tier is accurate but expensive; the cheap tier alone misses half the critical defects.</p>"""),
            ("What it does not claim", """<p>One seed, 75 images, and no healthy-blade class, so this is not a claim that inspection can be automated. The cascade drafts a finding for an engineer to approve or correct.</p>"""),
        ],
        "links": [("Repository", GH + "/cg-bi", True), ("Full report", "reports/cg-bi/index.html", False)],
    },
    {
        "slug": "demand-forecasting",
        "metric_short": "0.218",
        "metric_note": "WAPE",
        "idx": "05",
        "title": "Demand forecasting",
        "tagline": "Forecasts that stay honest after deployment",
        "row": "A contracts-in, gate-out forecasting platform with drift-driven retraining.",
        "stack": "LightGBM &middot; FastAPI &middot; CI",
        "metric": "21.8%",
        "metric_label": "WAPE on a held-out window",
        "stats": [
            ("0.218", "WAPE, held-out"),
            ("0.794", "interval coverage, nominal 0.80"),
            ("4.3 ms", "p99 serve latency"),
            ("570 req/s", "one process, four clients"),
        ],
        "kicker": "Selected work &middot; 05",
        "sub": "An MLOps reference implementation: contracts validate the input, a gate decides what reaches production, and a drift monitor opens the retraining issue.",
        "tags": ["Python", "LightGBM", "FastAPI", "GitHub Actions"],
        "sections": [
            ("What it is", """<p>A demand forecasting platform for NYC taxi data where the interesting part is everything after the model: input contracts, a champion and challenger gate, an API that reports on itself, and a monitor that files a ticket when the model starts to slip. Everything runs on free tiers, with no always-on infrastructure.</p>"""),
            ("How it works", """<ul>
<li><strong>Five stages, one repository.</strong> Panel contract, time-split training, registry gate, served forecast API, drift monitor. Each runs as a command locally and as a workflow in CI.</li>
<li><strong>A gate with a margin.</strong> A challenger replaces the champion only if it wins by more than 2% WAPE.</li>
<li><strong>Monitoring closes the loop.</strong> A WAPE, bias or PSI breach opens a retraining issue, so monitoring is part of the pipeline rather than a report at the end.</li>
</ul>"""),
            ("What it measured", """<table>
<thead><tr><th>Metric</th><th class="num">Value</th><th>Reading</th></tr></thead>
<tbody>
<tr><td>WAPE</td><td class="num">0.218</td><td>total absolute error over total demand</td></tr>
<tr><td>Coverage, p10 to p90</td><td class="num">0.794</td><td>nominal 0.80, band is calibrated</td></tr>
<tr><td>Bias</td><td class="num">&minus;2.5%</td><td>inside the &plusmn;10% gate</td></tr>
<tr><td>p99 serve latency</td><td class="num">4.3 ms</td><td>one client, 48-slot forecast</td></tr>
<tr><td>Throughput</td><td class="num">570 req/s</td><td>four concurrent clients, one process</td></tr>
</tbody>
</table>"""),
            ("What it does not claim", """<p>One run per configuration, no tuning on the test window, and errors below the 5% noise floor are not claimed. It is a reference implementation on public data, not a production deployment.</p>"""),
        ],
        "links": [("Repository", GH + "/demand-forecasting-platform", True), ("Full report", "reports/demand-forecasting/index.html", False)],
    },
]


def home():
    rows = "\n".join(
        f"""      <a class="work-row reveal" href="work/{p['slug']}.html">
        <span class="idx">{p['idx']}</span>
        <span>
          <span class="t">{p['title']}</span>
          <span class="d">{p['row']}</span>
          <span class="stack-inline">{p['stack']}</span>
        </span>
        <span class="metric"><b>{p['metric_short']}</b><i>{p['metric_note']}</i></span>
        <span class="go">&#8599;</span>
      </a>"""
        for p in PROJECTS
    )

    html = head(
        "Aprameya C V — AI engineer",
        "AI engineer at Oracle building agentic and generative AI systems, and measuring what they actually do.",
        "",
    )
    html += f"""
<header class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Bengaluru, India</p>
      <h1 class="display">AI systems,<br>built to be <em>measured</em>.</h1>
      <p class="lede">I am Aprameya, an AI engineer at Oracle. I take agentic and generative AI from a customer's first conversation to production: retrieval, agent design, GPU serving, and the infrastructure underneath.</p>
      <div class="meta">
        <span><i></i>Cloud Engineering &middot; AI</span>
        <span><i></i>Oracle</span>
        <span><i></i>Five measured projects</span>
      </div>
      <div class="cta-row">
        <a class="btn" href="#work">See the work <span class="dot">&#8595;</span></a>
        <a class="btn ghost" href="resume.pdf" target="_blank" rel="noreferrer">Resume <span class="dot">&#8599;</span></a>
      </div>
    </div>
    <aside class="card-outer reveal">
      <div class="card-inner">
        <h3>At a glance</h3>
        <div class="kv"><span>Role</span><span class="v">AI engineer, Oracle</span></div>
        <div class="kv"><span>Focus</span><span class="v">Agents &amp; inference</span></div>
        <div class="kv"><span>Reports</span><span class="v"><b>5</b> with numbers</span></div>
        <div class="kv"><span>Open to</span><span class="v">Applied AI, FDE</span></div>
      </div>
    </aside>
  </div>
</header>

<section id="work">
  <div class="wrap">
    <div class="section-head">
      <h2 class="h2">Selected work</h2>
      <span class="count">05 / 2025&ndash;2026</span>
    </div>
    <div class="work-list">
{rows}
    </div>
    <p class="small" style="margin-top:22px">Also built: a five-stage <a href="{GH}/agentic-supply-chain-operations-platform" style="text-decoration:underline;text-underline-offset:3px">multi-agent supply chain platform</a> and an <a href="{GH}/autonomous-clinical-data-pipeline" style="text-decoration:underline;text-underline-offset:3px">agentic clinical data pipeline</a>.</p>
  </div>
</section>

<section id="experience">
  <div class="wrap">
    <div class="section-head">
      <h2 class="h2">Experience</h2>
      <span class="count">2025 &ndash; present</span>
    </div>
    <div class="xp reveal">
      <div class="when">Jun 2026 &ndash; Present</div>
      <div>
        <h3>Oracle</h3>
        <div class="role">Cloud Engineering &middot; AI (L2)</div>
        <ul>
          <li>Technical scoping lead and point of contact on EMEA engagements across GPU serving, guardrails, voice AI, MCP and agentic automation.</li>
          <li>Built a three-agent ServiceNow suite for a public-sector client: natural-language search over 1M+ tickets in under 7 seconds, hybrid search over 500K+ multilingual articles, ticket creation under a minute.</li>
          <li>Built a multilingual legal and tax RAG assistant for a national tax authority, so citizens can ask questions in their own language.</li>
          <li>Delivered OCI infrastructure end to end: landing zones, networking, storage, IAM, VM migration and disaster recovery, automated with Terraform.</li>
        </ul>
      </div>
    </div>
    <div class="xp reveal">
      <div class="when">Jul 2025 &ndash; May 2026</div>
      <div>
        <h3>Oracle</h3>
        <div class="role">Cloud Solution Engineer (L1)</div>
        <ul>
          <li>Built a trademark platform for a government ministry, exposed as two APIs: similarity over 500K+ images with multilingual text and compliance rules on a CPU-only machine, and open-source image generation and editing on NVIDIA CUDA GPUs through a custom ComfyUI module.</li>
          <li>Primary developer of internal AI tools used across teams, from a document generator to a security-review agent.</li>
        </ul>
      </div>
    </div>
    <div class="xp reveal">
      <div class="when">Jan 2025 &ndash; Jul 2025</div>
      <div>
        <h3>Oracle</h3>
        <div class="role">Project Intern</div>
        <ul>
          <li>Built the Solution Document Generator on LangGraph and OKE, and a security-review agent for go-live projects.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="about">
  <div class="wrap">
    <div class="section-head">
      <h2 class="h2">About</h2>
      <span class="count">01</span>
    </div>
    <div class="split" style="padding-top:34px">
      <div class="reveal">
        <p>I work on applied AI: agentic systems, retrieval, and the serving layer under them. Most of what I ship is measured, and each project above carries its own benchmark. When something does not hold, it is reported next to the result that does.</p>
        <p>Before Oracle I studied electronics at JSS Science and Technology University, where I published on SLAM and VSLAM and hold a design patent. I still keep the research habit: state the question, fix the variables, report the interval.</p>
        <p><a href="{LI}" style="text-decoration:underline;text-underline-offset:3px">LinkedIn</a> &middot; <a href="{GH}" style="text-decoration:underline;text-underline-offset:3px">GitHub</a> &middot; <a href="{HF}" style="text-decoration:underline;text-underline-offset:3px">Hugging Face</a></p>
      </div>
      <div class="stack-grid reveal">
        <div class="stack-item"><h4>Agents &amp; RAG</h4><p>ADK, LangGraph, LangChain, Deep Agents, OpenAI SDK, MCP; hybrid retrieval, pgvector, guardrails, agent memory</p></div>
        <div class="stack-item"><h4>Inference &amp; training</h4><p>vLLM, llama.cpp, speculative decoding, FP8 KV cache, CUDA, LoRA fine-tuning, Hugging Face</p></div>
        <div class="stack-item"><h4>Cloud &amp; infrastructure</h4><p>AWS, Google Cloud, OCI (Enterprise AI, Dedicated AI Clusters, OKE, landing zones, VCN, IAM, DR), Terraform</p></div>
        <div class="stack-item"><h4>Languages &amp; DevOps</h4><p>Python, TypeScript, SQL; Linux, Docker, Kubernetes, Helm, Prometheus, CI/CD</p></div>
      </div>
    </div>
  </div>
</section>

<section id="contact" class="contact">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h2 class="display">Building something that needs to <em>work</em>?</h2>
    <p class="lede">I am open to applied AI and forward-deployed engineering roles. The fastest way to reach me is email.</p>
    <div class="contact-links">
      <a href="mailto:{EMAIL}"><span class="k">Email</span> {EMAIL}</a>
      <a href="{LI}" target="_blank" rel="noreferrer"><span class="k">LinkedIn</span> aprameyacv <span>&#8599;</span></a>
      <a href="{GH}" target="_blank" rel="noreferrer"><span class="k">GitHub</span> Aprameya-C-V <span>&#8599;</span></a>
      <a href="{HF}" target="_blank" rel="noreferrer"><span class="k">HF</span> apracv <span>&#8599;</span></a>
    </div>
  </div>
</section>
"""
    html += foot("")
    return html


def project_page(p):
    links = "".join(
        '<a class="tag" href="%s"%s>%s</a>'
        % (href if href.startswith("http") else "../" + href,
           ' target="_blank" rel="noreferrer"' if ext else "",
           label)
        for label, href, ext in p["links"]
    )
    stats = "".join(f'<div class="stat"><b>{v}</b><span>{l}</span></div>' for v, l in p["stats"])
    sections = ""
    blocks = p["sections"]
    for i, (title, body) in enumerate(blocks):
        if i == 0:
            sections += f'<div class="block prose reveal"><h2>{title}</h2>{body}</div>'
        elif i == 1:
            sections += f'<div class="block prose reveal"><h2>{title}</h2>{body}</div>'
        else:
            sections += f'<div class="block prose reveal"><h2>{title}</h2>{body}</div>'

    report = next((h for l, h, e in p["links"] if "reports/" in h), None)
    cta = (
        f'<a class="report-cta" href="../{report}">Read the full report <span class="dot">&#8599;</span></a>'
        if report
        else ""
    )

    html = head(f"{p['title']} — Aprameya C V", p["tagline"], "../")
    html += f"""
<header class="proj-head">
  <div class="wrap">
    <p class="kicker">{p['kicker']}</p>
    <h1>{p['title']}: {p['tagline']}</h1>
    <p class="sub">{p['sub']}</p>
    <div class="proj-meta">
      {''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}
      {links}
    </div>
    <div class="stats">{stats}</div>
  </div>
</header>

<div class="wrap">
  {sections}
  <div class="block reveal">
    {cta}
    <p class="small" style="margin-top:18px"><a href="../index.html#work" style="text-decoration:underline;text-underline-offset:3px">&larr; All work</a></p>
  </div>
</div>
"""
    html += foot("../")
    return html


def not_found():
    html = head("Not found — Aprameya C V", "That page does not exist.", "")
    html += """
<header class="hero" style="padding-top:clamp(140px,22vh,220px)">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1 class="display">This page is not<br><em>here</em>.</h1>
    <p class="lede">The link may be old, or the report may have moved. Everything lives from the home page.</p>
    <div class="cta-row"><a class="btn" href="/">Back to the site <span class="dot">&#8599;</span></a></div>
  </div>
</header>
"""
    html += foot("")
    return html


def extras():
    (ROOT / "404.html").write_text(not_found(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8"
    )
    urls = ["/"] + [f"/work/{p['slug']}.html" for p in PROJECTS]
    body = "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body
        + "</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n\n/assets/*\n  Cache-Control: public, max-age=604800\n",
        encoding="utf-8",
    )


def build():
    (ROOT / "index.html").write_text(home(), encoding="utf-8")
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    for p in PROJECTS:
        (work / f"{p['slug']}.html").write_text(project_page(p), encoding="utf-8")
    extras()
    print(f"wrote index.html, {len(PROJECTS)} project pages, 404, robots, sitemap")


if __name__ == "__main__":
    build()
