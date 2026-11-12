/* JowJoWork 全站共用脚本 */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 滚动进场 · 错峰 */
  var rises = [].slice.call(document.querySelectorAll('.rise'));
  if (reduced || !('IntersectionObserver' in window)) {
    rises.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -36px 0px' });
    rises.forEach(function (el) { io.observe(el); });
  }

  /* 顶部进度条 */
  var bar = document.getElementById('bar');
  if (bar) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    };
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  }

  /* 当前区块高亮：只在有页内锚点的页面生效 */
  var links = [].slice.call(document.querySelectorAll('nav a'));
  var targets = links.map(function (a) {
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '#') return null;
    var el = document.querySelector(href);
    return el ? { a: a, el: el } : null;
  }).filter(Boolean).sort(function (x, y) { return x.el.offsetTop - y.el.offsetTop; });

  if (targets.length) {
    var sync = function () {
      var y = window.scrollY + 140, idx = 0;
      targets.forEach(function (t, i) { if (t.el.offsetTop <= y) idx = i; });
      links.forEach(function (a) { a.classList.remove('on'); });
      if (targets[idx]) targets[idx].a.classList.add('on');
    };
    window.addEventListener('scroll', sync, { passive: true });
    sync();
  }
})();
