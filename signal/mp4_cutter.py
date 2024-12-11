from moviepy.editor import AudioFileClip

# pip install numpy==1.17.3
# pip install moviepy
def mp42wav(mp4_file_path, wav_file_path):
    try:
        audioclip = AudioFileClip(mp4_file_path)
        audioclip.write_audiofile(wav_file_path)
        return True
    except:
        return False

print(mp42wav('test.mp4', 'test.wav'))

