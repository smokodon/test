#!/usr/bin/env bash

set -o errexit
set -o xtrace

main() {
    wget https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_linux_hotspot_16.0.2_7.tar.gz
    tar xzf OpenJDK16U-jdk_x64_linux_hotspot_16.0.2_7.tar.gz
    export PATH=$PWD/jdk-16.0.2+7/bin:$PATH

}

main "$@"