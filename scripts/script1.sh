#!/bin/bash

# Set the URL for the JDK tar.gz archive
JDK_URL="https://github.com/ibmruntimes/semeru21-binaries/releases/download/jdk-21.0.3%2B9_openj9-0.44.0/ibm-semeru-open-jdk_x64_linux_21.0.3_9_openj9-0.44.0.tar.gz"

# Define the installation directory
INSTALL_DIR="/opt"

# Download the JDK tarball
wget -q "$JDK_URL" -O jdk.tar.gz

# Extract the tarball
tar xzf jdk.tar.gz -C "$INSTALL_DIR"

ls -al $INSTALL_DIR
ls -al $INSTALL_DIR/jdk-21.0.3+9
ls -al $INSTALL_DIR/jdk-21.0.3+9/bin

sudo update-alternatives --install /usr/bin/java java /opt/jdk-21.0.3+9/bin/java 1000

#export JAVA_HOME=$INSTALL_DIR/jdk-21.0.3+9/bin/java
#export PATH=$JAVA_HOME/bin:$PATH

echo $JAVA_HOME
echo $PATH
# Set JAVA_HOME
#echo "export JAVA_HOME=$INSTALL_DIR/jdk" >> ~/.bashrc

# Add JDK bin directory to PATH
#echo "export PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc

# Reload the shell
#source ~/.bashrc

# Verify Java version
java -version
