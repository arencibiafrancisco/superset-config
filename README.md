# Superset Configurations

This project contains the necessary configurations to deploy **Superset** using **Docker** and **NGINX**. Below is a description of the main files and directories.

## Project Structure

- **certs/**: This directory contains the SSL certificates needed for NGINX HTTPS configuration.

- **docker/**: Directory with additional files and configurations related to Docker.

- **docker-compose.yml**: Docker Compose configuration file to orchestrate the necessary containers for running Superset.

- **nginx.conf**: NGINX configuration file. It configures the reverse proxy and SSL rules.

## Requirements

Make sure to have the following components installed before running the project:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Valid SSL certificates located in the `certs/` directory

## Usage Instructions

### 1. Clone the repository

```bash
git clone git@github.com:arencibiafrancisco/superset-config.git
cd superset-configs
```

### 2. Configure Environment Variables
Before running the containers, you need to configure the environment variables in the .env file located inside the docker/ directory. Open the file and set the necessary values for your environment.

```bash
nano docker/.env
```

### 3. Run Docker Compose
To start all containers, use the following command:

```bash
docker compose up -d
```

### 4. NGINX Configuration
Ensure that the nginx.conf file is correctly set up to redirect traffic to the Superset container and use the SSL certificates found in the certs/ directory.

### 5. Change Superset Admin Password
To change the Superset administrator password, follow these steps:

Open a bash shell inside the running Superset container:

```bash
docker exec -it superset_app /bin/bash
```

Run the following command to reset the admin password:

```bash
superset fab reset-password --username admin --password yourpassword
```

### 6. Access Superset
Once the containers are up and running, you can access Superset in your web browser at the following URL:

```bash
https://<YOUR_DOMAIN_OR_IP>
```
