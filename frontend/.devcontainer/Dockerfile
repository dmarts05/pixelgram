FROM mcr.microsoft.com/devcontainers/base:bookworm

# Install Node and NPM for development tools that require them and openssh-client for git support.
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Install Bun 1.2.11. 
RUN npm install -g bun@1.2.11