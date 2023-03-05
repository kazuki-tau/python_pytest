# 本番用のビルドステージ(builder)
FROM python:latest AS builder

WORKDIR /workspace
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY ./src ./

# 開発用のビルドステージ
FROM builder AS dev-envs

RUN apt-get update && \
    apt-get install -y --no-install-recommends git

RUN useradd -s /bin/bash -m vscode && \
    groupadd docker && \
    usermod -aG docker vscode

USER vscode
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /