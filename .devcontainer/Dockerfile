FROM mambaorg/micromamba:latest

# Copy environment configuration
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

# Install/create the 'ph306' environment from the spec
RUN micromamba create -y -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Install Git
USER root
RUN apt update && apt install -y --no-install-recommends git && apt clean && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Automatically activate 'ph306' in terminal sessions
ENV ENV_NAME=ph306
