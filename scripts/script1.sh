# sync package metadata
sudo apt-get update
# install dependencies manually
sudo apt-get -y install socat logrotate init-system-helpers adduser

# download the package
sudo apt-get -y install wget
wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.13.3/rabbitmq-server_3.13.3-1_all.deb

# install the package with dpkg
sudo dpkg -i rabbitmq-server_3.13.3-1_all.deb

rm rabbitmq-server_3.13.3-1_all.deb