# Use the slim Python image for a smaller footprint
FROM python:3.9-slim

# Set the working directory inside the container to /client
WORKDIR /client

# Copy the requirements.txt file from the client folder on your host to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the content from the client folder into the container’s working directory (/client)
COPY . .

# Specify the command to run the client.py file
CMD ["python", "client.py"]
