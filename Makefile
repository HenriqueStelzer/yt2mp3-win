APP_DIR=~/.local/bin/yt2mp3

move-folder:
	mv ../yt2mp3 $(APP_DIR)

install-requirements:
	pip install -r $(APP_DIR)/requirements.txt --break-system-packages

add-alias:
	echo "alias yt2mp3='python3 $(APP_DIR)/app.py'" >> ~/.bashrc
	source ~/.bashrc

remove-folder:
	rm -rf $(APP_DIR)

remove-alias:
	sed -i '/alias yt2mp3/d' ~/.bashrc
	source ~/.bashrc

install: move-folder install-requirements add-alias
uninstall: remove-folder remove-alias
