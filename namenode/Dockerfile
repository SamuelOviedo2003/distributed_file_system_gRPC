# Use the slim Python image for a smaller footprint
FROM python:3.9-slim

# Set the working directory inside the container to /namenode
WORKDIR /namenode

# Copy the requirements.txt file from the namenode folder on your host to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the content from the namenode folder into the container’s working directory ()
COPY . .

EXPOSE 50051


# Specify the command to run the namenode.py file
CMD ["python", "namenode.py"]