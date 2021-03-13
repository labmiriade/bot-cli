# BOT CLI

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/labmiriade/bot-cli)

A command line interface for interacting with our beloved 🐷 BOT.

## Installation

### 0. Check for python

This tool is based on **python 3.8** or higher, check that you have it.

### 1. Install with pip

Install the cli with pip (Python package installer)

```sh
python3 -m pip install git+https://github.com/labmiriade/bot-cli.git
```

### 2. _Optional_ add autocompletion

Adding autocompletion is optional but highly recommended.
Instruction varies between shells.

For **Bash**, add this to ~/.bashrc:

```sh
eval "$(_BOT_COMPLETE=source_bash bot)"
```

For **Zsh**, add this to ~/.zshrc:

```sh
eval "$(_BOT_COMPLETE=source_zsh bot)"
```

For **Fish**, add this to ~/.config/fish/completions/foo-bar.fish:

```sh
eval (env _BOT_COMPLETE=source_fish bot)
```

## Getting Started

Per iniziare digita `bot config` e inserisci il tuo username e la tua password.

### Common Commands

I comandi più comuni sono quelli in `bot rapp`, come **add**, **ls**, **missing**.

## Contribuire

Sarebbe fantastico se volessi contribuire con l'introduzione di nuove feature o sistemare qualche problema ❤️.
Leggi [CONTRIBUTING.md](/CONTRIBUTING.md) per ulteriori informazioni su come fare.

