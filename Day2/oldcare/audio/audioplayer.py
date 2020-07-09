# -*- coding: utf-8 -*-
'''
audio player
'''

# import library
from subprocess import Popen
from subprocess import call

# play audio
def play_audio(audio_name):
    try:
        child = Popen('mpg321 ' + audio_name, shell=True) # use mpg321 player
    except KeyboardInterrupt as e:
        print(e)
    finally:
        pass
    return child
if __name__ == '__main__':
    pass