document.addEventListener('DOMContentLoaded', function(){
  const track = document.querySelector('.marcas-slider__track');
  if(!track) return;

  let idx = 0;
  const slides = Array.from(track.children);
  const total = slides.length;

  // Calcula el ancho de un slide (incluyendo gap) para desplazar
  function slideWidth(){
    const slide = slides[0];
    if(!slide) return 0;
    const style = getComputedStyle(track);
    const gap = parseFloat(getComputedStyle(track).gap) || 18;
    return slide.getBoundingClientRect().width + gap;
  }

  let timer = null;

  function goTo(index){
    const w = slideWidth();
    track.style.transform = `translateX(${-(w * index)}px)`;
  }

  function next(){
    // Avanzar 1 slide, pero loop infinito suave
    idx++;
    if(idx > total - visibleCount()){
      idx = 0;
    }
    goTo(idx);
  }

  function visibleCount(){
    // aproximación del número de slides visibles según ancho
    const vw = window.innerWidth;
    if(vw < 420) return 1;
    if(vw < 700) return 2;
    if(vw < 1100) return 3;
    return 4;
  }

  function start(){
    stop();
    timer = setInterval(next, 5000);
  }
  function stop(){
    if(timer) clearInterval(timer);
    timer = null;
  }

  // pausa al hover
  track.parentElement.addEventListener('mouseenter', stop);
  track.parentElement.addEventListener('mouseleave', start);

  // botones prev/next
  const btnPrev = document.querySelector('.marcas-prev');
  const btnNext = document.querySelector('.marcas-next');
  if(btnPrev){
    btnPrev.addEventListener('click', function(){
      idx = Math.max(0, idx - 1);
      goTo(idx);
      start(); // reiniciar timer
    });
  }
  if(btnNext){
    btnNext.addEventListener('click', function(){
      idx = Math.min(total - visibleCount(), idx + 1);
      goTo(idx);
      start(); // reiniciar timer
    });
  }

  // reajustar al redimensionar
  window.addEventListener('resize', function(){
    goTo(idx);
  });

  // iniciar
  start();
});
