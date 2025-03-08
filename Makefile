APP_DIR=$(HOME)/yt2mp3
SCRIPT_NAME=yt2mp3
EXEC_PATH=/usr/local/bin/$(SCRIPT_NAME)

create-venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		python3 -m venv $(VENV_DIR); \
		echo "Virtual environment created at $(VENV_DIR)"; \
	else \
		echo "Virtual environment already exists"; \
	fi

install-requirements:
	pip install -r $(APP_DIR)/requirements.txt

create-symlink:
	ln -sf $(APP_DIR)/app.py $(EXEC_PATH)

make-executable:
	chmod +x ~/yt2mp3/app.py


install: create-venv install-requirements create-symlink
