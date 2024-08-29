# Use the official Python image with Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the local directory to the /app directory in the container
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
# No-cache-dir: Don't cache the installed packages to save space
# Upgrade: Upgrade all specified packages to the newest available version
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire app directory (containing main.py and any other files) from the local directory to the /app directory
COPY ./app /app

# Set the command to run the application using uvicorn
# "main:app" tells uvicorn to look for an object called app in a module named main (main.py)
# --host 0.0.0.0: Bind socket to all network interfaces (makes the server accessible from outside the container)
# --port 80: Listen on port 80 inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
