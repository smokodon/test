#!/usr/bin/env bash

set -o errexit
set -o xtrace

main() {

  local JAVA_VERSION
  JAVA_VERSION=13
  sudo apt-get update -yqq
  PACKAGE="bellsoft-java${JAVA_VERSION}"
  wget -qO - https://download.bell-sw.com/pki/GPG-KEY-bellsoft | sudo apt-key add -
  sudo add-apt-repository  'deb [arch='$TRAVIS_CPU_ARCH'] https://apt.bell-sw.com/ stable main'
  sudo apt-get update -yqq
  sudo apt-get -yqq --no-install-suggests --no-install-recommends install "$PACKAGE" || true
  travis_cmd "export JAVA_HOME=/usr/lib/jvm/bellsoft-java${JAVA_VERSION}-${TRAVIS_CPU_ARCH}" --echo
  travis_cmd 'export PATH="$JAVA_HOME/bin:$PATH"' --echo
  sudo update-java-alternatives -s "$PACKAGE"*

}

main "$@"