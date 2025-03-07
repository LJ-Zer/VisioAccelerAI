import os
import subprocess
import sys
import time

###Sample for John

# Path to the local repository directory
repository_path = "/home/ubuntu/Desktop/Face-Detected"

# Configure Git with user name and email
subprocess.run(['git', 'config', '--global', 'user.email', '20-06391@g.batstate-u.edu.ph'])
subprocess.run(['git', 'config', '--global', 'user.name', 'Zer-000'])

try:
    while True:
      
        # Change to the repository directory
        os.chdir(repository_path)

        # Pull the latest changes from the remote repository
        subprocess.run(['git', 'pull'])

        # Get a list of all files in the directory
        files = os.listdir(repository_path)

        # Iterate over each file and add, commit, and push
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Add the specific photo file to the repository's staging area
                subprocess.run(['git', 'add', '.', file])

                # Commit the changes with a commit message
                subprocess.run(['git', 'commit', '-m', f'Upload {file}'])

                # Push the changes to the remote repository on GitHub
                subprocess.run(['git', 'push'])

        # Add a delay of 5 seconds before the next iteration
        time.sleep(5)

except KeyboardInterrupt:
    sys.exit()

