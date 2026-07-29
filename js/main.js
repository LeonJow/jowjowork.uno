/* =========================================================
   JowJow — 交互：导航玻璃态 / 滚动揭示 / 文字逐行揭示 /
    pinned 作品区 / 移动菜单 / 滚动进度条 / 卡片 3D 倾斜
   ========================================================= */
(function () {
  "use strict";

  /* ---- 导航：滚动后变玻璃胶囊 ---- */
  var nav = document.getElementById("nav");
  function onNav() {
    if (window.scrollY > 40) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }

  /* ---- 首屏滚动进度条（高仿 decart） ---- */
  var progress = document.getElementById("scrollProgress");
  function updateProgress() {
    if (!progress) return;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var r = h > 0 ? window.scrollY / h : 0;
    progress.style.transform = "scaleX(" + Math.min(1, Math.max(0, r)) + ")";
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

  /* ---- 滚动揭示 + 文字逐行揭示 ---- */
  var reveals = document.querySelectorAll(".reveal, .reveal-lines");
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
    cards.forEach(function (c, i) {
      c.classList.toggle("active", i === idx);
      if (i !== idx) { c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg"); }
    });
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
    updateProgress();
    requestWorks();
    parallax();
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { updateWorks(); updateProgress(); });
  onScroll();
  updateWorks();

  /* ---- 卡片 3D 倾斜（高仿 decart，仅桌面鼠标设备，尊重 reduced-motion） ---- */
  function initTilt() {
    var fine = window.matchMedia("(hover:hover) and (pointer:fine)").matches;
    var reduce = window.matchMedia("(prefers-reduced-motion:reduce)").matches;
    if (!fine || reduce) return;

    // 普通卡片：数据/能力/理念/hero 卡
    var els = document.querySelectorAll(".stat, .card, .idea, .hero-card");
    els.forEach(function (el) {
      el.classList.add("tilt");
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform =
          "perspective(800px) rotateX(" + (-py * 8).toFixed(2) + "deg) rotateY(" +
          (px * 10).toFixed(2) + "deg) translateY(-4px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });

    // 作品卡：仅 active 时倾斜（用 CSS 变量，不破坏 pinned 切换动画）
    cards.forEach(function (c) {
      c.addEventListener("mouseenter", function () { c.classList.add("tilting"); });
      c.addEventListener("mousemove", function (e) {
        if (!c.classList.contains("active")) return;
        var r = c.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        c.style.setProperty("--rx", (-py * 6).toFixed(2) + "deg");
        c.style.setProperty("--ry", (px * 8).toFixed(2) + "deg");
      });
      c.addEventListener("mouseleave", function () {
        c.classList.remove("tilting");
        c.style.setProperty("--rx", "0deg");
        c.style.setProperty("--ry", "0deg");
      });
    });
  }
  initTilt();
})();
