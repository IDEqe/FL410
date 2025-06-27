import time

def check_stall(pitch, stall_start_time, stall_stage, stall_active):
    warnings = []
    current_time = time.time()

    # Stall trigger at 25 deg
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

        # Stall lasts about 8 seconds, pitch decreases smoothly and faster
        # 0-1s: hold pitch, 1-3s: decrease to 0, 3-5s: decrease to -10, 5-7s: decrease to -20, 7-8s: decrease to -25
        if elapsed < 1:
            # Hold initial pitch
            stall_pitch = max(pitch, 26)
        elif elapsed < 3:
            # Smoothly decrease to 0
            t = (elapsed - 1) / 2  # 0 to 1
            stall_pitch = max(0, int(round((1 - t) * max(pitch, 26))))
        elif elapsed < 5:
            # Smoothly decrease to -10
            t = (elapsed - 3) / 2  # 0 to 1
            stall_pitch = int(round((1 - t) * 0 + t * -10))
        elif elapsed < 7:
            # Smoothly decrease to -20
            t = (elapsed - 5) / 2  # 0 to 1
            stall_pitch = int(round((1 - t) * -10 + t * -20))
        elif elapsed < 8:
            # Smoothly decrease to -25
            t = (elapsed - 7) / 1  # 0 to 1
            stall_pitch = int(round((1 - t) * -20 + t * -25))
        else:
            # Recovery complete
            stall_pitch = -25
            stall_active = False
            stall_stage = 5

        # Set stall_stage for compatibility (not used for logic anymore)
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
