(function () {
  const logo = document.querySelector('.ascii-logo');
  if (!logo) return;

  function scheduleFlicker() {
    const delay = 4000 + Math.random() * 6000;
    setTimeout(() => {
      logo.style.transition = 'opacity 40ms';
      logo.style.opacity = (0.7 + Math.random() * 0.2).toFixed(2);

      setTimeout(() => {
        logo.style.opacity = '1';
        setTimeout(() => {
          if (Math.random() > 0.5) {
            logo.style.opacity = (0.8 + Math.random() * 0.15).toFixed(2);
            setTimeout(() => { logo.style.opacity = '1'; }, 60);
          }
          scheduleFlicker();
        }, 80);
      }, 50);
    }, delay);
  }

  scheduleFlicker();
})();
