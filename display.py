import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_pitch(p):
    arrow = '↑' if p > 0 else '↓' if p < 0 else '→'
    return f"{arrow} {abs(p)}°"

def format_roll(r):
    arrow = '→' if r > 0 else '←' if r < 0 else '─'
    return f"{arrow} {abs(r)}°"

def print_status(airspeed, altitude, pitch, roll, heading, warnings, crashed=False, crash_fill_progress=None, vsi_str=None):
    # Fill PFD with colored hashtags: brown/orange below 0 deg, blue above 1 deg, keep borders, airplane, pitch lines, numbers intact
    # (Moved after grid, border, and variable initialization)
    clear_screen()
    WIDTH = 90
    HEIGHT = 45
    AIRSPEED_PAD = 14  # Space on the left for airspeed
    PFD_OFFSET_X = AIRSPEED_PAD
    PFD_OFFSET_Y = 0
    GRID_WIDTH = WIDTH + AIRSPEED_PAD
    GRID_HEIGHT = HEIGHT
    center_x = PFD_OFFSET_X + WIDTH // 2
    center_y = PFD_OFFSET_Y + HEIGHT // 2
    # grid, border_top, border_bottom, y_aspect are initialized below
    # ...existing code...
    # After grid, border, and y_aspect are set up:
    # (Insert after y_aspect = 2.1)

    WIDTH = 90
    HEIGHT = 45
    AIRSPEED_PAD = 14  # Space on the left for airspeed
    PFD_OFFSET_X = AIRSPEED_PAD
    PFD_OFFSET_Y = 0
    GRID_WIDTH = WIDTH + AIRSPEED_PAD
    GRID_HEIGHT = HEIGHT
    center_x = PFD_OFFSET_X + WIDTH // 2
    center_y = PFD_OFFSET_Y + HEIGHT // 2

    grid = [[' ' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Draw the border, leaving at least 2 spaces at the top
    border_top = 2
    border_bottom = HEIGHT - 1
    for x in range(PFD_OFFSET_X, PFD_OFFSET_X + WIDTH):
        grid[border_top][x] = '#'
        grid[border_bottom][x] = '#'
    for y in range(border_top, border_bottom + 1):
        grid[y][PFD_OFFSET_X] = '#'
        grid[y][PFD_OFFSET_X + WIDTH - 1] = '#'

    import math
    y_aspect = 2.1

    if crashed:
        # Fill the entire PFD area with fast-changing red Xs, and make all text red
        import random
        fill_count = crash_fill_progress if crash_fill_progress is not None else (WIDTH - 2) * (HEIGHT - 2)
        fill_idx = 0
        for y in range(HEIGHT):
            for x in range(GRID_WIDTH):
                # Fill only inside the PFD border
                if (border_top < y < border_bottom and PFD_OFFSET_X < x < PFD_OFFSET_X + WIDTH - 1):
                    # Use random Xs for fast-changing effect
                    grid[y][x] = '\033[31mX\033[0m' if random.random() > 0.2 else '\033[91mX\033[0m'
                else:
                    # Keep border as red
                    if grid[y][x] == '#':
                        grid[y][x] = '\033[31m#\033[0m'
        airspeed = 0
        altitude = max(0, altitude)
    else:
        roll_rad = math.radians(roll)
        for pitch_deg in range(-90, 91, 10):
            offset = int(pitch_deg - pitch)
            # Draw pitch lines with three spaces from the border (do not touch border)
            left_x = PFD_OFFSET_X + 3
            right_x = PFD_OFFSET_X + WIDTH - 4
            y_left = int(center_y - offset + (left_x - center_x) * math.sin(roll_rad))
            y_right = int(center_y - offset + (right_x - center_x) * math.sin(roll_rad))
            steps = abs(right_x - left_x)
            # Choose pitch line symbol based on bank angle
            abs_roll = abs(roll)
            if abs_roll >= 88 and abs_roll <= 92:
                pitch_char = '|'
            elif roll <= -30:
                pitch_char = '/'
            elif roll >= 30:
                pitch_char = '\\'
            else:
                pitch_char = '-'
            for step in range(steps + 1):
                x = left_x + step
                y_line = int(y_left + (y_right - y_left) * (step / steps))
                rel_x = x - center_x
                rel_y = (y_line - center_y) * y_aspect
                # Ensure all pitch lines are always visible within the PFD area
                if (PFD_OFFSET_X + 1 <= x < PFD_OFFSET_X + WIDTH - 1) and (border_top + 1 <= y_line < border_bottom):
                    grid[y_line][x] = pitch_char
            # Draw pitch number at the right end of the line, just inside the border
            label = f"{pitch_deg:+}"
            label_x = PFD_OFFSET_X + WIDTH - 2 - len(label) - 1  # 1 space from border
            label_y = int(center_y - offset)
            if border_top < label_y < border_bottom:
                for i, c in enumerate(label):
                    lx = label_x + i
                    if 0 <= lx < GRID_WIDTH:
                        grid[label_y][lx] = c

        # Draw horizon line, always visible and never overwritten
        horizon_y = center_y
        for dx in range(-3, 4):
            x = center_x + dx - 1
            y = horizon_y
            # Ensure horizon line is always visible within the PFD area
            if (PFD_OFFSET_X + 1 <= x < PFD_OFFSET_X + WIDTH - 1) and (border_top + 1 <= y < border_bottom):
                grid[y][x] = 'x'

    # Fill PFD with colored hashtags: yellow below 0 deg pitch line, blue above (including 0),
    # keep borders, airplane, pitch lines, numbers intact. Color moves with pitch.
    for y in range(border_top + 1, border_bottom):
        for x in range(PFD_OFFSET_X + 1, PFD_OFFSET_X + WIDTH - 1):
            # Skip if already drawn (border, pitch lines, horizon, airplane, numbers, etc.)
            if grid[y][x] != ' ':
                continue
            # Calculate pitch for this y (relative to current pitch)
            rel_y = y - center_y
            pitch_here = -rel_y / y_aspect + pitch
            if pitch_here < 0:
                # Yellow (ANSI 33)
                grid[y][x] = '\033[33m#\033[0m'
            else:
                # Blue (ANSI 34)
                grid[y][x] = '\033[34m#\033[0m'

    # Warnings (single line, above horizon)
    if not isinstance(warnings, list):
        if warnings is None:
            warnings = []
        else:
            warnings = [str(warnings)]

    stall_shift = 0
    # --- Add PRIMARY FLIGHT DISPLAY title above warnings ---
    title_text = "PRIMARY FLIGHT DISPLAY"
    title_line = f"\033[37m{title_text}\033[0m"
    title_y = border_top - 2
    title_x = PFD_OFFSET_X + (WIDTH // 2) - (len(title_text) // 2)
    if 0 <= title_y < HEIGHT:
        for i, c in enumerate(title_line):
            x = title_x + i
            if PFD_OFFSET_X + 1 <= x < PFD_OFFSET_X + WIDTH - 1:
                grid[title_y][x] = c

    warn_y = border_top - 1
    if crashed or altitude <= 0:
        # Only show the custom CRASH warning when crashed or altitude <= 0
        crash_warning = "CRASH CRASH CRASH CRASH CRASH CRASH"
        warning_line = f"\033[31m{crash_warning}\033[0m"
        warn_x = PFD_OFFSET_X + (WIDTH // 2) - (len(crash_warning) // 2)
        if 0 <= warn_y < HEIGHT:
            for i, c in enumerate(warning_line):
                x = warn_x + i
                if PFD_OFFSET_X + 1 <= x < PFD_OFFSET_X + WIDTH - 1:
                    grid[warn_y][x] = c
    elif warnings:
        # Show all warnings (colored red) during normal flight
        colored_warnings = []
        for w in warnings:
            w_str = str(w)
            if "\033[31m" not in w_str:
                w_str = f"\033[31m{w_str}\033[0m"
            colored_warnings.append(w_str)
        warning_line = '   '.join(colored_warnings)
        warn_x = PFD_OFFSET_X + (WIDTH // 2) - (len(''.join([str(w) for w in warnings])) // 2)
        if 0 <= warn_y < HEIGHT:
            for i, c in enumerate(warning_line):
                x = warn_x + i
                if PFD_OFFSET_X + 1 <= x < PFD_OFFSET_X + WIDTH - 1:
                    grid[warn_y][x] = c

    # ...existing code...
    # When printing lines, shift after STALL STALL if needed
    # (Find the print loop and add the shift)


    # Compose airspeed, altitude, vsi for horizon line
    airspeed_str = f"\033[33m{airspeed:.0f} kts\033[0m"
    altitude_str = f"\033[32m{int(altitude)} ft\033[0m"
    vsi_indicator = "---"
    if crashed:
        vsi_indicator = "NONE"
    elif vsi_str:
        for line_vsi in vsi_str.splitlines():
            if "---" in line_vsi or "\\" in line_vsi or "/" in line_vsi:
                vsi_indicator = line_vsi.strip().split()[-1]
                break
    # Dynamic VSI column: show 'x' above 0 for climb, '-x' below 0 for descent, based on vertical speed
    vsi_zero = '0'
    vsi_column = []
    # Determine vertical speed magnitude (from pitch)
    try:
        vsi_val = 0
        if vsi_indicator == '\\':
            vsi_val = 5  # max climb
        elif vsi_indicator == '/':
            vsi_val = -5  # max descent
        else:
            vsi_val = 0
    except Exception:
        vsi_val = 0

    # Show 5 numbers above zero, then zero, then 5 numbers below zero (for a total of 11 lines)
    # Custom VSI labels: 6k, 3k, 1k, 500, 200, 0, -200, -500, -1k, -3k, -6k
    vsi_labels = [
        ('5', '6k'),
        ('4', '3k'),
        ('3', '1k'),
        ('2', '500'),
        ('1', '200'),
        ('0', '0'),
        ('-1', '-200'),
        ('-2', '-500'),
        ('-3', '-1k'),
        ('-4', '-3k'),
        ('-5', '-6k'),
    ]
    vsi_column = [label for num, label in vsi_labels]

    # Adjust label positions: move 6k, 3k, 1k and their negatives 2 spaces left; 500, 200 and their negatives 3 spaces left
    def adjust_vsi_label(label, idx):
        if label in ('6k', '3k', '1k'):
            return '  ' + label
        if label in ('-6k', '-3k', '-1k'):
            return '  ' + label
        if label in ('500', '200'):
            return '   ' + label
        if label in ('-500', '-200'):
            return '   ' + label
        return label
    vsi_column = [adjust_vsi_label(label, i) for i, label in enumerate(vsi_column)]

    # Compose the VSI display base string for the '0' line
    # For the column, we want to show the altitude, the 0, and the VSI indicator (or a placeholder)
    # Use symbolic VSI: '\' for up, '/' for down, '-' for level, 'X' for crash/ground
    if crashed or altitude <= 0:
        vsi_indicator = 'X'
    else:
        if pitch > 0:
            vsi_indicator = '\\'
        elif pitch < 0:
            vsi_indicator = '/'
        else:
            vsi_indicator = '---'
    vsi_display_base = f"{altitude_str}   0   {vsi_indicator}"  # 2 spaces before 0, 3 before indicator
    zero_index = vsi_display_base.find('0')
    # Compose multi-line VSI display, aligning the '0' in the column with the '0' in the string
    # The VSI column will always be at a fixed position (e.g., col 78 for 'x', col 77 for '-x')
    # Move numbers further to the left (smaller column index)
    # QUICK FIX: Move VSI numbers further left for better alignment
    # Individual horizontal positions for each VSI label (from 6k to -6k, including 0)
    VSI_LABEL_X_COLS = {
        '6k': PFD_OFFSET_X - 8,
        '3k': PFD_OFFSET_X - 8,
        '1k': PFD_OFFSET_X - 8,
        '500': PFD_OFFSET_X - 10,
        '200': PFD_OFFSET_X - 10,
        '0': PFD_OFFSET_X - 4,
        '-200': PFD_OFFSET_X - 11,
        '-500': PFD_OFFSET_X - 11,
        '-1k': PFD_OFFSET_X - 9,
        '-3k': PFD_OFFSET_X - 9,
        '-6k': PFD_OFFSET_X - 9,
    }
    vsi_display_lines = []
    for i, val in enumerate(vsi_column):
        line = [' '] * (GRID_WIDTH)
        # For each label, use its own horizontal position
        label_stripped = val.strip()
        x_col = VSI_LABEL_X_COLS.get(label_stripped, PFD_OFFSET_X - 10)
        if val == '0':
            # Place the altitude string and VSI indicator at the left, as before
            base = vsi_display_base
            for idx, c in enumerate(base):
                if idx < GRID_WIDTH:
                    line[idx] = c
        else:
            if x_col < GRID_WIDTH - 1:
                for idx, c in enumerate(val):
                    if x_col + idx < GRID_WIDTH:
                        line[x_col + idx] = c
        vsi_display_lines.append(''.join(line).rstrip())

    # Print grid, inject airspeed and altitude/vsi outside PFD on horizon line
    # Print grid, inject airspeed and altitude/vsi outside PFD on horizon line
    vsi_center_y = center_y
    vsi_start_y = vsi_center_y - 5
    vsi_end_y = vsi_center_y + 5
    for y in range(HEIGHT):
        line = "".join(grid[y])
        # If crashed, make all output red
        if crashed:
            line = f"\033[31m{line}\033[0m"
        # Only print the PFD area (between borders)
        if border_top <= y <= border_bottom:
            if vsi_start_y <= y <= vsi_end_y:
                vsi_line = vsi_display_lines[y - vsi_start_y]
            else:
                vsi_line = ''
            if y == center_y:
                left_border = line.find('#')
                right_border = line.rfind('#')
                pfd_content = line[left_border+1:right_border]
                abs_roll = abs(roll)
                if abs_roll >= 88 and abs_roll <= 92:
                    airplane_symbol = '|'
                elif roll <= -30:
                    airplane_symbol = '/'
                elif roll >= 30:
                    airplane_symbol = '\\'
                else:
                    airplane_symbol = '|'
                airplane_pos = pfd_content.find('xxxxxxx')
                if airplane_pos == -1:
                    airplane_pos = len(pfd_content) // 2 - 3
                    pfd_content = (
                        pfd_content[:airplane_pos] +
                        '   ' + airplane_symbol + '   ' +
                        pfd_content[airplane_pos+7:]
                    )
                import re
                pfd_content = re.sub(r'(-+)([ ]?[\+\-]?0)$', lambda m: ' ' * (len(m.group(1)) - 2) + '  ' + m.group(2), pfd_content)
                left = airspeed_str.rjust(AIRSPEED_PAD - 4) + '  '
                # Add PFD left and right border
                pfd_line = '|' + pfd_content + '|'
                # Only add left space if not displaying VSI x marker
                if vsi_line.strip() == 'x' or vsi_line.strip().startswith('-x'):
                    right = '  ' + vsi_line
                else:
                    right = '  ' + vsi_line if vsi_line else ''
                prefix = ' ' * stall_shift if stall_shift else '     '
                print(prefix + left + pfd_line + right)
            else:
                left_border = line.find('#')
                right_border = line.rfind('#')
                if vsi_start_y <= y <= vsi_end_y:
                    vsi_line = vsi_display_lines[y - vsi_start_y]
                else:
                    vsi_line = ''
                # Add PFD left and right border
                pfd_line = '|' + line[left_border+1:right_border] + '|'
                # Only add left space if not displaying VSI x marker
                if vsi_line.strip() == 'x' or vsi_line.strip().startswith('-x'):
                    right = '  ' + vsi_line
                else:
                    right = '  ' + vsi_line if vsi_line else ''
                print(' ' * (AIRSPEED_PAD) + pfd_line + right)
        else:
            print(line)

    # Print heading, VSI, and bank just once, centered below the PFD
    if crashed:
        heading_str = f"HDG {int(heading):03d}"
        vsi_str_display = "VSI: X FPM"
        bank_str = "Bank: X.X degrees"
    else:
        heading_str = f"HDG {heading:06.3f}"
        # Use new nonlinear pitch-to-vspeed mapping, but in feet per minute
        def pitch_to_vspeed_fpm(pitch):
            sign = 1 if pitch >= 0 else -1
            abs_pitch = abs(int(round(pitch)))
            if abs_pitch == 0:
                return 0
            return sign * (10 + (abs_pitch - 1) * 5) * 60
        vsi_rate_fpm = pitch_to_vspeed_fpm(pitch)
        if altitude <= 0:
            vsi_str_display = "VSI: X FPM"
        else:
            vsi_str_display = f"VSI: {vsi_rate_fpm:+d} FPM"
        bank_str = f"Bank: {roll:.1f}°"
    combined_str = f"{heading_str}   {vsi_str_display}   {bank_str}"
    # Print one blank line, then the indicators, centered below the PFD bottom border
    print()  # blank line
    print(" " * (center_x - len(combined_str) // 2) + combined_str)

    # (Warnings below heading/bank if needed, not duplicated)

