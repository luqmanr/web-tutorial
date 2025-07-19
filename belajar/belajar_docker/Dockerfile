# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /workdir

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY ./app.py /workdir/

# Define the command to run the application
# python3 app.py
CMD [ "python3", "app.py" ]