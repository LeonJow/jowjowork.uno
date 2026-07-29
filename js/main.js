/* =========================================================
   JowJow — 交互：导航玻璃态 / 滚动揭示 / pinned 作品区 / 移动菜单
   ========================================================= */
(function () {
  "use strict";

  /* ---- 导航：滚动后变玻璃胶囊 ---- */
  var nav = document.getElementById("nav");
  function onNav() {
    if (window.scrollY > 40) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }

  /* ---- 移动端菜单 ---- */
  var burger = document.getElementById("navBurger");
  var links = document.getElementById("navLinks");
  if (burger) {
    burger.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("open"); });
    });
  }

  /* ---- 滚动揭示 ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in-view");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---- pinned 作品区：随滚动切换 active 卡片 ---- */
  var pin = document.getElementById("works");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".work-card"));
  var dots = Array.prototype.slice.call(document.querySelectorAll(".wp-dot"));
  var ticking = false;

  function updateWorks() {
    ticking = false;
    if (!pin || cards.length === 0) return;
    var rect = pin.getBoundingClientRect();
    var vh = window.innerHeight;
    var total = pin.offsetHeight - vh;
    var scrolled = Math.min(Math.max(-rect.top, 0), total);
    var ratio = total > 0 ? scrolled / total : 0;
    var idx = Math.min(cards.length - 1, Math.floor(ratio * cards.length));
    cards.forEach(function (c, i) { c.classList.toggle("active", i === idx); });
    dots.forEach(function (d, i) { d.classList.toggle("active", i === idx); });
  }

  function requestWorks() {
    if (!ticking) { window.requestAnimationFrame(updateWorks); ticking = true; }
  }

  /* ---- Hero 视差（轻量） ---- */
  var heroVisual = document.querySelector(".hero-visual");
  function parallax() {
    if (heroVisual && window.scrollY < window.innerHeight) {
      heroVisual.style.transform = "translateY(" + window.scrollY * 0.08 + "px)";
    }
  }

  function onScroll() {
    onNav();
    requestWorks();
    parallax();
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", updateWorks);
  onScroll();
  updateWorks();
})();
