(function(){
  const carousel = document.getElementById('promocionesCarousel');
  if(!carousel) return;

  const track = carousel.querySelector('.carousel__track');
  const slides = Array.from(carousel.querySelectorAll('.carousel__slide'));
  const prevBtn = carousel.querySelector('[data-action="prev"]');
  const nextBtn = carousel.querySelector('[data-action="next"]');
  const dots = Array.from(carousel.querySelectorAll('.carousel__dot'));

  let current = 0;
  let timer = null;
  const interval = 5000; // 5s

  function goTo(index){
    if(index < 0) index = slides.length -1;
    if(index >= slides.length) index = 0;
    track.style.transform = `translateX(-${index * 100}%)`;
    slides.forEach((s, i) => s.classList.toggle('active', i === index));
    dots.forEach((d,i)=> d.classList.toggle('active', i===index));
    current = index;
  }

  function next(){ goTo(current+1) }
  function prev(){ goTo(current-1) }

  function startTimer(){ stopTimer(); timer = setInterval(next, interval) }
  function stopTimer(){ if(timer) { clearInterval(timer); timer=null } }

  nextBtn.addEventListener('click', ()=>{ next(); startTimer(); });
  prevBtn.addEventListener('click', ()=>{ prev(); startTimer(); });

  dots.forEach(d => d.addEventListener('click', e=>{ const i = parseInt(e.currentTarget.dataset.index,10); goTo(i); startTimer(); }));

  // pause on hover
  carousel.addEventListener('mouseenter', stopTimer);
  carousel.addEventListener('mouseleave', startTimer);

  // keyboard support
  carousel.addEventListener('keydown', e=>{
    if(e.key === 'ArrowLeft') prev();
    if(e.key === 'ArrowRight') next();
    startTimer();
  });

  // init
  goTo(0);
  startTimer();
  // make carousel focusable
  carousel.tabIndex = 0;
})();