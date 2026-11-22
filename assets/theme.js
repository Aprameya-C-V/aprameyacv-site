/* Sets the theme before first paint: a saved choice wins, otherwise the system preference. */
(function () {
  var t = null;
  try { t = localStorage.getItem("theme"); } catch (e) {}
  if (t !== "light" && t !== "dark") {
    t = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  document.documentElement.setAttribute("data-theme", t);
  var m = document.querySelector('meta[name="theme-color"]');
  if (m) m.setAttribute("content", t === "dark" ? "#11130f" : "#f3f1eb");
})();
