# there must be a better way
FROM python:3.10.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get -y update && apt-get -y install curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rustup.sh \
    && sh rustup.sh -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd src/match_engine \
    && cargo install maturin \
    && maturin build -r --sdist
RUN python -m pip install poetry
RUN poetry install  # TODO: install from lockfile

ENTRYPOINT ["poetry", "run", "uvicorn", "server.main:app"]
