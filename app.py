import requests
import os

from InquirerPy import prompt
from io import BytesIO
from pytubefix import YouTube
from youtube_search import YoutubeSearch
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TAL

# requirements.txt
#
# pytubefix
# youtube_search
# mutagen
# InquirerPy

def search(user_input):
    try:        
        query = " ".join(user_input)
        
        search_results = YoutubeSearch(query, max_results=5).to_dict()
        
        choices = [{"name": f"{item['title']} ({item['channel']})", "value": item} for item in search_results]
        
        chosen_video = prompt([{
            'type': 'list',
            'name': 'search',
            'message': 'Search Results:',
            'choices': choices,
        }])
        
        chosen_video = chosen_video['search']

        youtube_video = YouTube('https://youtube.com' + chosen_video['url_suffix'], use_oauth=True)
        youtube_audio = youtube_video.streams.filter(only_audio=True).first()
        
        output_file = youtube_audio.download(output_path='.')
        base = os.path.splitext(output_file)[0]
        os.rename(output_file, base + ".mp3")
        
        try:
            audio = MP3(base + ".mp3", ID3=ID3)
            audio.add_tags()
        except HeaderNotFoundError:
            return
        
        audio.tags.add(TIT2(
            encoding=3,
            text=chosen_video["title"]
            ))
        
        audio.tags.add(TPE1(
            encoding=3,
            text=chosen_video["channel"]
            ))
        
        audio.tags.add(TAL(
            encoding=3,
            text=("https://youtube.com" + chosen_video["url_suffix"])
            ))
        
        thumbnail_url = chosen_video["thumbnails"][0]
        response = requests.get(thumbnail_url)
        img_data = BytesIO(response.content)
        with open("cover.jpg", "wb") as cover_file:
            cover_file.write(img_data.getbuffer())
            
        audio.tags.add(APIC(
            encoding=3,
            mime="cover/jpeg",
            type=3,
            desc="Cover Image",
            data=open("cover.jpg", "rb").read()
            ))
        
        os.remove("cover.jpg")
        
        audio.save()
        
        return base + ".mp3"

    except KeyboardInterrupt:
        
        return 1
    
if __name__ == "__main__":

    file = search(input("Search: ").split())
    
    if file == 1:
        print("\033[91m" + "Download interrupted." + "\033[0m")
        
    elif input("Do you want to delete the file? (y/n): ") == "y":
        os.remove(file)
        print("\033[92m" + "File sucessfully deleted." + "\033[0m")