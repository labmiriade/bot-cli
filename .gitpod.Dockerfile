FROM gitpod/workspace-full

USER gitpod

RUN pyenv install 3.8.8 --skip-existing
RUN pyenv global 3.8.8
RUN pip install --upgrade poetry

ENV PIP_USER=false
