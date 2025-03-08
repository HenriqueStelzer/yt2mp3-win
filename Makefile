install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	sudo pacman -S --noconfirm xclip
	mkdir -p ~/.local/bin
	mv ../yt2mp3 ~/.local/bin/
	chmod +x ~/.local/bin/yt2mp3/yt2mp3
	export PATH="\$PATH:\$HOME\.local\bin\yt2mp3"
	source ~/.bashrc
	source venv/bin/activate


uninstall:
	rm -rf ~/.local/bin/yt2mp3
	rm -rf venv
	sed -i '/export PATH="\$PATH:\$HOME\.local\bin\yt2mp3"/d' ~/.bashrc
	source ~/.bashrc

reinstall: uninstall install
