FROM rustlang/rust:nightly-slim as builder

RUN apt-get -y update && apt-get -y install curl

# wasm-pack
RUN curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | bash

# node
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash \
	&& apt-get install -y nodejs

WORKDIR /app

COPY docker_run.sh ./
COPY wasm /app/wasm
COPY client/package.json /app/client/
COPY client /app/client

RUN cd wasm \
    && rustup target add wasm32-unknown-unknown \
    && cargo build --release --target wasm32-unknown-unknown \
    # this step doesn't work, hence previous curl install
    # && cargo install wasm-pack \
    && wasm-pack build

RUN cd client \
    && npm install \
    && ls node_modules/wasm-conway \
    && npm run build

FROM nginx:alpine

COPY --from=builder /app/client/dist /usr/share/nginx/html
