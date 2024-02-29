# SHAREISH

## Project Introduction
Shareish is an open-source web platform to foster diverse solidarity practices (incl. mutual aid, generalized exchange, non-monetary sharing, caremongering, or gift economy). On Shareish, everything is free, no real or virtual currency is used. Everyone is free to request or offer any material, manual, intellectual, logistical aid, and act in solidarity on a regular or occasional basis.

Once you are registered and logged in, Shareish offers an interactive map where specific items (goods and services to give or to lend, requests for help, free events, free public resources) can be viewed, added, and edited by registered users. Items can be geolocated so it is very easy to explore your neighbourdhood hence foster local mutual aid, at your street corner or in your area. Users can start conversations to get further details about an item/request or to arrange an appointment for the exchange. These items can also be viewed as a list where they are sorted by date. External public data (such as free drinking water sources, public bookcases and gift boxes, free shops, falling fruits, ...) can also be displayed and edited (through OpenStreetMap and FallingFruit databases). Search mechanisms and AI methods can be used to ease search and encoding.

Shareish development was initiated by a team of computer scientists at the Montefiore Institute, University of Liège, Belgium. Contributors are welcome !

Its first official release is described in the scientific paper [Shareish (Share & Cherish): an open-source, map-based, web platform to foster mutual aid](https://dl.acm.org/doi/10.1145/3593743.3593790), published in the Proceedings of the 11th International Conference on Communities & Technologies, Lahti, May 2023. It is continuoulsy developed and important features have been added since then, you can test latest version using our public demonstration server (see below).

If you are interested by this project (as a potential user, contributor, developer, member of a grassroot movements, ...), say a word in [GitHub Discussions](https://github.com/shareish/shareish/discussions) or <info@shareish.org> (if you are more comfortable by e-mail) !

![Shareish map](shareish-map-screenshot.jpg?raw=true "Shareish map")

## Demonstration server

[A public server hosted by the University of Liège is available](https://shareish.org/)

## Installation
Shareish can be installed in development mode for local tests and development ("Local development with Docker-compose (on your own computer)") or in production mode on a server ("Installation for deployment on a production server"). See below for relevant installation instructions.

## Local development with Docker-compose (on your own computer)

Shareish can be run in development mode on your own computer environment using Docker-compose (it should take about 10 minutes the first time, depending on Internet speed) :

1. Install Docker and Docker compose on your computer: https://docs.docker.com/engine/install/

2. Then, clone the Shareish repository on your system:
```
git clone https://github.com/shareish/shareish.git
```

Then configure your installation:
3. Create a **docker-compose.env** file in the main directory (you can copy our template docker-compose.env.template) that contains a short list of environment variables to be adapted to your environment. Edit the file and:
4. Set **DEV=True** to activate the DEVelopment mode.
5. Add a **SECRET_KEY** value (see https://django-secret-key-generator.netlify.app to generate a secret key).
6. Edit the **E-mail settings** that are used by the backend to send e-mails for account creation and notifications by editing the following variables: **EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD** and **EMAIL_USE_TLS=True** (to be checked with your e-mail provider).
7. Edit database settings (**POSTGRES_** variables) or leave default values
8. Be sure the `frontend/node_modules` does not exist (only first time, or when you have strange issues with `npm`).

You are ready to build your local instance:
9. To build backend and frontend dev images:
```
docker compose -f docker-compose.dev.yaml build
```
10. To run dev environment:
``` 
docker compose -f docker-compose.dev.yaml up -d --build
```

Once installed, frontend is running locally at `http://localhost:8081`; backend API is located at `http://localhost:8000/api/v1/`, and backend administration interface is running at `http://localhost:8000/admin/`.

In development mode, there is an hot reload mechanism: every time you save a file in backend or frontend, the corresponding code is recompiled if needed and the server is restarted automatically. This eases direct assessment of your changes to the code.

If you want to update Shareish to latest version, git pull the last commits (or release tag) and run again the Docker build (9.) and up (10.) commands. The Docker volumes are kept so the data inserted in your database will be conserved.


## Installation for deployment on a production server

The first step is to have a server that can be accessed through HTTP(s).
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

Then configure settings, first edit **frontend/src/main.js**:
1. Change the name of your host server name by editing the variable **PROD_URL**.

Then edit **backend/mapsite/settings.py**:
2. Change the name of your host sever name by editing the **PROD_DOMAIN** variable to match the server host name of your production server.

Then create a **docker-compose.env** file in the main directory (you can copy our template docker-compose.env.template) that contains a short list of environment variables to be adapted to your environment:
3. Keep **`DEV=False`** to activate the production mode.
4. Add a **SECRET_KEY** value (see https://django-secret-key-generator.netlify.app to generate a secret key).
5. Edit the **E-mail settings** that are used by the backend to send e-mails for account creation and notifications by editing the following variables: **EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD** and **EMAIL_USE_TLS=True** (to be checked with your e-mail provider).
6. Edit database settings (**POSTGRES_** variables) or leave default values

Additionally, you should also have your own privacy policy and terms of conditions (as you will be hosting user data), these are defined in **frontend/src/locales/translations.csv** in variables faq_data_collection_answer and faq_everything_answer and will be displayed on the homepage.

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

Build the docker images of Shareish instance by executing the following command in the main directory where you put Shareish folders:

```
> docker-compose build
```

Start the docker containers.

```
> docker-compose up -d
```

Your Shareish instance should be up and running at `https://PROD_DOMAIN'

If you want to update Shareish to latest version, download the latest zip files and run again the Docker build and up commands.
The Docker volumes are kept so the data inserted in your database will be conserved.


## Update of SSL certificate for HTTPS production server
The let's encrypt certificate has to be renewed every three months. It is possible to have a cron script to do this procedure automatically (this script stop docker compose, launch certificate update using certbot, then restart docker compose). This script has to be executed within the directory where you downloaded Shareish folders and files as explained previously. Here is an example of cron script scheduled at 3.16 AM (the folder where Shareish is installed has to be modified accordingly):
```
> crontab -e
16 3 * * * cd /SHAREISH_FOLDER && certbot renew -n --pre-hook "docker-compose stop" --post-hook "docker-compose up -d" >> /output.cron
```


## Logs and Docker operations
See the logs in live: `docker compose logs` (in the root directory).

For logs of a specific container, use:
Logs of the backend: `docker compose logs -f web`
Logs of the frontend: `docker compose logs -f ui`
Logs of the database: `docker compose logs -f db`
Logs of the backup: `docker compose logs -f backup`

To stop: `docker compose stop` (in the root directory).
To remove container: `docker compose rm` (in the root directory, data are kept in the volumes).

See Docker documentation for more information.

If you want to free some space by cleaning images (this will not delete Shareish data but only unused containers e.g. older deployments):
```
sudo docker system df
docker image prune --all
docker system prune -a
```
The volumes are kept so the data inserted in your database will be conserved.


If however you want to re-install from scratch and re-deploy an empty Shareish website (**WARNING: it deletes all your Shareish instance data**), you can type:

```
> docker volumes prune -a
```
See Docker documentation for more information about volumes, images, etc.




## Backup Shareish data
A backup of Shareish data (item and user images, and Postgres SQL content) is automatically done using cron (every day at 11.30PM, with 7 stored versions) by the backup container. It basically put data into the backup/ directory (sub-folders image and postgres). However, this is only a local copy, you should copy these elsewhere (through scp, sftp or other means). If you want to edit backup frequency or other parameters, see sh files in backup/ directory.


## Technical implementation
We use various tools and libraries including Python, Django, Vue.JS+Bulma, PostgreSQL+PostGIS,... See our paper for more information about our technical implementation.