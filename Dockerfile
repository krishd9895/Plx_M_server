# Use Ubuntu as the base image
FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    fuse \
    python3 \
    python3-pip \
    && apt-get clean

# Install rclone
RUN curl https://rclone.org/install.sh | bash

# Copy the Python script
COPY setup_rclone_and_plex.py /setup_rclone_and_plex.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Python script to set up rclone and Plex
RUN python3 /setup_rclone_and_plex.py

# Expose Plex Media Server port
EXPOSE 32400

# Start Plex Media Server
CMD ["plexmediaserver"]
