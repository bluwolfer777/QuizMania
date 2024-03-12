  // Funzione per aggiornare la progress bar
  function updateProgressBar(totalSeconds, elapsedSeconds) {
    const progress = ((totalSeconds - elapsedSeconds) / totalSeconds) * 100; // Calcola la percentuale invertendo il tempo rimanente
    document.querySelector('.progress-bar').style.width = progress + '%'; // Imposta la larghezza della progress bar
  }

  // Esempio di utilizzo
  const totalSeconds = 30; // Tempo totale in secondi
  let elapsedSeconds = 0; // Tempo trascorso in secondi

  // Funzione per aggiornare la progress bar ogni secondo
  const intervalId = setInterval(function() {
    elapsedSeconds++; // Incrementa il tempo trascorso
    updateProgressBar(totalSeconds, elapsedSeconds); // Aggiorna la progress bar
    if (elapsedSeconds >= totalSeconds) {
      clearInterval(intervalId); // Interrompi l'aggiornamento della progress bar quando il tempo è scaduto
    }
  }, 1000);