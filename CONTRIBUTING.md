# Contributing

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/labmiriade/bot-cli)

Grazie per voler contribuire alla BOT CLI 🐷 💪🏽.

## Pull Request Process

1. Prima di tutto controlla che non esista già una issue su quello che vuoi fare tu, se esiste quello è il posto dove discutere cosa verrà implementato e come.

2. Se la issue non esiste, aprine una cercando di spiegare al meglio l'obiettivo nella descrizione e come intendi farlo nei commenti.
Se ci sono nuovi dettagli non farti problemi a **modificare il primo commento**: dovrebbe essere il punto da cui partire per comprendere la questione,
mentre puoi usare i commenti per discutere idee.

3. Quando decidi di lavorare scrivilo in un commento così da evitare che altri prendano in mano la issue sprecando tempo.

4. Per iniziare a scrivere codice effettua un [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)
della repo nel tuo account, un fork è una copia della repo principale nel tuo account.

5. Crea un branch da `main` con un nome che descriva bene cosa intendi fare (non inserire riferimenti alla issue nel nome).

6. Scrivi il codice 🧙, testalo e fai pure `git push`: il codice verrà salvato in un branch nel tuo fork (la copia della repo nel tuo account) ma non verrà
incluso nella repo principale. Non dimenticarti di scrivere qualche test 🧪.

7. Quando sei soddisfatto del lavoro e vuoi che venga incluso nella repo principale, apri una PR dal tuo branch (nella tua repo) al branch
`main` della repo principale (compare il banner nella homepage della repo forked, se hai dubbi
[vedi qui](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork))

8. Nella PR che apri indica il riferimento alla issue che stai risolvendo (è sufficiente che nel testo principale compaia `#<id-issue>`)
così da collegare la issue alla PR.

9. Aspetta di ricevere una review, se questa dura tanto chiedi tu una review attraverso il bottone a dx nella pagina della review.

10. Done ✔️ grazie per la tua prima contribution a BOT CLI 🐷.

Per qualsiasi dubbio, non farti problemi e chiedi una mano! 😉

## Avvio del progetto

Il progetto è scritto in Python perché è un linguaggio che si presta molto bene allo scopo ed è largamente conosciuto.
Ci sono però alcune cose da tenere a mente perché il progetto resti di qualità e per facilitare la collaborazione:

* Le versioni compatibili devono essere **python 3.8** e superiori, quindi evita di utilizzare funzionalità non presenti in _python 3.8_.

* Per favorire la sanità mentale di tutti **indica i tipi** (es. `Dict[str, str]` per un dizionario di stringhe) in tutte le dichiarazioni
di funzioni, classi, metodi e ovunque debbano essere riutilizzati da altri

* Per uniformare al massimo lo stile di scrittura si usa **black**: è sufficiente, dopo aver scritto il codice, eseguire `black` nella home
del progetto. _Se ti dimentichi di formattare il codice, verrà verificato in sede di PR, non preoccuparti._

* Per evitare errori, Python deve soddisfare i requisiti di [pep8](https://www.python.org/dev/peps/pep-0008/), questo viene controllato con
**flake8**, puoi controllare che il codice soddisfi i requisiti con `flake8 src tests` dalla home del progetto. _Se ti dimentichi di
formattare il codice, verrà verificato in sede di PR, non preoccuparti._

## Configurazione IDE

Se vuoi iniziare a programmare senza dover configurare un ambiente locale puoi utilizzare il tasto
[Open in Gitpod](https://gitpod.io/#https://github.com/labmiriade/bot-cli) per lanciare un ambiente virtuale
(Visual Studio Code) in cloud. _Il piano gratuito prevede 50 ore di utilizzo al mese per i progetti open source 😉_

Visual Studio Code sarà già configurato al meglio e ti resta solo da lanciare `pytest` nel terminale in basso
per vedere che tutto funzioni. Puoi usare `bot config` e inserire le tue credenziali per testare il comando.

Per lo sviluppo devi installare tutte le dipendenze che si trovano in _requirements.txt_ con `pip install -r requirements.txt`.
Ti consiglio di farlo solo **dopo** aver creato e attivato un ambiente virtuale dove isolare le dipendenze per questo progetto:

- **Creare il venv** da fare una sola volta `python3 -m venv venv`: creerà una cartella _venv_ in cui verranno salvate tutte le
dipendenze del progetto.

- **Attivare il venv** quando apri una shell (se non lo fa in automatico l'IDE) devi attivare l'ambiente virtuale che hai creato
per usare le dipendenze lì salvate. Si fa con: `source venv/bin/activate` (se vuoi disattivarlo chiudi la shell o esegui `deactivate`).
