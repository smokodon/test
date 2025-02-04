#!/usr/bin/env bash

  echo "Download and extract Ant"
  wget -q "https://downloads.apache.org/ant/binaries/apache-ant-1.10.14-bin.tar.gz"
  tar xzf apache-ant-1.10.14-bin.tar.gz
  sudo mv apache-ant-1.10.14/ /usr/local/ant
  echo "Add Ant variables to a profile"
  ANT_HOME=/usr/local/ant
  PATH="$PATH:/usr/local/ant/bin"
  export ANT_HOME
  export PATH="$PATH:/usr/local/ant/bin" >> /etc/profile
  cat /etc/profile

