APP_DIR=$(HOME)/yt2mp3
SCRIPT_NAME=yt2mp3
EXEC_PATH=/usr/local/bin/$(SCRIPT_NAME)

install-requirements:
	pip install -r $(APP_DIR)/requirements.txt

create-symlink:
	ln -sf $(APP_DIR)/app.py $(EXEC_PATH)

make-executable:
	chmod +x ~/yt2mp3/app.py


install: install-requirements create-symlink
