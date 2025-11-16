// JS separado para generar transaccion_id, sincronizar monto y manejar UX de envío
(function(){
  // Genera una referencia única simple para la transacción
  function generarTransaccionId(){
    const t = Date.now().toString(36);
    const r = Math.random().toString(36).slice(2,8);
    return 'TX-' + t + '-' + r;
  }

  document.addEventListener('DOMContentLoaded', function(){
    const transInput = document.getElementById('pago-transaccion_id');
    const transVisible = document.getElementById('transaccion-visible');
    const montoInput = document.getElementById('pago-monto');
    const montoVisible = document.getElementById('monto-visible');
    const form = document.querySelector('.pago-form');
    const btn = document.getElementById('btn-pagar');
    const estado = document.getElementById('pago-estado');

    if(transInput && transVisible){
      const id = generarTransaccionId();
      transInput.value = id;
      transVisible.value = id;
    }

    // Asegurar que el monto visible coincida con el input (por si se pasa como string con coma)
    if(montoInput && montoVisible){
      montoVisible.textContent = montoInput.value;
    }

    // Manejo simple de envío para mostrar estado (no reemplaza procesamiento en servidor)
    if(form){
      form.addEventListener('submit', function(e){
        // validaciones básicas
        const metodo = document.getElementById('metodo-select');
        if(!metodo || !metodo.value){
          e.preventDefault();
          estado.textContent = 'Por favor seleccione un método de pago.';
          metodo && metodo.focus();
          return;
        }

        // mostrar loader/estado y permitir que el POST continúe
        btn.classList.add('loading');
        btn.setAttribute('disabled', 'disabled');
        estado.textContent = 'Procesando pago...';

        // Si deseas manejar por AJAX, intercepta aquí y evita que el formulario se envíe.
      });
    }
  });
})();
