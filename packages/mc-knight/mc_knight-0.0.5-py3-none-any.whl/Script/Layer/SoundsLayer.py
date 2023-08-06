from Script.Layer.Layer import Layer
from Resources.sounds.Sounds import Sounds
from Script.assist.Array import Array
import pygame
import _thread
import time
class SoundsLayer():
    def __init__(self):
        self.sound=Sounds()
    def CreateLayer(self):
        pygame.mixer_music.load(self.sound.GetEement())
    def PlaySound(self):
        _thread.start_new_thread(self.Play,())
    def Play(self):
        while True:
            pygame.mixer_music.play()
            time.sleep(171)
            pygame.mixer_music.stop()