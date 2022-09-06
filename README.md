# SHAREISH

## Installation for deployment
Download the folders and files

Change the name of your host server name in the file main.js in /frontend/src/

Download docker and start it on your device.

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

Build the docker images.

```
> docker-compose build
```

Start the docker containers.

```
> docker-compose up -d
```

When you need to change the code and re-deploy your website, the volumes are kept so the data inserted in your database will be conserved. If you want to refresh everything and prune every volumes on your server, you can type:

```
> docker volumes prune -a
```

Do not forget to change the settings in the /backend/mapsite/settings.py file that are marked as

```
#CHANGE THIS WHEN CLONING THE PROJECT
```

## Development with Docker-compose

Shareish can be run in development environment using Docker-compose:

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
To remove container: `docker compose rm` (in the root directory, data is preserved).

In development, there is hot reload: every time you save a file in backend or frontend, the 
corresponding code is recompiled if needed and server restarted automatically (see the logs).