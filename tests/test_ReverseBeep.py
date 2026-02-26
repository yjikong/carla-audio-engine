from ..FMOD.Sounds import ReverseBeep

if __name__ == '__main__':
    reverse_beep = ReverseBeep()
    while True:
        reverse_beep.play()