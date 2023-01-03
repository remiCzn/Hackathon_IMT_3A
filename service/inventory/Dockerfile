FROM rust:1.61.0

WORKDIR /usr/src
COPY . .

RUN cargo install --path .

CMD ["inventory"]