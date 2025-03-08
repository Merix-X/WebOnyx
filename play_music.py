import pygame
import random

# Inicializace Pygame
pygame.init()

# Seznam skladeb
songs = ["/mnt/data/music.zip/music/fourt_rendez_vous.mp3", "/mnt/data/music.zip/music/titles.mp3"]  # Upravte podle vašich skutečných souborů

# Náhodný výběr skladby
random_song = random.choice(songs)

# Inicializace přehrávače
pygame.mixer.init()

# Přehrání náhodně vybrané skladby
pygame.mixer.music.load(random_song)
pygame.mixer.music.play()

# Udržení programu v činnosti, dokud skladba hraje
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Ukončení Pygame
pygame.quit()