# Define paths
APP_DIR=$(HOME)/yt2mp3
SCRIPT_NAME=yt2mp3
EXEC_PATH=/usr/local/bin/$(SCRIPT_NAME)

# Install dependencies from requirements.txt
install-requirements:
	pip install -r $(APP_DIR)/requirements.txt

# Create a symbolic link to the script in /usr/local/bin for global access
create-symlink:
	ln -sf $(APP_DIR)/app.py $(EXEC_PATH)

# Install dependencies and create symlink
install: install-requirements create-symlink
