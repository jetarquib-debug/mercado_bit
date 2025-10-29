document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('categorias');
  const panel = document.getElementById('categorias-panel');
  if(!btn || !panel) return;
  const headerMain = document.querySelector('.header_contenedor_secundario');
  const headerSec = document.querySelector('.header_contenedor');
  const arrow = btn.querySelector('.arrow');

  function adjustPanelPosition(){
    const inner = panel.querySelector('.categorias-panel__inner');
    if(!inner) return;
    // Calculamos la altura combinada del header principal y, si existe, el header secundario
    const topOffset = headerMain ? Math.ceil(headerMain.getBoundingClientRect().bottom) : (headerSec ? Math.ceil(headerSec.getBoundingClientRect().bottom) : 0);
    // Posicionar el panel (elemento .categorias-panel) por debajo del header para que
    // el backdrop no cubra la barra superior
    panel.style.top = topOffset + 'px';
    panel.style.height = `calc(100vh - ${topOffset}px)`;
    // El inner ocupa todo el espacio del panel
    inner.style.top = '0';
    inner.style.height = '100%';
  }

  function openPanel(){
    panel.setAttribute('aria-hidden','false');
    panel.classList.add('open');
    document.body.style.overflow = 'hidden';
    adjustPanelPosition();
    if(arrow) arrow.style.transform = 'rotate(180deg)';
  }
  function closePanel(){
    panel.setAttribute('aria-hidden','true');
    panel.classList.remove('open');
    document.body.style.overflow = '';
    // limpiar estilos inline para dejar CSS por defecto
    const inner = panel.querySelector('.categorias-panel__inner');
    if(inner){ inner.style.top = ''; inner.style.height = ''; }
    // limpiar estilos inline del panel
    panel.style.top = '';
    panel.style.height = '';
  }

  btn.addEventListener('click', function(e){
    e.preventDefault();
    const hidden = panel.getAttribute('aria-hidden') === 'true';
    if(hidden) openPanel(); else closePanel();
  });

  // cerrar al click en elementos con data-close
  panel.addEventListener('click', function(e){
    if(e.target.closest('[data-close]')) closePanel();
  });

  // cerrar con ESC
  window.addEventListener('keydown', function(e){
    if(e.key === 'Escape') closePanel();
  });

  // ajustar al redimensionar si el panel está abierto
  window.addEventListener('resize', function(){
    if(panel.getAttribute('aria-hidden') === 'false') adjustPanelPosition();
  });

  // cuando se hace click en un enlace de categoría, cerrar el panel (y permitir navegación)
  panel.addEventListener('click', function(e){
    const a = e.target.closest('a');
    if(!a) return;
    // dejamos que el enlace proceda; cerramos visualmente el panel
    closePanel();
  });
});
