document.addEventListener('DOMContentLoaded', function(){
  const main = document.getElementById('mainImage');
  const thumbs = document.querySelectorAll('.thumbnails img');

  // Smooth swap with fade
  function swapMain(src){
    if(!main) return;
    main.classList.add('fade-out');
    setTimeout(()=>{
      main.src = src;
      main.classList.remove('fade-out');
    }, 180);
  }

  if(thumbs && thumbs.length){
    thumbs.forEach(t => {
      t.addEventListener('click', function(){
        const s = this.dataset.src || this.src;
        swapMain(s);
      });
      // small hover 3D on thumbnails
      t.addEventListener('pointerenter', ()=> t.style.transform = 'translateY(-6px) scale(1.03)');
      t.addEventListener('pointerleave', ()=> t.style.transform = '');
    });
  }

  // Lightbox: click main image to open large view
  function createLightbox(src){
    const lb = document.createElement('div');
    lb.className = 'pd-lightbox';
    lb.innerHTML = `<img src="${src}" alt="producto">`;
    lb.addEventListener('click', (e)=>{ if(e.target === lb) close(); });
    function open(){ document.body.appendChild(lb); requestAnimationFrame(()=> lb.classList.add('open')); }
    function close(){ lb.classList.remove('open'); setTimeout(()=> lb.remove(), 220); }
    return { open, close };
  }

  if(main){
    main.addEventListener('click', ()=>{
      const src = main.src;
      const lb = createLightbox(src);
      lb.open();
    });
    // keyboard close
    document.addEventListener('keydown', (ev)=>{
      if(ev.key === 'Escape'){ const lb = document.querySelector('.pd-lightbox.open'); if(lb) lb.classList.remove('open'); }
    });
  }

  // small safety: if main image fails, set placeholder
  if(main){
    main.addEventListener('error', ()=> main.src = '/media/productos_imagenes/default_producto.png');
  }

  // Quantity controls and sync with add-to-cart button
  document.querySelectorAll('.qty-controls').forEach(wrapper => {
    const input = wrapper.querySelector('.qty-input');
    const btnInc = wrapper.querySelector('.qty-increase');
    const btnDec = wrapper.querySelector('.qty-decrease');
    const productId = wrapper.dataset.productId;
    const addBtn = document.querySelector(`.add-to-cart[data-id="${productId}"]`);

    if(!input) return; // nothing to do

    function setQuantity(q){
      const max = Math.max(1, parseInt(input.max || '9999', 10) || 9999);
      let n = parseInt(q, 10);
      if(Number.isNaN(n)) n = 1;
      n = Math.max(1, Math.min(n, max));
      input.value = n;
      if(addBtn) addBtn.dataset.quantity = String(n);
    }

    // Increase / decrease handlers
    if(btnInc){ btnInc.addEventListener('click', (e)=>{ e.preventDefault(); setQuantity(Number(input.value||1)+1); }); }
    if(btnDec){ btnDec.addEventListener('click', (e)=>{ e.preventDefault(); setQuantity(Number(input.value||1)-1); }); }

    // Allow keyboard up/down on the input as well
    input.addEventListener('keydown', (ev)=>{
      if(ev.key === 'ArrowUp'){ ev.preventDefault(); setQuantity(Number(input.value||1)+1); }
      if(ev.key === 'ArrowDown'){ ev.preventDefault(); setQuantity(Number(input.value||1)-1); }
    });

    // Normalize pasted/typed values
    input.addEventListener('input', ()=>{
      // ensure only numbers
      const cleaned = (input.value || '').replace(/[^0-9]/g, '');
      if(cleaned !== input.value) input.value = cleaned;
    });

    input.addEventListener('change', ()=> setQuantity(input.value));
    // initialize
    setQuantity(input.value || 1);
  });
});
