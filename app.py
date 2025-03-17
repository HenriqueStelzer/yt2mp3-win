#!/usr/bin/env python3

import librosa
import librosa.display
import requests
import os
import soundfile as sf
import subprocess

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
# librosa
# soundfile

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

        artist = input("What is the artist name? ")
        if not artist:
            artist = chosen_video["channel"]
        
        music = input("What is the music name? ") 
        if not music:
            music = chosen_video["title"]

        base = os.path.splitext(artist + " - " + music)[0]

        os.rename(output_file, base + ".mp3")

        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"{base}.mp3", f"{base}.wav"], check=True)
        subprocess.run(["rm", "-f", f"{base}.mp3"], check=True)

        if input("Modify audio? (y/n) ") in ["y", "Y"]:
            semitones = float(input("How many semitones to shift? (0 for none): "))
            speed = float(input("Speed factor (1.0 for normal): "))
            audio_modify(base + ".wav", semitones, speed)
        
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"{base}.wav", "-b:a", "192k", f"{base}.mp3"], check=True)
        os.remove(f"{base}.wav")

        try:
            audio = MP3(base + ".mp3", ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
        except HeaderNotFoundError:
            return base + ".mp3"
        
        audio.tags.add(TIT2(
            encoding=3,
            text=music
            ))
        
        audio.tags.add(TPE1(
            encoding=3,
            text=artist
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

def audio_modify(path, semitones, speed):
    audio_data, sample_rate = librosa.load(path, sr=None)

    if semitones != 0:
        modified_audio = librosa.effects.pitch_shift(y=audio_data, sr=sample_rate, n_steps=semitones)

    if speed != 1:
        modified_audio = librosa.effects.time_stretch(y=audio_data, rate=speed)

    sf.write(path, modified_audio, sample_rate)
    
if __name__ == "__main__":

    file = search(input("Search: ").split())
    
    if file == 1:
        print("\033[91m" + "Download interrupted." + "\033[0m")
    
    else:
        print("\033[92m" + str(file) + " was downloaded sucessfully." + "\033[0m")

