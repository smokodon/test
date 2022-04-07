#!/usr/bin/env bash

set -o errexit
set -o xtrace

main() {
    
  local JAVA_VERSION
  JAVA_VERSION="17"
  sudo apt-get update -yqq
  PACKAGE="temurin-${JAVA_VERSION}-jdk"
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /usr/share/keyrings/adoptium.asc
    echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
    sudo apt-get update -yqq
    #export JAVA_HOME="/usr/bin/java"
    # shellcheck disable=SC2016
    #export PATH="$JAVA_HOME/bin:$PATH"
    sudo apt-get -yqq --no-install-suggests --no-install-recommends install "$PACKAGE" || true
    sudo update-java-alternatives -s /usr/lib/jvm/"$PACKAGE"* --verbose
    whereis java
    #echo $JAVA_HOME
    #java -version
}

main "$@"