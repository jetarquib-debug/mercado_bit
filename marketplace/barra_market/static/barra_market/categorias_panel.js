document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('categorias');
  const panel = document.getElementById('categorias-panel');
  if(!btn || !panel) return;

  const headerSec = document.querySelector('.header_contenedor_secundario');

  function adjustPanelPosition(){
    const inner = panel.querySelector('.categorias-panel__inner');
    if(!inner) return;
    const topOffset = headerSec ? Math.ceil(headerSec.getBoundingClientRect().bottom) : 0;
    // asegurar que el top no sea 0 si hay un header secundario
    inner.style.top = topOffset + 'px';
    inner.style.height = `calc(100vh - ${topOffset}px)`;
  }

  function openPanel(){
    panel.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    adjustPanelPosition();
  }
  function closePanel(){
    panel.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
    // limpiar estilos inline para dejar CSS por defecto
    const inner = panel.querySelector('.categorias-panel__inner');
    if(inner){ inner.style.top = ''; inner.style.height = ''; }
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
});
