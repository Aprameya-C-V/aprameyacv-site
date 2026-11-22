(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Reveal on scroll, with count-up for [data-count].
  const count = (el) => {
    const to = parseFloat(el.dataset.count);
    const dec = parseInt(el.dataset.dec || "0", 10);
    const suf = el.dataset.suffix || "";
    if (reduce) { el.textContent = to.toFixed(dec) + suf; return; }
    let t0 = null;
    const step = (t) => {
      if (t0 === null) t0 = t;
      const p = Math.min((t - t0) / 1100, 1);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = (to * e).toFixed(dec) + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const el = entry.target;
      el.classList.add("in");
      el.querySelectorAll("[data-count]").forEach(count);
      io.unobserve(el);
    }
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Reading progress bar.
  const bar = document.querySelector(".progress i");
  if (bar) {
    let ticking = false;
    const update = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.transform = `scaleX(${max > 0 ? Math.min(h.scrollTop / max, 1) : 0})`;
      ticking = false;
    };
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // Active section in nav and in the project table of contents.
  const spy = (links, targets) => {
    if (!links.length || !targets.length) return;
    const so = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        links.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href").endsWith("#" + e.target.id)));
      }
    }, { rootMargin: "-35% 0px -55% 0px" });
    targets.forEach((t) => so.observe(t));
  };
  spy([...document.querySelectorAll(".links a")], [...document.querySelectorAll("main section[id]")]);
  spy([...document.querySelectorAll(".toc a")], [...document.querySelectorAll(".pblock[id]")]);

  // Work filter.
  const chips = [...document.querySelectorAll(".chip")];
  const rows = [...document.querySelectorAll(".wrow")];
  const empty = document.querySelector(".empty");
  chips.forEach((chip) => chip.addEventListener("click", () => {
    const f = chip.dataset.filter;
    chips.forEach((c) => c.classList.toggle("is-on", c === chip));
    let shown = 0;
    rows.forEach((r) => {
      const on = f === "all" || r.dataset.cat === f;
      r.hidden = !on;
      if (on) { shown += 1; r.classList.add("in"); }
    });
    if (empty) empty.hidden = shown !== 0;
  }));

  // Copy email.
  const toast = document.querySelector(".toast");
  document.querySelectorAll("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(btn.dataset.copy); } catch (_) { return; }
    if (!toast) return;
    toast.classList.add("on");
    setTimeout(() => toast.classList.remove("on"), 1800);
  }));

  // Gentle magnetic pull on primary buttons (pointer devices only).
  if (!reduce && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("[data-magnet]").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - (r.left + r.width / 2)) * 0.18;
        const y = (e.clientY - (r.top + r.height / 2)) * 0.28;
        el.style.transform = `translate(${x}px, ${y}px)`;
      });
      el.addEventListener("pointerleave", () => { el.style.transform = ""; });
    });
  }

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
})();
