"""
Audio management module.
Handles initialization of the mixer and safe playback of sound files.
"""
import pygame
import os

class AudioManager:
    """Controls SFX and background music playback."""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sfx(self, name, path):
        """Safely loads a sound and prints a message if it fails."""
        if os.path.exists(path):
            self.sounds[name] = pygame.mixer.Sound(path)
            print(f"✅ Successfully loaded sound: {name}")
        else:
            print(f"❌ ERROR: File not found at {path}. Check your 'assets' folder!")

    def play_sfx(self, name):
        """Play a specific sound by its key name."""
        if name in self.sounds:
            self.sounds[name].play()

    def start_music(self, path):
        """Stream and loop background music."""
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)