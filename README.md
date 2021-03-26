# BOT CLI

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/labmiriade/bot-cli)

A command line interface for interacting with our beloved 🐷 BOT.

## Installazione

### 0. Python

Controlla di avere installata una versione di Python 🐍 compatibile, cioè **3.8** o superiore.
Per controllare esegui `python3 --version` nel terminale.

### 1. Installa il comando

Il comando si installa con *pip* il [Package Installer per Python](https://pypi.org/project/pip/).

```sh
python3 -m pip install --upgrade https://github.com/labmiriade/bot-cli/releases/latest/download/bot_cli-1.0.0-py3-none-any.whl
```

### 2. _Opzionale_ Aggiungere l'autocompletamento

Non è obbligatorio abilitare l'autocompletamento ma semplifica notevolmente la vita (ad esempio nell'inserimento
dei nomi delle commesse).

La procedura consiste nell'aggiungere un comando all'avvio della shell: questo varia a seconda della
shell che si utilizza ma per tutte consiste nel copiare il comando _eval_ qui sotto nel file eseguito
all'avvio di una nuova sezione.

Per **Bash**, aggiungi a _~/.bashrc_:

```sh
eval "$(_BOT_COMPLETE=source_bash bot)"
```

Per **Zsh**, aggiungi a _~/.zshrc_:

```sh
eval "$(_BOT_COMPLETE=source_zsh bot)"
```

Per **Fish**, crea il file _~/.config/fish/completions/bot.fish_:

```sh
eval (env _BOT_COMPLETE=source_fish bot)
```

## Getting Started

Per iniziare digita `bot config` e inserisci il tuo username (la mail aziendale), la tua password
e la sede preferita (potrai impostarla per ogni rapportino, questo sarà il default).

### Ottenere la password

Se hai sempre fatto il login con Google è probabile che tu non conosca la password del tuo utente:
questa è la procedura per ottenerla.

1. Vai nella [homepage di bot](https://bot.miriade.it) e seleziona "Password dimenticata".

2. Compila i campi username e password

3. Se ti viene chiesto di rispondere alla domanda di sicurezza, rispondi. Se non ricordi la risposta
la puoi leggere accedendo a BOT, cliccando sull'icona in alto a dx, andando in Impostazioni Account >
Password.

4. Controlla la tua casella email e segui le istruzioni per impostare una nuova password.

### Comandi più comuni

I comandi più comuni sono quelli in `bot rapp`, come **add**, **ls**, **missing**.

Ma è molto importante conoscere anche `bot settings svuota-cache`, per svuotare la cache e assicurarsi
di ricevere le commesse appena aggiunte.

#### Rapportini

Per interagire con i rapportini puoi iniziare con:

```sh
bot rapp ls
```

che inizierà a stampare a ritroso i rapportini inseriti negli ultimi 7 giorni.

Puoi usare l'opzione `--data 03-03-2021` per controllare i rapportini di una data specifica
e l'opzione `--count <numero-giorni>` per decidere quanti giorni a ritroso dalla data selezionata
vanno mostrati.

Per visualizzare le date per cui manca da inserire i rapportini puoi utilizzare:

```sh
bot rapp missing
```

Mentre per inserire un rapportino puoi digitare:

```sh
bot rapp add COMMESSA ATTIVITÀ
```

non è necessario inserire la commessa o l'attività se si è abilitato l'autocompletamento, basta utilizzare il tasto
_<tab>_ per far comparire una lista di opzioni.

Verranno chieste dal comando le opzioni come data, ore da inserire, descrizione, note e sede ma tutte queste sono
opzioni che possono essere specificate nel comando iniziale:

```sh
bot rapp add 81_MIR_FORMAZIONE 24_Formazione_effettuata --sede 2 --ore 4
```

fa sì che le informazioni su sede e ore non vengano chieste.

Prima di salvare il rapportino è possibile premere `f` per modificare i _flag_ (trasferta, prepagato, fatturare,
straordinario), altrimenti premere `y` per confermare.

## Contribuire

Sarebbe fantastico se volessi contribuire con l'introduzione di nuove feature o sistemare qualche problema ❤️.
Leggi [CONTRIBUTING.md](/CONTRIBUTING.md) per ulteriori informazioni su come fare.
