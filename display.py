import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_pitch(p):
    arrow = '↑' if p > 0 else '↓' if p < 0 else '→'
    return f"{arrow} {abs(p)}°"

def format_roll(r):
    arrow = '→' if r > 0 else '←' if r < 0 else '─'
    return f"{arrow} {abs(r)}°"

def print_status(airspeed, altitude, pitch, roll, heading, warnings, crashed=False, crash_fill_progress=None):
    clear_screen()

    WIDTH = 60
    HEIGHT = 30
    PFD_OFFSET_X = 18  # offset for tapes/labels
    PFD_OFFSET_Y = 9   # offset for tapes/labels
    GRID_WIDTH = WIDTH + 35
    GRID_HEIGHT = HEIGHT + 18
    center_x = PFD_OFFSET_X + WIDTH // 2
    center_y = PFD_OFFSET_Y + HEIGHT // 2

    # Prepare the display grid
    grid = [[' ' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Draw top and bottom borders (width 60)
    for x in range(center_x - WIDTH // 2, center_x + WIDTH // 2):
        for y in [center_y - HEIGHT // 2, center_y + HEIGHT // 2 - 1]:
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                grid[y][x] = '#'
    # Draw left and right borders (height 30)
    for y in range(center_y - HEIGHT // 2, center_y + HEIGHT // 2):
        for x in [center_x - WIDTH // 2, center_x + WIDTH // 2 - 1]:
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                grid[y][x] = '#'

    # Adjust y_aspect for the new rectangle
    import math
    y_aspect = 2.1

    # If crashed, fill PFD with 'X' (animated if crash_fill_progress is given)
    if crashed:
        fill_count = crash_fill_progress if crash_fill_progress is not None else (WIDTH - 2) * (HEIGHT - 2)
        fill_idx = 0
        for y in range(center_y - HEIGHT // 2 + 1, center_y + HEIGHT // 2 - 1):
            for x in range(center_x - WIDTH // 2 + 1, center_x + WIDTH // 2 - 1):
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    if fill_idx < fill_count:
                        grid[y][x] = 'X'
                        fill_idx += 1
        airspeed = 0
        altitude = max(0, altitude)
    else:
        # Draw pitch lines every 10 degrees up to 40 (above and below horizon), including 0, with banking effect
        roll_rad = math.radians(roll)
        for pitch_deg in range(-40, 41, 10):
            offset = int(pitch_deg - pitch)
            y = int(center_y - offset)
            # Make the line touch the border: dx from -WIDTH//2+1 to WIDTH//2-2
            for dx in range(-WIDTH // 2 + 1, WIDTH // 2 - 1):
                x = int(center_x + dx * math.cos(roll_rad))
                y_line = int(y + dx * math.sin(roll_rad))
                rel_x = x - center_x
                rel_y = (y_line - center_y) * y_aspect
                if (abs(rel_x) < (WIDTH // 2 - 0)) and (abs(rel_y) < (HEIGHT // 2 - 3)):
                    if 0 <= x < GRID_WIDTH and 0 <= y_line < GRID_HEIGHT:
                        grid[y_line][x] = '-'
            label = f"{pitch_deg:+}"
            label_dx = WIDTH // 2 - 4
            label_x = int(center_x + label_dx * math.cos(roll_rad))
            label_y = int(center_y - offset + label_dx * math.sin(roll_rad))
            if (abs(label_x - center_x) < (WIDTH // 2 - 1)) and (abs(label_y - center_y) < (HEIGHT // 2 - 3)):
                if 0 <= label_x < GRID_WIDTH and 0 <= label_y < GRID_HEIGHT:
                    for i, c in enumerate(label):
                        lx = label_x + i
                        if (abs(lx - center_x) < (WIDTH // 2 - 1)) and (0 <= lx < GRID_WIDTH):
                            grid[label_y][lx] = c

        # Draw horizon line (7 x's), always centered horizontally and vertically in the PFD, and override pitch lines
        horizon_y = center_y
        for dx in range(-3, 4):  # -3 to 3 inclusive = 7 positions
            x = center_x + dx
            y = horizon_y
            rel_x = x - center_x
            rel_y = (y - center_y) * y_aspect
            if (abs(rel_x) <= (WIDTH // 2 - 3)) and (abs(rel_y) <= (HEIGHT // 2 - 3)):
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    grid[y][x] = 'x'

    # Remove roll indicator (arc at top of rectangle) and roll pointer (caret '^')
    # (Delete the following code block:)
    # for angle in range(-60, 61, 10):
    #     rad = math.radians(angle)
    #     rx = int(center_x + (WIDTH // 2 - 2) * math.sin(rad))
    #     ry = int(center_y - (HEIGHT // 2 - 2) * math.cos(rad) / y_aspect)
    #     if 0 <= rx < GRID_WIDTH and 0 <= ry < GRID_HEIGHT:
    #         grid[ry][rx] = '|'
    # roll_pointer_angle = math.radians(roll)
    # px = int(center_x + (WIDTH // 2 - 4) * math.sin(roll_pointer_angle))
    # py = int(center_y - (HEIGHT // 2 - 4) * math.cos(roll_pointer_angle) / y_aspect)
    # if 0 <= px < GRID_WIDTH and 0 <= py < GRID_HEIGHT:
    #     grid[py][px] = '^'

    # Draw airspeed (left, horizontally next to rectangle, centered vertically)
    airspeed_str = f"{airspeed:.0f} kts"
    airspeed_x = center_x - WIDTH // 2 - len(airspeed_str) - 2
    airspeed_y = center_y
    for i, c in enumerate(airspeed_str):
        x = airspeed_x + i
        if 0 <= x < GRID_WIDTH and 0 <= airspeed_y < GRID_HEIGHT:
            grid[airspeed_y][x] = c

    # Draw altitude (right, horizontally next to rectangle, centered vertically)
    altitude_str = f"{int(altitude)} ft"
    altitude_x = center_x + WIDTH // 2 + 2
    altitude_y = center_y
    for i, c in enumerate(altitude_str):
        x = altitude_x + i
        if 0 <= x < GRID_WIDTH and 0 <= altitude_y < GRID_HEIGHT:
            grid[altitude_y][x] = c

    # Draw heading and bank just below the rectangle, centered together
    if crashed:
        heading_str = f"HDG {int(heading):03d}"
        bank_str = "Bank: X.X degrees"
    else:
        heading_str = f"HDG {heading:06.3f}"
        bank_str = f"Bank: {roll:.1f}°"
    combined_str = f"{heading_str}   {bank_str}"
    heading_y = center_y + HEIGHT // 2 + 2
    start_x = center_x - len(combined_str) // 2
    for i, c in enumerate(combined_str):
        x = start_x + i
        y = heading_y
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            grid[y][x] = c

    # Print the grid
    print("\n".join("".join(row) for row in grid))

    # Print warnings just below heading
    warning_y = heading_y + 2
    if not isinstance(warnings, list):
        if warnings is None:
            warnings = []
        else:
            warnings = [str(warnings)]

    if warnings:
        print("\n" + " " * (center_x - 4) + "WARNING:")
        for w in warnings:
            print(" " * (center_x - 4) + w)
