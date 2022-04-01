  #!/usr/bin/env bash
  
main() {
  local JAVA_VERSION
  JAVA_VERSION="17"
  sudo apt-get update -yqq
  PACKAGE="temurin-${JAVA_VERSION}-jdk"
  if ! dpkg -s "$PACKAGE" >/dev/null 2>&1; then
    if dpkg-query -l temurin* >/dev/null 2>&1; then
       dpkg-query -l temurin* | grep temurin | awk '{print $2}' | xargs sudo dpkg -P
    fi
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /usr/share/keyrings/adoptium.asc
    echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
    sudo apt-get update -yqq
    sudo apt-get -yqq --no-install-suggests --no-install-recommends install "$PACKAGE" || true
    sudo update-java-alternatives -s "$PACKAGE"*


main "$@"