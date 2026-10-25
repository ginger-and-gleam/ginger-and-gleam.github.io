/* Ginger & Gleam — small, dependency-free behaviour. */
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header turns solid once the hero scrolls away. */
  var head = document.querySelector('[data-head]');
  function onScrollHead() { head.classList.toggle('is-solid', window.scrollY > 24); }
  if (head) { onScrollHead(); window.addEventListener('scroll', onScrollHead, { passive: true }); }

  /* Year in the footer. */
  var y = document.querySelector('[data-year]');
  var todayCT = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Chicago', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  if (y) y.textContent = todayCT.slice(0, 4);

  /* Seasonal offers show only on their dates (US Central). */
  var season = document.querySelector('[data-season]');
  if (season) {
    var shown = 0;
    season.querySelectorAll('[data-from]').forEach(function (el) {
      var on = todayCT >= el.dataset.from && todayCT <= el.dataset.until;
      el.hidden = !on; if (on) shown++;
    });
    season.hidden = shown === 0;
  }

  /* The inspection light: surfaces stay in the dark until the light passes over them. */
  var sec = document.querySelector('[data-inspect]');
  var list = sec && sec.querySelector('[data-surfaces]');
  if (!sec || !list || reduce || !('IntersectionObserver' in window)) return;

  var items = Array.prototype.slice.call(list.children);
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var beam = document.createElement('div');
  beam.className = 'beam'; beam.setAttribute('aria-hidden', 'true');
  sec.appendChild(beam);
  sec.classList.add('lit');

  var px = null, py = null, inView = false, raf = 0, fallback = 0;
  var R = 150; /* how close the light has to come to a line */

  function see(li) { if (!li.classList.contains('is-seen')) li.classList.add('is-seen'); }

  function frame() {
    raf = 0;
    if (!inView) return;
    var s = sec.getBoundingClientRect();
    var vh = window.innerHeight;
    var bx, by;
    if (fine && px !== null) {
      bx = px; by = py;
    } else {
      var l = list.getBoundingClientRect();
      bx = l.left + Math.min(l.width * 0.35, 220); by = vh * 0.58;
    }
    beam.style.transform = 'translate(' + (bx - s.left) + 'px,' + (by - s.top) + 'px)';
    var line = vh * (fine ? 0.42 : 0.62);
    items.forEach(function (li) {
      var r = li.getBoundingClientRect();
      var cy = r.top + r.height / 2;
      var near = Math.abs(cy - by) < R && bx > r.left - R && bx < r.left + r.width + R;
      if (near || cy < line) see(li);
    });
    if (items.every(function (li) { return li.classList.contains('is-seen'); })) {
      window.removeEventListener('scroll', queue);
    }
  }
  function queue() { if (!raf) raf = requestAnimationFrame(frame); }

  new IntersectionObserver(function (entries) {
    inView = entries[0].isIntersecting;
    sec.classList.toggle('is-beaming', inView && (!fine || px !== null));
    if (inView) {
      queue();
      /* Nobody misses the list: after a while in view, everything is lit. */
      if (!fallback) fallback = setTimeout(function () {
        items.forEach(function (li, i) { setTimeout(function () { see(li); }, i * 140); });
      }, 9000);
    }
  }, { threshold: 0.05 }).observe(sec);

  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue);
  if (fine) {
    sec.addEventListener('pointermove', function (e) { px = e.clientX; py = e.clientY; sec.classList.add('is-beaming'); queue(); });
    sec.addEventListener('pointerleave', function () { px = null; sec.classList.remove('is-beaming'); });
  }
})();
