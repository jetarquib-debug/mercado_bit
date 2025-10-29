document.addEventListener('DOMContentLoaded', function () {
  const wrapper = document.querySelector('.categorias-track-wrapper');
  const track = document.querySelector('.categorias-track');
  const prevBtn = document.querySelector('.cat-prev');
  const nextBtn = document.querySelector('.cat-next');
  if (!wrapper || !track) return;

  // Agrupar items (ya están envueltos en .categoria-item)
  let items = Array.from(track.children);
  const originalCount = items.length;
  if (originalCount === 0) return;

  // Duplicar contenido para efecto infinito
  track.innerHTML = track.innerHTML + track.innerHTML;
  let allItems = Array.from(track.children);

  // Medición precisa del ancho entre dos items (incluye gap)
  function measureItemWidth() {
    const first = allItems[0];
    const second = allItems[1];
    if (!first) return 0;
    if (!second) return first.getBoundingClientRect().width;
    const r1 = first.getBoundingClientRect();
    const r2 = second.getBoundingClientRect();
    return Math.abs(r2.left - r1.left);
  }

  let itemWidth = measureItemWidth();
  let position = 0; // px desplazados desde el inicio
  let intervalMs = 5000;
  let timer = null;
  let transitioning = false;

  function setTransition(enabled) {
    if (enabled) {
      track.classList.add('transitioning');
    } else {
      track.classList.remove('transitioning');
    }
  }

  function slideLeft() {
    if (transitioning) return;
    itemWidth = measureItemWidth() || itemWidth;
    if (!itemWidth) return;
    transitioning = true;
    setTransition(true);
    position += itemWidth;
    track.style.transform = `translateX(-${position}px)`;

    const onEnd = function (e) {
      if (e.propertyName && e.propertyName !== 'transform') return;
      const cycle = itemWidth * originalCount;
      if (position >= cycle) {
        // quitar transición, ajustar al inicio equivalente y forzar reflow para continuar suave
        setTransition(false);
        position = position - cycle;
        track.style.transform = `translateX(-${position}px)`;
        void track.offsetWidth;
      }
      transitioning = false;
    };

    track.addEventListener('transitionend', onEnd, { once: true });
  }

  function slideRight() {
    if (transitioning) return;
    itemWidth = measureItemWidth() || itemWidth;
    if (!itemWidth) return;
    transitioning = true;
    // Si estamos al inicio, saltamos al final del bloque duplicado para mover hacia atrás
    if (position === 0) {
      setTransition(false);
      position = itemWidth * originalCount;
      track.style.transform = `translateX(-${position}px)`;
      // forzar reflow
      void track.offsetWidth;
    }

    setTransition(true);
    position -= itemWidth;
    track.style.transform = `translateX(-${position}px)`;

    const onEnd = function (e) {
      if (e.propertyName && e.propertyName !== 'transform') return;
      transitioning = false;
    };
    track.addEventListener('transitionend', onEnd, { once: true });
  }

  function startAuto() {
    stopAuto();
    timer = setInterval(slideLeft, intervalMs);
  }
  function stopAuto() { if (timer) { clearInterval(timer); timer = null; } }

  // Botones
  if (nextBtn) nextBtn.addEventListener('click', () => { slideLeft(); startAuto(); });
  if (prevBtn) prevBtn.addEventListener('click', () => { slideRight(); startAuto(); });

  // Pausar al hover
  wrapper.addEventListener('mouseenter', stopAuto);
  wrapper.addEventListener('mouseleave', startAuto);

  // Recalcular anchos al redimensionar
  window.addEventListener('resize', () => {
    // recalcular ancho del item (puede cambiar por media queries o gaps)
    allItems = Array.from(track.children);
    itemWidth = measureItemWidth();
    // Normalizar posición para que no se salga del bloque original
    const cycle = itemWidth * originalCount;
    if (cycle > 0) {
      position = position % cycle;
      track.style.transition = 'none';
      track.style.transform = `translateX(-${position}px)`;
      // forzar reflow
      void track.offsetWidth;
      track.classList.remove('transitioning');
    }
  });

  // Init
  track.style.transform = 'translateX(0px)';
  startAuto();
});
