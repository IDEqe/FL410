import msvcrt

def get_controls(stall_active, pitch, roll, heading):
    exit_requested = False

    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8').lower()
        if not stall_active:
            if key == 'w':
                pitch += 1
            elif key == 's':
                pitch -= 1
            elif key == 'a':
                roll -= 1
            elif key == 'd':
                roll += 1
            elif key == 'q':
                heading -= 1
            elif key == 'e':
                heading += 1
            elif key == 'x':
                exit_requested = True

        pitch = max(-90, min(90, pitch))
        roll = ((roll + 180) % 360) - 180
        heading %= 360

    return pitch, roll, heading, exit_requested
