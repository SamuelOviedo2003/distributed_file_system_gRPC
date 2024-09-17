# Use the slim Python image for a smaller footprint
FROM python:3.9-slim

# Set the working directory inside the container to /datanode
WORKDIR /datanode

# Copy the requirements.txt file from the datanode folder on your host to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the content from the datanode folder into the container’s working directory ()
COPY . .

# Specify the command to run the datanode.py file
CMD ["python", "datanode.py", "--port", "50052"]