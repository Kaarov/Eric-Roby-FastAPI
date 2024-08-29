### To run Dockerfile

### Step 1: Build the Docker Image
```shell
docker build -t fastapi-docker .
```

### Step 2: Run Docker Container
```shell
docker run -d --name fastapi-docker-container -p 80:80 fastapi-docker
```