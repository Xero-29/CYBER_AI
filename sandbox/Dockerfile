FROM python:3.12-slim-bookworm@sha256:0f086103b026048cc50cb5da25ec435c023c5241a83fc44daea593377abc61c4

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python -m pip install --no-cache-dir \
      ruff==0.14.5 \
      bandit==1.8.6 \
    && groupadd --gid 65532 cyberai \
    && useradd --uid 65532 --gid 65532 --no-create-home --shell /usr/sbin/nologin cyberai

USER 65532:65532
WORKDIR /workspace
ENTRYPOINT ["python"]
