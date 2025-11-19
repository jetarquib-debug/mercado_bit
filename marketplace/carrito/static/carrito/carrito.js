/* carrito.js
   Manage cart stored in localStorage and render cart page; also listens for add-to-cart clicks.
*/
(function(){
  function readCart(){
    try{ return JSON.parse(localStorage.getItem('mb_cart')||'[]'); }catch(e){ return []; }
  }
  function writeCart(cart){ localStorage.setItem('mb_cart', JSON.stringify(cart)); updateBadge(); }

  function updateBadge(){
    const cart = readCart();
    const count = cart.reduce((s,i)=> s + (i.qty||0), 0);
    const badge = document.getElementById('cart-count');
    if(badge){ badge.innerText = count; badge.style.display = count>0 ? 'inline-block' : 'none'; }
  }

  function findItem(cart, id){ return cart.find(i=> String(i.id) === String(id)); }

  // handle add to cart buttons across site
  function handleAddButton(e){
    const btn = e.target.closest('.add-to-cart');
    if(!btn) return;
    const id = btn.dataset.id; const name = btn.dataset.name; const price = parseFloat(btn.dataset.price||0);
    const image = btn.dataset.image || null;
    const quantity = Math.max(1, parseInt(btn.dataset.quantity||btn.getAttribute('data-quantity')||1, 10) || 1);
    if(!id) return;
    const cart = readCart();
    let item = findItem(cart, id);
    if(item){ item.qty = (item.qty||1) + quantity; }
    else { cart.push({ id: id, name: name, price: price, qty: quantity }); }
    // attach image if provided
    if(image){ const it = findItem(cart,id); if(it) it.image = image; }
    writeCart(cart);
    // small feedback showing quantity added + animation
    const prevText = btn.getAttribute('data-prev-text') || btn.innerText;
    const addedText = `Añadido (${quantity}) ✓`;
    btn.setAttribute('data-prev-text', prevText);
    btn.innerText = addedText;
    // add a transient class to animate the button
    btn.classList.add('added-animate');
    setTimeout(()=>{ btn.innerText = prevText; btn.classList.remove('added-animate'); }, 900);
  }

  // Render cart page items
  function renderCartPage(){
    const container = document.getElementById('cart-items');
    if(!container) return;
    const cart = readCart();
    container.innerHTML = '';
    if(cart.length===0){ container.innerHTML = '<div class="empty-cart"><p>Tu carrito está vacío.</p><p><a href="/">Seguir comprando</a></p></div>'; updateSummary(); return; }
    cart.forEach(it => {
      const el = document.createElement('div'); el.className = 'cart-item';
      el.dataset.id = it.id;
      const imgSrc = it.image || '/media/productos_imagenes/default_producto.png';
      el.innerHTML = `
        <img src="${imgSrc}" alt="${escapeHtml(it.name)}">
        <div class="item-body">
          <p class="item-title">${escapeHtml(it.name)}</p>
          <div class="item-meta">S/. ${Number(it.price).toFixed(2)}</div>
          <div style="margin-top:0.5rem; display:flex; gap:1rem; align-items:center;">
            <div class="qty-controls">
              <button class="qty-decrease" aria-label="Disminuir">−</button>
              <div class="qty-number">${it.qty}</div>
              <button class="qty-increase" aria-label="Aumentar">+</button>
            </div>
            <button class="btn btn-small btn-remove">Eliminar</button>
          </div>
        </div>
        <div class="item-subtotal">S/. ${(Number(it.price)*it.qty).toFixed(2)}</div>
      `;
      container.appendChild(el);
    });
    attachCartHandlers(); updateSummary();
  }

  function attachCartHandlers(){
    document.querySelectorAll('.qty-increase').forEach(b=> b.addEventListener('click', function(){
      const itemEl = this.closest('.cart-item'); const id = itemEl.dataset.id; const cart = readCart(); const it = findItem(cart,id); if(it){ it.qty = (it.qty||1)+1; writeCart(cart); renderCartPage(); }
    }));
    document.querySelectorAll('.qty-decrease').forEach(b=> b.addEventListener('click', function(){
      const itemEl = this.closest('.cart-item'); const id = itemEl.dataset.id; const cart = readCart(); const it = findItem(cart,id); if(it){ it.qty = Math.max(1,(it.qty||1)-1); writeCart(cart); renderCartPage(); }
    }));
    document.querySelectorAll('.btn-remove').forEach(b=> b.addEventListener('click', function(){
      const itemEl = this.closest('.cart-item'); const id = itemEl.dataset.id; let cart = readCart(); cart = cart.filter(i=> String(i.id)!==String(id)); writeCart(cart); renderCartPage();
    }));
  }

  function updateSummary(){
    const cart = readCart(); const count = cart.reduce((s,i)=> s + (i.qty||0), 0); const total = cart.reduce((s,i)=> s + (i.qty||0)*Number(i.price||0), 0);
    const sc = document.getElementById('summary-count'); const st = document.getElementById('summary-total'); if(sc) sc.innerText = count; if(st) st.innerText = 'S/. '+ total.toFixed(2);
  }

  function escapeHtml(text){ return String(text).replace(/[&<>"']/g, function(ch){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]; }); }

  // Checkout/clear
  function attachSummaryButtons(){
    const btnClear = document.getElementById('btn-clear'); if(btnClear) btnClear.addEventListener('click', ()=>{ if(confirm('Vaciar carrito?')){ writeCart([]); renderCartPage(); } });
    const btnCheckout = document.getElementById('btn-checkout'); if(btnCheckout) btnCheckout.addEventListener('click', ()=>{ alert('Checkout placeholder — implementar pago.'); });
  }

  // initialize
  document.addEventListener('click', handleAddButton);
  document.addEventListener('DOMContentLoaded', function(){ updateBadge(); renderCartPage(); attachSummaryButtons(); });

  // expose for console
  window.mb_cart = { read: readCart, write: writeCart };
})();
