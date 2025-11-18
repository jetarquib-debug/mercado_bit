document.addEventListener('DOMContentLoaded', function(){
  // Filtrado y paginación dinámica para productos
  const form = document.getElementById('filtros-form');
  if(form){
    form.addEventListener('change', function(){
      form.submit();
    });
  }
  // Ordenación de tabla de productos
  const headers = document.querySelectorAll('.productos-grid th[data-order]');
  headers.forEach(h => {
    h.addEventListener('click', function(){
      const order = h.dataset.order;
      const url = new URL(window.location.href);
      url.searchParams.set('ordering', order);
      window.location.href = url.toString();
    });
  });
  // Paginación (ejemplo básico)
  const paginadores = document.querySelectorAll('.paginador-btn');
  paginadores.forEach(btn => {
    btn.addEventListener('click', function(){
      const page = btn.dataset.page;
      const url = new URL(window.location.href);
      url.searchParams.set('page', page);
      window.location.href = url.toString();
    });
  });
  
   // Notificaciones de éxito/error para operaciones CRUD
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
  
   // Ejemplo de consumo de API RESTful con feedback
   window.createProducto = async function(data){
     try{
       let resp = await fetch('/api/v1/productos/', {
         method: 'POST',
         headers: {'Content-Type': 'application/json'},
         body: JSON.stringify(data)
       });
       if(resp.status === 201){
         showNotification('Producto creado correctamente', 'success');
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
  
   window.deleteProducto = async function(id){
     try{
       let resp = await fetch(`/api/v1/productos/${id}/`, {method:'DELETE'});
       if(resp.status === 204){
         showNotification('Producto eliminado (soft delete)', 'success');
         location.reload();
       }else if(resp.status === 404){
         showNotification('Producto no encontrado', 'error');
       }else{
         showNotification('Error inesperado ('+resp.status+')', 'error');
       }
     }catch(e){
       showNotification('Error de red', 'error');
     }
});

// --- INTEGRACIÓN EXCHANGE ---
function fetchExchange(base) {
  const indicator = document.getElementById('exchange-indicator');
  if(!indicator) return;
  indicator.style.display = 'block';
  indicator.textContent = 'Cargando tasas...';
  fetch(`/api/exchange/?base=${base}`)
    .then(r => r.json())
    .then(data => {
      if(data.error) {
        indicator.textContent = data.error;
        indicator.style.color = '#d9534f';
      } else {
        indicator.textContent = `Tasa USD/PEN: ${data.rates ? data.rates.PEN : 'N/A'}`;
        indicator.style.color = '#333';
      }
    })
    .catch(() => {
      indicator.textContent = 'Error al consultar tasas.';
      indicator.style.color = '#d9534f';
    });
}
document.addEventListener('DOMContentLoaded', function(){ fetchExchange('USD'); });
});
