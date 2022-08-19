# tfe

Download the folders and files
Change name in the file main.js in /frontend/src/

Download docker and start it on your device.
curl https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo reboot
sudo systemctl start docker
sudo systemctl enable docker

Download docker-compose.
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

Set permissions to make it executable.
sudo chmod +x /usr/local/bin/docker-compose

Varify that docker-compose is correctly set up.
docker-compose --version

Build the containers
docker-compose build

Start the containers
docker-compose up

TODO Resolve images and conversations bugs (maybe use volumes for images)