def check_crash(altitude, crashed, crash_fill_progress):
    """
    Returns:
        crashed (bool): True if crash detected or ongoing
        altitude (float): clipped to >= 0
        crash_fill_progress (int): for animation
        crash_warning (str or None): "CRASH!" if crashed, else None
    """
    crash_warning = None
    if not crashed and altitude <= 0:
        crashed = True
        altitude = 0
        crash_fill_progress = 0
        crash_warning = "CRASH!"
    elif crashed:
        altitude = max(0, altitude)
        crash_fill_progress += 60  # Animation speed
        crash_warning = "CRASH!"
    return crashed, altitude, crash_fill_progress, crash_warning
