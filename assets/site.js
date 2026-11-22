const io = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      }
    }
  },
  { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
);

for (const el of document.querySelectorAll(".reveal")) io.observe(el);

const nav = document.querySelector(".nav");
if (nav) {
  const onScroll = () => {
    const y = window.scrollY;
    nav.style.transform = `translateX(-50%) translateY(${y > 40 ? "-2px" : "0"})`;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
}

const year = document.querySelector("[data-year]");
if (year) year.textContent = new Date().getFullYear();
