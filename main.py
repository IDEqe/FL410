import time
from display import clear_screen, print_status
from warnings import get_warnings, add_crash_warning
from controls import get_controls
from heading import update_heading
from crash import check_crash
from vsp import VerticalSpeedIndicator

airspeed = 250
altitude = 500
pitch = 0
roll = 0
heading = 0

# New helper for nonlinear pitch-to-vertical-speed mapping
def pitch_to_vspeed(pitch):
    sign = 1 if pitch >= 0 else -1
    abs_pitch = abs(int(round(pitch)))
    if abs_pitch == 0:
        return 0
    return sign * (10 + (abs_pitch - 1) * 5)

stall_start_time = None
stall_stage = 0
stall_active = False

last_time = time.time()

crashed = False
crash_fill_progress = 0

while True:
    import msvcrt
    exit_requested = False
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8').lower()
        if key == 'x':
            break

    if not crashed:
        warnings, pitch, stall_start_time, stall_stage, stall_active = get_warnings(
            pitch, roll, stall_start_time, stall_stage, stall_active, crashed
        )

        pitch, roll, heading, exit_requested = get_controls(stall_active, pitch, roll, heading)
        if exit_requested:
            break

        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        altitude += pitch_to_vspeed(pitch) * dt
        if altitude < 0:
            altitude = 0

        heading = update_heading(roll, heading, dt)
    else:
        time.sleep(0.02)

    crashed, altitude, crash_fill_progress, crash_warning = check_crash(
        altitude, crashed, crash_fill_progress
    )
    if crashed:
        airspeed = 0
        warnings = add_crash_warning(warnings, crashed)

    vsi = VerticalSpeedIndicator(pitch)
    vsi_str = vsi.render()

    print_status(
        airspeed,
        altitude,
        pitch,
        roll,
        heading,
        warnings if not crashed else warnings,
        crashed,
        crash_fill_progress if crashed else None,
        vsi_str
    )

    # Refresh at 1 FPS (1.0s per frame)
    time.sleep(1.0)
