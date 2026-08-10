/* 全站通用：代码块右上角"一键复制"小工具
   用法：在文章里把要复制的内容包成
   <div class="code-block"><pre><code>内容</code></pre></div>
   按钮会自动出现，无需每篇单独写 JS。 */
(function () {
  'use strict';
  function copyText(txt, btn, done) {
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = txt;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, fallback);
    } else {
      fallback();
    }
  }
  function init() {
    document.querySelectorAll('.code-block').forEach(function (b) {
      if (b.querySelector('.copy-btn')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.textContent = '复制';
      btn.setAttribute('aria-label', '复制代码');
      btn.addEventListener('click', function () {
        var code = b.querySelector('code') || b;
        copyText(code.innerText, btn, function () {
          btn.textContent = '已复制 ✓';
          setTimeout(function () { btn.textContent = '复制'; }, 2000);
        });
      });
      b.insertBefore(btn, b.firstChild);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
