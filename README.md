# SHAREISH

## Project Introduction
Shareish is an open-source web platform to foster mutual aid, and solidarity (also called generalized exchange or gift economy). On shareish, everything is free, no real or virtual currency is used. Everyone is free to request or offer any material, manual, intellectual, logistical aid, and act in solidarity on a regular or occasional basis.

Once you are registered and logged in, Shareish offers an interactive map where specific items (goods and services to give or to lend, requests for help, free events) can be viewed, added, and edited by registered users. Items can be geolocated so it is very easy to explore your neighbourdhood hence foster local mutual aid, at your street corner or in your area. Users can start conversations to get further details about an item/request or to arrange an appointment for the exchange. This items can also be viewed as a list where they are sorted by date. External public data (such as free drinking water sources, public bookcases and gift boxes, falling fruits, ...) can also be displayed. Search mechanisms and AI methods can be used to ease search and encoding.

Shareish development was initiated by a team of computer scientists at the Montefiore Institute supervised by [rmaree](https://github.com/rmaree), University of Liège, Belgium. Its first official release is described in the scientific paper "Shareish (Share & Cherish): an open-source, map-based, web platform to foster mutual aid", accepted for publication in the Proceedings of the 11th International Conference on Communities & Technologies, Lahti, May 2023.

## Demonstration server

A demonstration server is available at https://shareish.org/

## Installation
Shareish can be installed in production mode on a server ("Installation for deployment on a production server"), or in development mode for local development ("Local development with Docker-compose (on your own computer)"). See below for relevant installation instructions.

## Installation for deployment on a production server

The first step is to have a server that can be accessed through HTTP.

Then, you need a SSL certificate (for HTTPS, used for geolocalization of users) for your domain. In our case, we use certbot that use let's encrypt certificate. 
```
> sudo snap install --classic certbot
> sudo ln -s /snap/bin/certbot /usr/bin/certbot
> sudo certbot certonly --standalone
```  
When asked specify the URL associated to your server (e.g. shareish.org corresponding to the information of your server domain provider).


Then, download the Shareish folders and files and unzip them in a directory on your server, e.g.  using:

```
sudo curl -L https://github.com/shareish/shareish/archive/refs/heads/main.zip -o main.zip
unzip main.zip 
```

Change the name of your host server name by editing the file main.js in the directory frontend/src/

Then edit backend/mapsite/settings.py (you should change e.g. the default email address used to send e-mails for account creation, notifications, ...):

Download Docker and start it on your server (https://docs.docker.com/engine/install/):

```
> curl https://get.docker.com | sh
> sudo usermod -aG docker $USER
> sudo reboot
> sudo systemctl start docker
> sudo systemctl enable docker
```

Download docker-compose.

```
> sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Set permissions to make it executable.

```
> sudo chmod +x /usr/local/bin/docker-compose
```

Verify that docker-compose is correctly set up.

```
> docker-compose --version
```
It should output something like this:
```
docker-compose version 1.29.2, build 5becea4c
```

Build the docker images of Shareish by executing the following command in the directory where you put Shareish folders:

```
> docker-compose build
```

Start the docker containers.

```
> docker-compose up -d
```

When you need to update the code and re-deploy your website, the volumes are kept so the data inserted in your database will be conserved. If you want to refresh everything and prune every volumes on your server, you can type:

```
> docker volumes prune -a
```

Do not forget to change the settings in the /backend/mapsite/settings.py file that are marked as

```
#CHANGE THIS WHEN CLONING THE PROJECT
```

## Update of SSL certificate
The let's encrypt certificate has to be renewed every three months. It is possible to have a cron script to do this procedure automatically (this script stop docker compose, launch certificate update using certbot, then restart docker compose). This script has to be executed within the directory where you downloaded Shareish folders and files as explained previously. Here is an example of cron script scheduled at 3.16 AM (the folder where shareish is installed has to be modified accordingly):
```
> crontab -e
16 3 * * * cd /SHAREISH_FOLDER && certbot renew -n --pre-hook "docker-compose stop" --post-hook "docker-compose up -d" >> /output.cron
```

## Local development with Docker-compose (on your own computer)

Shareish can be run in development environment using Docker-compose on your own computer:

Install Docker and Docker compose on your computer (https://docs.docker.com/engine/install/).

Then, clone the Shareish repository on your system:
git clone https://github.com/shareish/shareish.git

Then edit settings (you should change e.g. the default email address used to send e-mails for account creation, notifications, ...):
1. Set `DEV=True` in `backend/mapsite/settings.py`.
2. Be sure the `frontend/node_modules` does not exist (only first time, or when you have 
   strange issues with `npm`).
3. To build backend and frontend dev images:
```
docker compose -f docker-compose.dev.yaml build
```
4. To run dev environment:
``` 
docker compose -f docker-compose.dev.yaml up -d --build
```

Backend is running at `http://localhost:8000`, and frontend at `http://localhost:8081`.

See the logs in live: `docker compose logs` (in the root directory).
To stop: `docker compose stop` (in the root directory).
To remove container: `docker compose rm` (in the root directory, data are kept in the volumes).

In development mode, there is an hot reload mechanism: every time you save a file in backend or frontend, the 
corresponding code is recompiled if needed and the server is restarted automatically (see the logs using docker compose logs -f web/ui/db).
