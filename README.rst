
# OpenWeatherAPI

Async requests for weather data

# Docker Installation

In this guide, you will demonstrate how to install Docker Compose server and how to get started using this tool.

```bash
  sudo apt update
```
```bash
  sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
```bash
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```bash
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
```bash
  apt-cache policy docker-ce
```
```bash
  sudo apt install docker-ce
```
```bash
  sudo systemctl status docker
```

# Docker-compose Installation

In this guide, you will demonstrate how to install Docker Compose server and how to get started using this tool.

```bash
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```bash
  sudo chmod +x /usr/local/bin/docker-compose
```
```bash
  docker-compose --version
```

# How to run

Create .env file

Execute docker-compose.yml file

```bash
  docker-compose up -d --build
```

Populate database through migration tool alembic

```bash
  docker ps -a
```
```bash
  docker exec it <openweather-api container-id> sh
```

```bash
  alembic upgrade 3d144f520f5c
```

Acess API documentation in 0.0.0.0:5000/docs