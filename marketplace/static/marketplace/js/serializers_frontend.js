// Frontend helpers para mantener sincronía con los serializers (validaciones, campos computados y previews)

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

window.updateUsuario = async function(id, data){
    try{
        let resp = await fetch(`/api/v1/usuarios/${id}/`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if(resp.status === 200){
            showNotification('Usuario actualizado correctamente', 'success');
            location.reload();
        }else if(resp.status === 400){
            let err = await resp.json();
            showNotification('Error de validación: ' + JSON.stringify(err), 'error');
        }else if(resp.status === 404){
            showNotification('Usuario no encontrado', 'error');
        }else{
            showNotification('Error inesperado ('+resp.status+')', 'error');
        }
    }catch(e){
        showNotification('Error de red', 'error');
    }
}

window.deleteUsuario = async function(id){
    try{
        let resp = await fetch(`/api/v1/usuarios/${id}/`, {method:'DELETE'});
        if(resp.status === 204){
            showNotification('Usuario eliminado (soft delete)', 'success');
            location.reload();
        }else if(resp.status === 404){
            showNotification('Usuario no encontrado', 'error');
        }else{
            showNotification('Error inesperado ('+resp.status+')', 'error');
        }
    }catch(e){
        showNotification('Error de red', 'error');
    }
}
document.addEventListener('DOMContentLoaded', function () {
    // Validación simple: precio > 0, stock >=0 (forms de producto si existen)
    const productForm = document.querySelector('form[data-form="producto"]');
    if (productForm) {
        productForm.addEventListener('submit', function (e) {
            const precioEl = productForm.querySelector('[name="precio"]');
            const stockEl = productForm.querySelector('[name="stock"]');
            let valid = true;
            if (precioEl) {
                const precio = parseFloat(precioEl.value || '0');
                if (!(precio > 0)) {
                    valid = false;
                    showFieldError(precioEl, 'El precio debe ser mayor a cero.');
                } else {
                    clearFieldError(precioEl);
                }
            }
            if (stockEl) {
                const stock = parseInt(stockEl.value || '0', 10);
                if (isNaN(stock) || stock < 0) {
                    valid = false;
                    showFieldError(stockEl, 'El stock no puede ser negativo.');
                } else {
                    clearFieldError(stockEl);
                }
            }
            if (!valid) e.preventDefault();
        });
    }

    // Registro de usuario: verificar passwords coinciden y email básico
    const registroForm = document.querySelector('form[data-form="registro-usuario"]');
    if (registroForm) {
        registroForm.addEventListener('submit', function (e) {
            const p1 = registroForm.querySelector('[name="password1"]');
            const p2 = registroForm.querySelector('[name="password2"]');
            const email = registroForm.querySelector('[name="email"]');
            let valid = true;
            if (p1 && p2) {
                if (p1.value !== p2.value) {
                    showFieldError(p2, 'Las contraseñas no coinciden.');
                    valid = false;
                } else {
                    clearFieldError(p2);
                }
            }
            if (email) {
                const re = /\S+@\S+\.\S+/;
                if (!re.test(email.value)) {
                    showFieldError(email, 'Ingrese un correo válido.');
                    valid = false;
                } else {
                    clearFieldError(email);
                }
            }
            if (!valid) e.preventDefault();
        });
    }

    // RUC: 11 caracteres en el formulario de tienda
    const tiendaForm = document.querySelector('form[data-form="registro-tienda"]');
    if (tiendaForm) {
        tiendaForm.addEventListener('submit', function (e) {
            const ruc = tiendaForm.querySelector('[name="ruc"]');
            if (ruc && ruc.value) {
                if (ruc.value.length !== 11) {
                    showFieldError(ruc, 'El RUC debe tener 11 caracteres.');
                    e.preventDefault();
                } else {
                    clearFieldError(ruc);
                }
            }
        });
    }

    // Mostrar preview de imágenes al subir (usuario/tienda/producto)
    document.querySelectorAll('input[type=file][data-preview]').forEach(function (inp) {
        inp.addEventListener('change', function (e) {
            const previewSel = inp.getAttribute('data-preview');
            const previewEl = document.querySelector(previewSel);
            if (!previewEl) return;
            const file = inp.files && inp.files[0];
            if (!file) return;
            const url = URL.createObjectURL(file);
            previewEl.src = url;
            previewEl.onload = function () { URL.revokeObjectURL(url); };
        });
    });

    // Botón para filtrar productos con stock bajo en panel de tienda
    const btnLowStock = document.getElementById('btn-low-stock');
    if (btnLowStock) {
        btnLowStock.addEventListener('click', function () {
            document.querySelectorAll('.productos-list .producto-item').forEach(function (el) {
                const stock = parseInt(el.getAttribute('data-stock') || '0', 10);
                if (stock <= 5) el.style.display = '';
                else el.style.display = 'none';
            });
        });
    }

    // Helpers
    function showFieldError(el, msg) {
        if (!el) return;
        el.classList.add('field-error-input');
        let next = el.nextElementSibling;
        if (!next || !next.classList.contains('field-error')) {
            next = document.createElement('div');
            next.className = 'field-error';
            el.parentNode.insertBefore(next, el.nextSibling);
        }
        next.textContent = msg;
    }
    function clearFieldError(el) {
        if (!el) return;
        el.classList.remove('field-error-input');
        let next = el.nextElementSibling;
        if (next && next.classList.contains('field-error')) next.remove();
    }
});
