INSTALL_DIR := ~/.local/bin/yt2mp3

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	sudo pacman -S --noconfirm xclip
	mkdir -p ~/.local/bin
	mv ../yt2mp3 ~/.local/bin/
	sudo chmod +x ~/.local/bin/yt2mp3/yt2mp3

uninstall:
	rm -rf ~/.local/bin/yt2mp3
	rm -rf venv

reinstall: uninstall install
