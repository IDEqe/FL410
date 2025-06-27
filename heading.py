def update_heading(roll, heading, dt):
    abs_roll = abs(roll)

    if 1 <= abs_roll <= 2:
        heading_rate = 1 / 5  # degrees per second
    elif 3 <= abs_roll <= 4:
        heading_rate = 1 / 4
    elif 5 <= abs_roll <= 6:
        heading_rate = 1 / 3
    elif 7 <= abs_roll <= 8:
        heading_rate = 1 / 2
    elif 9 <= abs_roll <= 10:
        heading_rate = 1 / 1
    elif abs_roll > 10:
        # For bank angles > 10, heading change speeds up with each degree
        # Starting at 0.9s per degree for 11°, 0.8s for 12°, etc.
        # Calculate seconds per degree by linearly decreasing with bank angle
        seconds_per_degree = max(0.1, 1.0 - 0.1 * (abs_roll - 10))  # don't go below 0.1s
        heading_rate = 1 / seconds_per_degree
    else:
        heading_rate = 0

    # Update heading depending on roll direction
    if roll > 0:
        heading += heading_rate * dt
    elif roll < 0:
        heading -= heading_rate * dt

    # Normalize heading to 0-359
    heading = heading % 360

    return heading
