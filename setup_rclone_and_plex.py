import os
import subprocess
import requests

# Variables
rclone_conf_url = "https://example.com/path/to/rclone.conf"  # Replace with your rclone.conf URL
plex_media_server_url = "https://downloads.plex.tv/plex-media-server-new/1.40.4.8679-424562606/plexmediaserver_1.40.4.8679-424562606_amd64.deb"  # Replace with your Plex Media Server URL
remotes = {
    "remote1": "/mnt/remote1",
    "remote2": "/mnt/remote2",
    # Add more remotes if needed
}

# Download rclone.conf file
rclone_conf_path = "/root/.config/rclone/rclone.conf"
os.makedirs(os.path.dirname(rclone_conf_path), exist_ok=True)

response = requests.get(rclone_conf_url)
with open(rclone_conf_path, 'wb') as file:
    file.write(response.content)

# Mount rclone remotes
def mount_rclone_remote(remote_name, mount_point):
    os.makedirs(mount_point, exist_ok=True)
    command = [
        "rclone", "mount", remote_name + ":", mount_point,
        "--allow-other", "--vfs-cache-mode", "writes"
    ]
    subprocess.Popen(command)

for remote, mount_point in remotes.items():
    mount_rclone_remote(remote, mount_point)

# Download and install Plex Media Server
plex_media_server_deb = "/tmp/plexmediaserver.deb"
response = requests.get(plex_media_server_url)
with open(plex_media_server_deb, 'wb') as file:
    file.write(response.content)

subprocess.run(["dpkg", "-i", plex_media_server_deb])
subprocess.run(["apt-get", "install", "-f", "-y"])

# Wait for user input to keep the container running
input("Press Enter to stop...")
