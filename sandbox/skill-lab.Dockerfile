FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    CARGO_NET_OFFLINE=true \
    RUST_BACKTRACE=0

RUN apt-get update \
 && apt-get install -y --no-install-recommends rustc cargo ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd --gid 65532 cyberai \
 && useradd --uid 65532 --gid 65532 --no-create-home --shell /usr/sbin/nologin cyberai

USER 65532:65532
WORKDIR /workspace
ENTRYPOINT ["cargo"]
