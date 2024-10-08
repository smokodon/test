#!/bin/bash

  arch=$(uname -m)
  wget https://go.dev/dl/go1.21.1.linux-$arch.tar.gz
  sudo tar -C /usr/local -xzf go1.21.1.linux-$arch.tar.gz
  echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.profile
  export PATH=\$PATH:/usr/local/go/bin
  sudo chown -R travis: /tmp/__common-lib.sh


