import time
from display import clear_screen, print_status
from warnings import get_warnings, add_crash_warning
from controls import get_controls
from heading import update_heading
from crash import check_crash

airspeed = 250
altitude = 3000
pitch = 0
roll = 0
heading = 0  # new variable for heading in degrees 0-359

stall_start_time = None
stall_stage = 0
stall_active = False

last_time = time.time()

crashed = False
crash_fill_progress = 0  # Number of Xs to fill in the PFD

while True:
    # clear_screen() is now called inside print_status for smoother display

    if not crashed:
        warnings, pitch, stall_start_time, stall_stage, stall_active = get_warnings(
            pitch, roll, stall_start_time, stall_stage, stall_active, crashed  # pass crashed here
        )

        pitch, roll, heading, exit_requested = get_controls(stall_active, pitch, roll, heading)
        if exit_requested:
            break

        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        altitude += pitch * 10 * dt  # altitude changes 10 ft/sec per pitch degree
        if altitude < 0:
            altitude = 0

        heading = update_heading(roll, heading, dt)  # update heading based on roll and elapsed time

    else:
        # Only allow exit (X) when crashed, freeze all other controls and heading
        import msvcrt
        exit_requested = False
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'x':
                break
        time.sleep(0.02)

    # Crash detection and animation
    crashed, altitude, crash_fill_progress, crash_warning = check_crash(
        altitude, crashed, crash_fill_progress
    )
    if crashed:
        airspeed = 0
        warnings = add_crash_warning(warnings, crashed)

    print_status(
        airspeed,
        altitude,
        pitch,
        roll,
        heading,
        warnings if not crashed else warnings,
        crashed=crashed,
        crash_fill_progress=crash_fill_progress if crashed else None
    )

    if not crashed:
        time.sleep(0.08)  # Increase sleep to reduce flicker (about 12 FPS)
        time.sleep(0.08)  # Increase sleep to reduce flicker (about 12 FPS)
        time.sleep(0.08)  # Increase sleep to reduce flicker (about 12 FPS)
