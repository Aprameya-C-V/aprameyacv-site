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

# Filter group for the work index.
CATS = {
    "pramana": ("training", "Training"),
    "hbc-rag": ("retrieval", "Retrieval"),
    "speclane": ("inference", "Inference"),
    "cg-bi": ("vision", "Vision"),
    "demand-forecasting": ("mlops", "MLOps"),
}

ARROW = '<svg class="ico" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5 4h7v7M12 4 4 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_DOWN = '<svg class="ico" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M8 3v10M3.5 8.5 8 13l4.5-4.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_LEFT = '<svg class="ico" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M13 8H3M7.5 3.5 3 8l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
COPY = '<svg class="ico" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10.5 3.5v-.5a1 1 0 0 0-1-1H3.5a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'


def head(title, desc, base, page=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f3f1eb">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body{f' data-page="{page}"' if page else ''}>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><i></i></div>
<header class="bar">
  <nav class="bar-in" aria-label="Primary">
    <a class="mark" href="{base}index.html"><span class="mark-dot"></span>Aprameya C V</a>
    <div class="links">
      <a href="{base}index.html#about">About</a>
      <a href="{base}index.html#experience">Experience</a>
      <a href="{base}index.html#work">Work</a>
      <a href="{base}index.html#method">Method</a>
      <a href="{base}index.html#stack">Stack</a>
      <a href="{base}index.html#contact">Contact</a>
    </div>
    <a class="pill" href="{base}resume.pdf" target="_blank" rel="noreferrer">Resume {ARROW}</a>
  </nav>
</header>
<main id="main">
"""


def foot(base):
    return f"""</main>
<footer class="foot">
  <div class="wrap foot-in">
    <span>&copy; <span data-year>2026</span> Aprameya C V</span>
    <span class="mono">Bengaluru, India</span>
    <span class="mono">Static HTML, Cloudflare Pages</span>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite">Email copied</div>
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


LEDGER = [
    ("1,100", "+ h", 0, "Hours saved", "Internal AI tools, estimated"),
    ("80", "+", 0, "People enabled", "Codex adoption; they built 40 to 50 reusable assets"),
    ("1", "M+", 0, "Tickets searchable", "ServiceNow suite, answers in under 7 seconds"),
    ("500", "K+", 0, "Images matched", "Trademark platform, thousands of checks a week"),
]

BAND = [
    ("2.2", "x", 1, "LLM serving throughput from speculative decoding", "SpecLane"),
    ("58", "%", 0, "right clause found, up from 47%, in half the time", "HBC-RAG"),
    ("92", "%", 0, "critical defects caught at 47% of the strong model's cost", "CG-BI"),
    ("3.8", " pts", 1, "average gap between stated confidence and accuracy", "Pramana"),
]

METHOD = [
    ("Change one thing at a time", "Each study fixes the model, the prompt and the data, then varies a single setting. HBC-RAG varies passages per hop. SpecLane varies one engine flag. A difference then has one possible cause."),
    ("Score without a judge", "Character spans, exact match and held-out quality guards, not an LLM grader. Every number regenerates from saved runs, with no API spend and no judge drift."),
    ("Intervals, not single runs", "Comparisons carry paired bootstrap intervals. Anything inside the interval is called noise, including the cases where my own result is not significant."),
    ("State what it does not claim", "Every project page ends with its limits: one seed, small samples, no healthy class, one document per question. A result is only useful with its boundary."),
]

STACK = [
    ("Agents and retrieval", "ADK, LangGraph, LangChain, Deep Agents, OpenAI SDK, MCP, hybrid retrieval, pgvector, guardrails, agent memory"),
    ("Inference and training", "vLLM, llama.cpp, speculative decoding, FP8 KV cache, CUDA, NVIDIA GPUs, LoRA fine-tuning, Hugging Face"),
    ("Cloud", "OCI (Enterprise AI, Dedicated AI Clusters, Container Instances, OKE), AWS (EC2, ECS, Lambda), Google Cloud (Vertex AI, Model Garden)"),
    ("Infrastructure", "Landing zones, networking, storage, IAM, VM migration, disaster recovery, Terraform, Kubernetes, Helm, K3s, Prometheus"),
    ("Languages and tooling", "Python, TypeScript, SQL, FastAPI, Linux, Docker, CI/CD"),
]

XP = [
    ("Jun 2026 to present", "Oracle", "Cloud Engineering, AI (L2)", [
        "Technical scoping lead and point of contact on EMEA engagements across GPU serving, guardrails, voice AI, MCP and agentic automation.",
        "Built a three-agent ServiceNow suite for a public-sector client: natural-language search over 1M+ tickets in under 7 seconds, hybrid search over 500K+ multilingual articles, and ticket creation in under a minute.",
        "Built a multilingual legal and tax RAG assistant for a national tax authority, so citizens can ask questions in their own language.",
        "Delivered OCI infrastructure end to end: landing zones, networking, storage, IAM, VM migration and disaster recovery, automated with Terraform.",
        "Built deployable solution packs for RAG, agents, voice, MCP, guardrails and agent memory, and drove Codex adoption for 80+ people who built 40 to 50 reusable assets.",
    ]),
    ("Jul 2025 to May 2026", "Oracle", "Cloud Solution Engineer (L1)", [
        "Built a trademark platform for a government ministry, exposed as two APIs: similarity over 500K+ images with multilingual text and compliance rules on a CPU-only machine, and open-source image generation and editing on NVIDIA CUDA GPUs through a custom ComfyUI module.",
        "Primary developer of internal AI tools used across teams, from a document generator to a security-review agent, saving an estimated 1,100+ hours.",
    ]),
    ("Jan 2025 to Jul 2025", "Oracle", "Project Intern", [
        "Built the Solution Document Generator on LangGraph and OKE, contributing to 50+ documents and 100+ hours saved.",
    ]),
]


def ledger_rows():
    out = ""
    for i, (n, suf, dec, name, label) in enumerate(LEDGER):
        out += f"""        <li class="lrow reveal" style="--i:{i}">
          <div class="lhead"><span class="lname">{name}</span><span class="llabel">{label}</span></div>
          <div class="lvals mono"><span class="to big" data-count="{n.replace(',', '')}" data-dec="{dec}" data-suffix="{suf}" data-group="1">0{suf}</span></div>
        </li>
"""
    return out



def career_strip():
    cells = "".join(
        f"""<div class="cstat"><b class="mono" data-count="{n.replace(',', '')}" data-dec="{dec}" data-suffix="{suf}" data-group="1">0{suf}</b><span><em>{name}</em>{label}</span></div>"""
        for n, suf, dec, name, label in LEDGER
    )
    return f'<div class="cstrip reveal">{cells}</div>'


def work_rows():
    rows = ""
    for i, p in enumerate(PROJECTS):
        cat, catlabel = CATS[p["slug"]]
        rows += f"""      <a class="wrow reveal" href="work/{p['slug']}.html" data-cat="{cat}" style="--i:{i}">
        <span class="widx mono">{p['idx']}</span>
        <span class="wmain">
          <span class="wtitle">{p['title']}</span>
          <span class="wdesc">{p['row']}</span>
          <span class="wstack mono">{p['stack']}</span>
        </span>
        <span class="wmetric"><b class="mono">{p['metric_short']}</b><i class="mono">{p['metric_note']}</i></span>
        <span class="wgo">{ARROW}</span>
      </a>
"""
    return rows


def home():
    chips = '<button class="chip is-on" data-filter="all" type="button">All</button>' + "".join(
        f'<button class="chip" data-filter="{c}" type="button">{l}</button>' for c, l in
        [("inference", "Inference"), ("retrieval", "Retrieval"), ("training", "Training"), ("vision", "Vision"), ("mlops", "MLOps")]
    )
    band = "".join(
        f"""      <div class="bcell reveal" style="--i:{i}"><b class="mono" data-count="{n}" data-dec="{d}" data-suffix="{s}">0{s}</b><span>{t}</span><em class="mono">{src}</em></div>
"""
        for i, (n, s, d, t, src) in enumerate(BAND)
    )
    method = "".join(
        f"""      <div class="mitem reveal" style="--i:{i}"><span class="mno mono">0{i + 1}</span><h3>{t}</h3><p>{b}</p></div>
"""
        for i, (t, b) in enumerate(METHOD)
    )
    xp = ""
    for when, org, role, items in XP:
        lis = "".join(f"<li>{x}</li>" for x in items)
        xp += f"""      <article class="xrow reveal">
        <div class="xwhen mono">{when}</div>
        <div class="xbody"><h3>{org}<span> / {role}</span></h3><ul>{lis}</ul></div>
      </article>
"""
    stack = "".join(
        f"""      <div class="srow reveal"><h3>{h}</h3><p class="mono">{b}</p></div>
"""
        for h, b in STACK
    )

    html = head(
        "Aprameya C V, AI engineer",
        "AI engineer at Oracle building agentic and generative AI systems, and measuring what they actually do.",
        "", "home",
    )
    html += f"""
<header class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow mono"><span class="live"></span>AI engineer &middot; Oracle &middot; Bengaluru, India</p>
      <h1 class="name">Aprameya<br><span>C V</span></h1>
      <p class="role">I build agentic and generative AI systems, and measure what they actually do.</p>
      <p class="lede">I take AI from a customer's first conversation to production at Oracle: retrieval, agent design, GPU serving, and the infrastructure underneath. Every project on this site ships with its own benchmark and its own list of what it does not prove.</p>
      <div class="cta-row">
        <a class="btn" href="#work" data-magnet>See the work {ARROW_DOWN}</a>
        <a class="btn ghost" href="resume.pdf" target="_blank" rel="noreferrer" data-magnet>Resume {ARROW}</a>
      </div>
      <dl class="facts">
        <div><dt class="mono">Role</dt><dd>Cloud Engineering, AI</dd></div>
        <div><dt class="mono">At</dt><dd>Oracle, EMEA customers</dd></div>
        <div><dt class="mono">Open to</dt><dd>Applied AI, forward-deployed</dd></div>
      </dl>
    </div>
    <figure class="portrait reveal">
      <img src="assets/portrait.jpg" width="960" height="1315" alt="Portrait of Aprameya C V" fetchpriority="high">
      <figcaption class="mono"><span class="live"></span>Aprameya C V &middot; Bengaluru, India</figcaption>
    </figure>
  </div>
  <a class="scrollcue mono" href="#work" aria-label="Scroll to work">Scroll {ARROW_DOWN}</a>
</header>

<section id="about" class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="eyebrow mono">About</p><h2>Who I am</h2><p class="muted">An engineer who likes questions with a measurable answer.</p></div>
    <div class="about reveal">
      <p class="about-lead">I am an AI engineer at Oracle in Bengaluru. I joined as a project intern in January 2025, moved into a full-time engineering role that summer, and now work as a technical scoping lead for customers across EMEA.</p>
      <p>Most of my day is the gap between a prototype and something a customer can rely on: scoping the problem in the first conversation, building the agents, retrieval and serving layers, and deploying them on OCI. I have built systems for government and tax-authority clients, including multilingual assistants and image-matching APIs that run on a CPU-only machine.</p>
      <p>Outside client work I run small, controlled studies on the same questions: how many passages an agent should retrieve, which serving flag actually helps, when a cheap model should hand off to a strong one. Each is published here with its numbers and its limits.</p>
      <p>I studied electronics at JSS Science and Technology University, where I published on SLAM and hold a design patent. That is where the habit comes from: state the question, fix the variables, report the interval.</p>
    </div>
  </div>
</section>

<section id="experience" class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="eyebrow mono">01 / Experience</p><h2>Oracle</h2><p class="muted">Three roles in under two years, from intern to technical scoping lead.</p></div>
    <div>
{career_strip()}
    <div class="xlist">
{xp}    </div>
    </div>
  </div>
</section>

<section id="work" class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow mono">02 / Work</p><h2>Selected work</h2></div>
      <div class="chips" role="group" aria-label="Filter projects">{chips}</div>
    </div>
    <div class="wlist" id="wlist">
{work_rows()}    </div>
    <p class="empty" hidden>No projects in this group yet.</p>
    <p class="note">Also built: a five-stage <a href="{GH}/agentic-supply-chain-operations-platform">multi-agent supply chain platform</a>, a K3s <a href="{GH}/edge-ai-inference-engine-k3s">edge inference engine</a>, and a clinical <a href="{GH}/autonomous-clinical-data-pipeline">data pipeline</a>.</p>
  </div>
</section>

<section class="band" aria-label="Project results">
  <div class="wrap"><p class="eyebrow mono band-eyebrow">Project results</p></div>
  <div class="wrap band-grid">
{band}  </div>
</section>

<section id="method" class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="eyebrow mono">03 / Method</p><h2>How I measure</h2><p class="muted">The same four habits run through every project on this site.</p></div>
    <div class="mgrid">
{method}    </div>
  </div>
</section>

<section id="stack" class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="eyebrow mono">04 / Stack</p><h2>What I work with</h2><p class="muted">Grouped by the layer it sits in, not by logo.</p></div>
    <div class="slist">
{stack}    </div>
  </div>
</section>

<section id="education" class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="eyebrow mono">05 / Education</p><h2>Research habit</h2></div>
    <div class="edu reveal">
      <h3>JSS Science and Technology University<span> / B.E., Electronics and Communication</span></h3>
      <p class="mono edu-meta">Dec 2021 to Jun 2025 &middot; CGPA 8.93 &middot; Gold Medal</p>
      <p>Published on SLAM and VSLAM in Springer and IEEE venues and hold a design patent. I kept the research habit: state the question, fix the variables, report the interval.</p>
    </div>
  </div>
</section>

<section id="contact" class="sec contact">
  <div class="wrap">
    <p class="eyebrow mono">06 / Contact</p>
    <h2 class="contact-h">Building something that needs to work?</h2>
    <p class="lede">I am open to applied AI and forward-deployed engineering roles. Email is the fastest way to reach me.</p>
    <div class="mailrow">
      <a class="mail mono" href="mailto:{EMAIL}">{EMAIL}</a>
      <button class="copy" type="button" data-copy="{EMAIL}" aria-label="Copy email address">{COPY}<span>Copy</span></button>
    </div>
    <div class="clinks">
      <a href="{LI}" target="_blank" rel="noreferrer"><span class="mono">LinkedIn</span>aprameyacv {ARROW}</a>
      <a href="{GH}" target="_blank" rel="noreferrer"><span class="mono">GitHub</span>Aprameya-C-V {ARROW}</a>
      <a href="{HF}" target="_blank" rel="noreferrer"><span class="mono">Hugging Face</span>apracv {ARROW}</a>
      <a href="resume.pdf" target="_blank" rel="noreferrer"><span class="mono">Resume</span>PDF, one page {ARROW}</a>
    </div>
  </div>
</section>
"""
    html += foot("")
    return html


def project_page(p):
    links = "".join(
        '<a class="rlink" href="%s"%s>%s %s</a>'
        % (href if href.startswith("http") else "../" + href,
           ' target="_blank" rel="noreferrer"' if ext else "", label, ARROW)
        for label, href, ext in p["links"]
    )
    stats = "".join(
        f'<div class="pstat"><b class="mono">{v}</b><span>{l}</span></div>' for v, l in p["stats"]
    )
    toc = "".join(
        f'<a href="#s{i}">{t}</a>' for i, (t, _) in enumerate(p["sections"])
    )
    sections = ""
    for i, (title, body) in enumerate(p["sections"]):
        sections += f'<section class="pblock reveal" id="s{i}"><h2><span class="mono">0{i + 1}</span>{title}</h2><div class="prose">{body}</div></section>\n'

    idx = [q["slug"] for q in PROJECTS].index(p["slug"])
    prev_p = PROJECTS[(idx - 1) % len(PROJECTS)]
    next_p = PROJECTS[(idx + 1) % len(PROJECTS)]
    report = next((h for l, h, e in p["links"] if "reports/" in h), None)
    cta = (
        f'<a class="report-cta" href="../{report}">Read the full report {ARROW}</a>' if report else ""
    )
    tags = "".join(f'<span class="tag mono">{t}</span>' for t in p["tags"])

    html = head(f"{p['title']}, Aprameya C V", p["tagline"], "../", "project")
    html += f"""
<header class="phead">
  <div class="wrap">
    <p class="crumb mono"><a href="../index.html#work">Work</a><span>/</span>{p['idx']}</p>
    <h1>{p['title']}</h1>
    <p class="ptag">{p['tagline']}</p>
    <p class="psub">{p['sub']}</p>
    <div class="ptags">{tags}</div>
  </div>
</header>

<div class="wrap pgrid">
  <aside class="prail">
    <div class="prail-in">
      <div class="pstats">{stats}</div>
      <nav class="toc" aria-label="On this page"><span class="mono">On this page</span>{toc}</nav>
      <div class="rlinks">{links}</div>
    </div>
  </aside>
  <article class="pbody">
{sections}    <div class="pend reveal">
      {cta}
      <div class="pnav">
        <a href="../work/{prev_p['slug']}.html">{ARROW_LEFT}<span><i class="mono">Previous</i>{prev_p['title']}</span></a>
        <a class="r" href="../work/{next_p['slug']}.html"><span><i class="mono">Next</i>{next_p['title']}</span>{ARROW}</a>
      </div>
    </div>
  </article>
</div>
"""
    html += foot("../")
    return html


def not_found():
    html = head("Not found, Aprameya C V", "That page does not exist.", "", "nf")
    html += f"""
<header class="hero nf">
  <div class="wrap">
    <p class="eyebrow mono">404</p>
    <h1>This page is not here.</h1>
    <p class="lede">The link may be old, or the report may have moved. Everything is reachable from the home page.</p>
    <div class="cta-row"><a class="btn" href="/" data-magnet>Back to the site {ARROW}</a></div>
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
