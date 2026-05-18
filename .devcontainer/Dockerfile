ARG UV_VERSION=latest


FROM ghcr.io/astral-sh/uv:$UV_VERSION AS uv


FROM mcr.microsoft.com/vscode/devcontainers/base:debian

ENV TZ=America/Lima
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE=True \
    PYTHONUNBUFFERED=True \
    UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=system

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # For OpenCV etc...
    dnsutils \
    libgl1 libglib2.0-0 \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    # To remove the image size, it is recommended refresh the package cache as follows
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.13 /usr/local/bin/python3 \
    && ln -s /usr/bin/python3.13 /usr/local/bin/python

COPY --from=uv --chown=vscode: /uv /uvx /bin/
