// dropdown.js
// Añadido por cambios de mantenimiento: maneja dropdowns de usuario (login/usuario/tienda)
// y asegura que el enlace "Hola, Inicia sesión" funcione en todas las páginas.

document.addEventListener('DOMContentLoaded', function(){
  // Delegación: manejamos clicks en elementos con clase .dropdown-toggle
  document.body.addEventListener('click', function(e){
    const toggle = e.target.closest('.dropdown-toggle');
    if(!toggle) return;
    e.preventDefault();
    // buscamos el menú hermano más cercano
    const parent = toggle.parentElement;
    if(!parent) return;
    const menu = parent.querySelector('.dropdown-menu');
    if(!menu) return;

    // Preferimos alternar la clase 'open' en el contenedor (p. ej. .dropdown-login)
    // para que los selectores CSS que usan `.dropdown-login.open .dropdown-menu`
    // funcionen correctamente en todo el código.
    const container = parent.classList.contains('dropdown-login') ? parent : menu.parentElement || parent;
    const isOpen = container.classList.contains('open');
    // cerrar otros contenedores abiertos
    document.querySelectorAll('.dropdown-login.open').forEach(function(c){ if(c !== container) c.classList.remove('open'); });
    if(isOpen){
      container.classList.remove('open');
    } else {
      container.classList.add('open');
    }
  });

  // Cerrar dropdowns al hacer click fuera
  document.addEventListener('click', function(e){
    if(e.target.closest('.dropdown-menu') || e.target.closest('.dropdown-toggle')) return;
    document.querySelectorAll('.dropdown-menu.open').forEach(function(m){ m.classList.remove('open'); });
  });

  // Cerrar con ESC
  window.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      document.querySelectorAll('.dropdown-menu.open').forEach(function(m){ m.classList.remove('open'); });
    }
  });

  // Mejora de accesibilidad: permitir foco en enlaces del dropdown con teclado
  document.querySelectorAll('.dropdown-toggle').forEach(function(t){
    t.setAttribute('role','button');
    t.setAttribute('aria-haspopup','true');
  });
});
