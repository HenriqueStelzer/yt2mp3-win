install:  
	python3 -m venv venv  
	. venv/bin/activate && pip install -r requirements.txt  
	mkdir -p ~/.local/bin  
	mv ../yt2mp3 ~/.local/bin/  
	chmod +x ~/.local/bin/yt2mp3  

clean:  
	rm -rf venv  
	rm -rf ~/.local/bin/yt2mp3  
