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


// Copy install command
function copyCommand() {
  const command = document.getElementById("install-command");

  if (!command) return;

  navigator.clipboard.writeText(command.innerText.trim());

  const button = document.querySelector(".command-header button");

  if (!button) return;

  button.innerText = "Copied!";

  setTimeout(() => {
    button.innerText = "Copy";
  }, 2000);
}