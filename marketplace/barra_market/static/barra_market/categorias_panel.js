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
    // Intentar calcular la altura del header de forma robusta usando la variable CSS
    // `--header-height` (si existe) y sumando la altura real de la barra secundaria
    let headerHeightPx = 0;
    try{
      const rootStyles = getComputedStyle(document.documentElement);
      const v = rootStyles.getPropertyValue('--header-height');
      if(v){ headerHeightPx = parseInt(v.trim().replace('px','')) || 0; }
    }catch(e){ headerHeightPx = 0; }
    // fallback: medir el elemento si la variable no está presente
    if(!headerHeightPx && headerSec) headerHeightPx = headerSec.offsetHeight || 0;
    const secondaryHeight = headerMain ? (headerMain.offsetHeight || 0) : 0;
    const topOffset = headerHeightPx + secondaryHeight;

    // Posicionar el panel (elemento .categorias-panel) por debajo del header y la barra secundaria
    panel.style.top = topOffset + 'px';
    panel.style.height = `calc(100vh - ${topOffset}px)`;

    // Asegurar que el inner ocupe todo el alto disponible y comience en la parte superior
    inner.style.top = '0';
    inner.style.height = '100%';
    inner.style.marginTop = '0';
    // resetear scroll para que el contenido siempre empiece visible desde arriba
    inner.scrollTop = 0;
  }

  function openPanel(){
    panel.setAttribute('aria-hidden','false');
    panel.classList.add('open');
    document.body.style.overflow = 'hidden';
    adjustPanelPosition();
    if(arrow) arrow.style.transform = 'rotate(180deg)';
    // marcar el botón como abierto para permitir rotación vía CSS tambien
    if(btn) btn.classList.add('open');
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
    // resetear rotación y clase del botón
    if(arrow) arrow.style.transform = '';
    if(btn) btn.classList.remove('open');
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

  // Si el panel no contiene categorías (por ejemplo, el context processor falló),
  // solicitamos los datos al endpoint JSON y rellenamos la lista dinámicamente.
  function fetchAndRenderIfEmpty(){
    const categoriasList = panel.querySelector('.categorias-list');
    const marcasList = panel.querySelector('.marcas-list');
    const hasCategorias = categoriasList && categoriasList.querySelectorAll('li').length > 0 && categoriasList.textContent.trim() !== '(No hay categorías)';
    const hasMarcas = marcasList && marcasList.querySelectorAll('li').length > 0 && marcasList.textContent.trim() !== '(No hay marcas)';
    if(hasCategorias && hasMarcas) return; // ya está poblado
    // fallback AJAX con indicador de carga y preservando el parámetro `q` si existe
    // Crear indicador de carga si no existe
    let loader = panel.querySelector('.categorias-loader');
    if(!loader){
      loader = document.createElement('div');
      loader.className = 'categorias-loader';
      loader.innerHTML = '<div class="spinner" aria-hidden="true"></div>';
      const inner = panel.querySelector('.categorias-panel__inner');
      if(inner) inner.appendChild(loader);
    }
    loader.style.display = 'flex';

    function getQParam(){
      try{
        const params = new URLSearchParams(window.location.search);
        const q = params.get('q');
        return q ? q : null;
      }catch(e){ return null; }
    }

    const currentQ = getQParam();

    fetch('/api/categorias/')
      .then(function(res){ if(!res.ok) throw new Error('Network response not ok'); return res.json(); })
      .then(function(data){
        if(!categoriasList || !marcasList) return;
        categoriasList.innerHTML = '';
        marcasList.innerHTML = '';
        if(data.categorias && data.categorias.length){
          data.categorias.forEach(function(c){
            const li = document.createElement('li');
            li.className = 'categorias-list__item';
            const a = document.createElement('a');
            // preservamos q si existe
            let href = '/producto/lista/?categoria=' + encodeURIComponent(c.id);
            if(currentQ){ href = '/producto/lista/?q=' + encodeURIComponent(currentQ) + '&categoria=' + encodeURIComponent(c.id); }
            a.href = href;
            a.textContent = c.nomb_ca;
            li.appendChild(a);
            categoriasList.appendChild(li);
          });
        } else {
          const li = document.createElement('li'); li.className='categorias-list__item'; li.textContent='(No hay categorías)'; categoriasList.appendChild(li);
        }

        if(data.marcas && data.marcas.length){
          data.marcas.forEach(function(m){
            const li = document.createElement('li');
            li.className = 'marcas-list__item';
            const a = document.createElement('a');
            let href = '/producto/lista/?marca=' + encodeURIComponent(m.id);
            if(currentQ){ href = '/producto/lista/?q=' + encodeURIComponent(currentQ) + '&marca=' + encodeURIComponent(m.id); }
            a.href = href;
            a.textContent = m.nomb_marca;
            li.appendChild(a);
            marcasList.appendChild(li);
          });
        } else {
          const li = document.createElement('li'); li.textContent='(No hay marcas)'; marcasList.appendChild(li);
        }
      })
      .catch(function(){
        // silencioso: mantener el markup actual si falla
      })
      .finally(function(){ if(loader) loader.style.display = 'none'; });
  }

  // Llamar cuando se abre el panel
  const originalOpen = openPanel;
  openPanel = function(){
    fetchAndRenderIfEmpty();
    return originalOpen();
  };
});
