document.addEventListener('DOMContentLoaded', function(){

  function showNotification(message, type='info'){
    let notif = document.createElement('div');
    notif.className = 'notif notif-' + type;
    notif.textContent = message;
    notif.style.position = 'fixed';
    notif.style.top = '24px';
    notif.style.right = '24px';
    notif.style.zIndex = '9999';
    notif.style.padding = '12px 24px';
    notif.style.borderRadius = '8px';
    notif.style.background = type==='error' ? '#d9534f' : '#5cb85c';
    notif.style.color = '#fff';
    document.body.appendChild(notif);
    setTimeout(()=> notif.remove(), 3500);
  }

  window.createTienda = async function(data){
    try{
      let resp = await fetch('/api/v1/tiendas/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      if(resp.status === 201){
        showNotification('Tienda creada correctamente', 'success');
        location.reload();
      }else if(resp.status === 400){
        let err = await resp.json();
        showNotification('Error de validación: ' + JSON.stringify(err), 'error');
      }else{
        showNotification('Error inesperado ('+resp.status+')', 'error');
      }
    }catch(e){
      showNotification('Error de red', 'error');
    }
  }

  window.updateTienda = async function(id, data){
    try{
      let resp = await fetch(`/api/v1/tiendas/${id}/`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      if(resp.status === 200){
        showNotification('Tienda actualizada correctamente', 'success');
        location.reload();
      }else if(resp.status === 400){
        let err = await resp.json();
        showNotification('Error de validación: ' + JSON.stringify(err), 'error');
      }else if(resp.status === 404){
        showNotification('Tienda no encontrada', 'error');
      }else{
        showNotification('Error inesperado ('+resp.status+')', 'error');
      }
    }catch(e){
      showNotification('Error de red', 'error');
    }
  }

  window.deleteTienda = async function(id){
    try{
      let resp = await fetch(`/api/v1/tiendas/${id}/`, {method:'DELETE'});
      if(resp.status === 204){
        showNotification('Tienda eliminada (soft delete)', 'success');
        location.reload();
      }else if(resp.status === 404){
        showNotification('Tienda no encontrada', 'error');
      }else{
        showNotification('Error inesperado ('+resp.status+')', 'error');
      }
    }catch(e){
      showNotification('Error de red', 'error');
    }
  }
  const nav = document.querySelector('.comercial-nav');
  const buttons = nav ? Array.from(nav.querySelectorAll('button')) : [];
  const panels = document.querySelectorAll('.comercial-main .panel');

  function showPanel(name){
    panels.forEach(p => {
      if(p.dataset.panel === name){ p.hidden = false; } else { p.hidden = true; }
    });
    buttons.forEach(b => b.classList.toggle('active', b.dataset.action === name));
  }

  if(buttons.length){
    buttons.forEach(b => b.addEventListener('click', ()=> showPanel(b.dataset.action)));
    // default
    showPanel('info');
  }

  // Stock: export CSV
  const btnExport = document.getElementById('btn-export-csv');
  if(btnExport){
    btnExport.addEventListener('click', ()=>{
      // generar CSV simple en el navegador a partir de los productos en DOM
      const items = Array.from(document.querySelectorAll('.p-card'));
      if(items.length === 0){ alert('No hay productos para exportar.'); return; }
      const rows = [['Nombre','Precio','Stock','Estado']];
      items.forEach(it => {
        const name = it.querySelector('h3') ? it.querySelector('h3').innerText.trim() : '';
        const price = it.querySelector('.p-meta') ? it.querySelector('.p-meta').innerText.split('—')[0].replace('S/.','').trim() : '';
        const stock = it.querySelector('.p-stock') ? it.querySelector('.p-stock').innerText.replace('Stock:','').trim() : '';
        const estado = it.querySelector('.p-meta') ? it.querySelector('.p-meta').innerText.split('—')[1] ? it.querySelector('.p-meta').innerText.split('—')[1].trim() : '' : '';
        rows.push([name,price,stock,estado]);
      });
      const csv = rows.map(r => r.map(c => '"'+String(c).replace(/"/g,'""')+'"').join(',')).join('\n');
      const blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a'); a.href = url; a.download = 'inventario.csv'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    });
  }

  const btnLow = document.getElementById('btn-low-stock');
  if(btnLow){
    btnLow.addEventListener('click', ()=>{
      const list = document.getElementById('low-stock-list');
      if(!list) return;
      list.innerHTML = '';
      const items = Array.from(document.querySelectorAll('.p-card'));
      const low = items.filter(it => {
        const s = it.querySelector('.p-stock') ? parseInt(it.querySelector('.p-stock').innerText.replace(/[^0-9]/g,'')) : 0; return s > 0 && s <= 5;
      });
      if(low.length===0){ list.innerHTML = '<p>No hay productos con stock bajo (<=5).</p>'; list.hidden = false; return; }
      low.forEach(it => {
        const name = it.querySelector('h3').innerText.trim();
        const stock = it.querySelector('.p-stock').innerText.replace('Stock:','').trim();
        const div = document.createElement('div'); div.className = 'low-stock-item'; div.innerHTML = `<span>${name}</span><strong>${stock}</strong>`; list.appendChild(div);
      });
      list.hidden = false;
    });
  }

  // Oferta buttons (placeholders)
  const btnCrearOferta = document.getElementById('btn-crear-oferta');
  if(btnCrearOferta){ btnCrearOferta.addEventListener('click', ()=> alert('Crear oferta - funcionalidad no implementada aún.')); }
  const btnVerOfertas = document.getElementById('btn-ver-ofertas');
  if(btnVerOfertas){ btnVerOfertas.addEventListener('click', ()=> alert('Ver ofertas - funcionalidad no implementada aún.')); }

});
