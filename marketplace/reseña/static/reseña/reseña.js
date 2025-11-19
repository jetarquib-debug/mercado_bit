// Envío AJAX del formulario de reseña hacia el endpoint DRF `/api/resenas/`.
// Uso: el formulario debe tener la clase `.resena-form` y atributos
// data-product-id y data-authenticated (1 o 0).

document.addEventListener('DOMContentLoaded', function () {
	const form = document.querySelector('.resena-form');
	if (!form) return;

	// Obtener CSRF token desde la cookie (función sencilla)
	function getCookie(name) {
		const value = '; ' + document.cookie;
		const parts = value.split('; ' + name + '=');
		if (parts.length === 2) return parts.pop().split(';').shift();
		return null;
	}

	form.addEventListener('submit', function (e) {
		e.preventDefault();

		const productId = form.dataset.productId;
		const isAuthenticated = form.dataset.authenticated === '1';
		const puntuacionInput = form.querySelector('input[name="puntuacion"]:checked');
		const comentario = (form.querySelector('textarea[name="comentario"]') || { value: '' }).value.trim();

		if (!puntuacionInput) {
			alert('Por favor selecciona una puntuación (1-5).');
			return;
		}

		const payload = {
			producto: parseInt(productId, 10),
			puntuacion: parseInt(puntuacionInput.value, 10),
			comentario: comentario || '',
		};

		const csrftoken = getCookie('csrftoken');

		fetch('/api/resenas/', {
			method: 'POST',
			credentials: 'same-origin',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken || '',
				'Accept': 'application/json',
			},
			body: JSON.stringify(payload),
		}).then(async res => {
			if (res.status === 201 || res.status === 200) {
				const data = await res.json();
				const lista = document.querySelector('.lista-resenas');
				const contador = document.querySelector('.resenas-list h3');

				// Construir LI
				const li = document.createElement('li');
				li.className = 'resena-item';
				const autor = isAuthenticated ? (data.usuario_email || 'Tú') : (data.usuario_email || 'Anónimo');
				const fecha = new Date(data.fecha_creacion).toLocaleString();
				const estrellas = '★'.repeat(data.puntuacion) + '☆'.repeat(5 - data.puntuacion);
				li.innerHTML = `\
					<div class="cabecera"><strong class="autor">${autor}</strong><span class="fecha"> · ${fecha}</span></div>\
					<div class="puntuacion">${estrellas}</div>\
					${data.comentario ? `<div class="comentario">${data.comentario}</div>` : ''}`;

				if (lista) {
					if (lista.querySelector('.sin-resenas')) lista.innerHTML = '';
					lista.insertBefore(li, lista.firstChild);
				}

				if (contador) {
					const match = (contador.textContent || '').match(/\((\d+)\)/);
					let total = 1;
					if (match) total = parseInt(match[1], 10) + 1;
					contador.textContent = `Reseñas (${total})`;
				}

				form.reset();
				// Opcional: mostrar mensaje breve
				const prev = document.querySelector('.resena-toast');
				if (prev) prev.remove();
				const toast = document.createElement('div');
				toast.className = 'resena-toast';
				toast.textContent = 'Reseña enviada correctamente.';
				toast.style.position = 'fixed';
				toast.style.right = '20px';
				toast.style.bottom = '20px';
				toast.style.background = '#2575fc';
				toast.style.color = '#fff';
				toast.style.padding = '10px 14px';
				toast.style.borderRadius = '8px';
				document.body.appendChild(toast);
				setTimeout(() => toast.remove(), 3000);
			} else if (res.status === 400) {
				const err = await res.json().catch(() => ({}));
				alert('Error al enviar la reseña: ' + (err.detail || JSON.stringify(err)));
			} else if (res.status === 403 || res.status === 401) {
				alert('Necesitas iniciar sesión para enviar reseñas.');
			} else {
				const text = await res.text();
				alert('Error inesperado: ' + res.status + '\n' + text);
			}
		}).catch(err => {
			console.error(err);
			alert('Error de red al enviar la reseña.');
		});
	});
});

