import time

def check_stall(pitch, stall_start_time, stall_stage, stall_active):
    warnings = []
    current_time = time.time()

    if pitch > 25 and not stall_active:
        stall_start_time = current_time
        stall_stage = 0
        stall_active = True
        stall_pitch = pitch
    else:
        stall_pitch = pitch

    if stall_active:
        warnings.append("STALL WARNING!")
        elapsed = current_time - stall_start_time

        if elapsed < 1:
            stall_pitch = max(pitch, 26)
        elif elapsed < 3:
            t = (elapsed - 1) / 2
            stall_pitch = max(0, int(round((1 - t) * max(pitch, 26))))
        elif elapsed < 5:
            t = (elapsed - 3) / 2
            stall_pitch = int(round((1 - t) * 0 + t * -10))
        elif elapsed < 7:
            t = (elapsed - 5) / 2
            stall_pitch = int(round((1 - t) * -10 + t * -20))
        elif elapsed < 8:
            t = (elapsed - 7) / 1
            stall_pitch = int(round((1 - t) * -20 + t * -25))
        else:
            stall_pitch = -25
            stall_active = False
            stall_stage = 5

        if elapsed < 1:
            stall_stage = 0
        elif elapsed < 3:
            stall_stage = 1
        elif elapsed < 5:
            stall_stage = 2
        elif elapsed < 7:
            stall_stage = 3
        elif elapsed < 8:
            stall_stage = 4
        else:
            stall_stage = 5
    else:
        stall_stage = 0

    return warnings, stall_pitch, stall_start_time, stall_stage, stall_active