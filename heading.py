def update_heading(roll, heading, dt):
    abs_roll = abs(roll)

    if 1 <= abs_roll <= 2:
        heading_rate = 1 / 5
    elif 3 <= abs_roll <= 4:
        heading_rate = 1 / 4
    elif 5 <= abs_roll <= 6:
        heading_rate = 1 / 3
    elif 7 <= abs_roll <= 8:
        heading_rate = 1 / 2
    elif 9 <= abs_roll <= 10:
        heading_rate = 1 / 1
    elif abs_roll > 10:
        seconds_per_degree = max(0.1, 1.0 - 0.1 * (abs_roll - 10))
        heading_rate = 1 / seconds_per_degree
    else:
        heading_rate = 0

    if roll > 0:
        heading += heading_rate * dt
    elif roll < 0:
        heading -= heading_rate * dt

    heading = heading % 360

    return heading
