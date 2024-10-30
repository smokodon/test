FROM jammy:latest

ENV DEBIAN_FRONTEND noninteractive

# Add the packages.txt file
ADD packages.txt /var/tmp/packages.txt

# Update and install necessary tools
RUN apt-get update -yq && apt-get install -y software-properties-common

# Add additional repositories
RUN apt-add-repository -y multiverse && \
    apt-add-repository -y restricted && \
    apt-add-repository -y universe

# Update again after adding repositories
RUN apt-get update -yq

# Install packages from packages.txt
RUN cat /var/tmp/packages.txt | xargs apt-get install -yq --no-install-suggests --no-install-recommends

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*