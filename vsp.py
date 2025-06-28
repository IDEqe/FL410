
# Climb and Descent tables (ft/s) for given pitch degrees
CLIMB_TABLE = [
    (0, 0), (1, 10), (2, 20), (3, 30), (4, 40), (5, 50), (6, 60), (7, 70), (8, 80), (9, 90), (10, 100),
    (11, 112), (12, 124), (13, 136), (14, 148), (15, 160), (16, 168), (17, 175), (18, 180), (19, 185), (20, 190),
    (21, 193), (22, 195), (23, 197), (24, 198), (25, 200), (26, 201), (27, 201), (28, 201), (29, 201), (30, 200),
    (35, 180), (40, 140), (45, 80), (50, 20), (60, 0), (70, 0), (80, 0), (90, 0)
]

DESCENT_TABLE = [
    (-1, -12), (-2, -25), (-3, -38), (-4, -52), (-5, -65), (-10, -130), (-15, -200), (-20, -250), (-25, -300),
    (-30, -350), (-40, -400), (-50, -420), (-60, -450), (-70, -480), (-80, -500), (-90, -520)
]

def get_vertical_speed(pitch_deg):
    """
    Returns vertical speed (ft/s) for a given pitch (degrees).
    Uses the climb table for pitch >= 0, descent table for pitch < 0.
    Interpolates between table values for in-between pitches.
    """
    if pitch_deg >= 0:
        table = CLIMB_TABLE
    else:
        table = DESCENT_TABLE
    prev_p, prev_v = table[0]
    for p, v in table:
        if pitch_deg == p:
            return v
        if (pitch_deg < p and pitch_deg >= 0) or (pitch_deg > p and pitch_deg < 0):
            break
        prev_p, prev_v = p, v
    # Linear interpolation
    if p == prev_p:
        return v
    ratio = (pitch_deg - prev_p) / (p - prev_p)
    value = prev_v + (v - prev_v) * ratio
    return int(round(value))



# For backward compatibility: provide a VerticalSpeedIndicator class
class VerticalSpeedIndicator:
    def __init__(self, pitch_deg: float):
        self.pitch_deg = pitch_deg
        self.vspeed_fps = get_vertical_speed(self.pitch_deg)
        self.vspeed_fpm = self.vspeed_fps * 60

    def get_indicator(self) -> str:
        if self.pitch_deg > 0:
            return '\\'
        elif self.pitch_deg < 0:
            return '/'
        elif self.pitch_deg == 0:
            return '---'
        else:
            return 'X'

    def render(self) -> str:
        return self.get_indicator()

# Example usage for testing
if __name__ == "__main__":
    for pitch in range(-20, 21, 2):
        print(f"Pitch {pitch:+3d}°: {get_vertical_speed(pitch):+4d} ft/s")