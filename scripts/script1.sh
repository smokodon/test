#!/bin/bash

# # Set the URL for the JDK tar.gz archive
# JDK_URL="https://github.com/ibmruntimes/semeru21-binaries/releases/download/jdk-21.0.3%2B9_openj9-0.44.0/ibm-semeru-open-jdk_x64_linux_21.0.3_9_openj9-0.44.0.tar.gz"

# # Define the installation directory
# INSTALL_DIR="/usr/lib/jvm"

# # Download the JDK tarball
# wget -q "$JDK_URL" -O jdk.tar.gz

# # Extract the tarball
# tar xzf jdk.tar.gz -C "$INSTALL_DIR"

# export JAVA_HOME=$INSTALL_DIR/jdk-21.0.3+9
# export PATH=$JAVA_HOME/bin:$PATH

# # Reload the shell
# source ~/.bashrc

# # Verify Java version
# java -version

#local JAVA_VERSION
  JAVA_VERSION="11"

  if [[ "${TRAVIS_CPU_ARCH}" == "arm64" ]]; then
    ${TRAVIS_CPU_ARCH}="aarch64";
  elif [[ "${TRAVIS_CPU_ARCH}" == "amd64" ]]; then
    ${TRAVIS_CPU_ARCH}="x64";
  fi

  case "${JAVA_VERSION}" in
    8) JDK_URL="https://github.com/ibmruntimes/semeru8-binaries/releases/download/jdk8u412-b08_openj9-0.44.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_8u412b08_openj9-0.44.0.tar.gz" ;; 
    11) JDK_URL="https://github.com/ibmruntimes/semeru11-binaries/releases/download/jdk-11.0.23%2B9_openj9-0.44.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_11.0.23_9_openj9-0.44.0.tar.gz" ;;
    16) JDK_URL="https://github.com/ibmruntimes/semeru16-binaries/releases/download/jdk-16.0.2%2B7_openj9-0.27.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_16.0.2_7_openj9-0.27.0.tar.gz" ;;
    17) JDK_URL="https://github.com/ibmruntimes/semeru17-binaries/releases/download/jdk-17.0.11%2B9_openj9-0.44.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_17.0.11_9_openj9-0.44.0.tar.gz" ;;
    18) JDK_URL="https://github.com/ibmruntimes/semeru18-binaries/releases/download/jdk-18.0.2%2B9_openj9-0.33.1/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_18.0.2_9_openj9-0.33.1.tar.gz" ;;
    19) JDK_URL="https://github.com/ibmruntimes/semeru19-binaries/releases/download/jdk-19.0.2%2B7_openj9-0.37.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_19.0.2_7_openj9-0.37.0.tar.gz" ;;
    20) JDK_URL="https://github.com/ibmruntimes/semeru20-binaries/releases/download/jdk-20.0.2%2B9_openj9-0.40.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_20.0.2_9_openj9-0.40.0.tar.gz" ;;
    21) JDK_URL="https://github.com/ibmruntimes/semeru21-binaries/releases/download/jdk-21.0.3%2B9_openj9-0.44.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_21.0.3_9_openj9-0.44.0.tar.gz" ;;
    22) JDK_URL="https://github.com/ibmruntimes/semeru22-binaries/releases/download/jdk-22.0.1%2B8_openj9-0.45.0/ibm-semeru-open-jdk_${TRAVIS_CPU_ARCH}_linux_22.0.1_8_openj9-0.45.0.tar.gz" ;;
    *) echo "JDK ${JAVA_VERSION} missing in the Semeru repository. Please choose a different version." ;;
  esac

echo $JDK_URL

# Define the installation directory
INSTALL_DIR="/usr/lib/jvm"

# Download the JDK tarball
wget -q "$JDK_URL" -O jdk.tar.gz

# Extract the tarball
tar xzf jdk.tar.gz -C "$INSTALL_DIR"

export JAVA_HOME="$INSTALL_DIR/jdk-${JAVA_VERSION}*"
export PATH=$JAVA_HOME/bin:$PATH

# Reload the shell
source ~/.bashrc

# Verify Java version
java -version