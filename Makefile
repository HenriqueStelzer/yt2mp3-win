INSTALL_DIR := ~/.local/share/txt2b64

install:
	sudo pip3 install -r requirements.txt
	sudo mkdir -p $(INSTALL_DIR)
	sudo mv ../txt2b64 $(INSTALL_DIR)
	sudo pacman -S --noconfirm xclip
	sudo chmod +x $(INSTALL_DIR)/txt2b64

uninstall:
	sudo rm -rf $(INSTALL_DIR)
	sudo pip3 uninstall -r requirements.txt -y

reinstall: uninstall install
