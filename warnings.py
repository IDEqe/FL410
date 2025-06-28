def get_warnings(pitch, roll, stall_start_time, stall_stage, stall_active, crashed):
    from stall import check_stall
    from bank import check_bank
    warnings, pitch, stall_start_time, stall_stage, stall_active = check_stall(
        pitch, stall_start_time, stall_stage, stall_active)

    if not isinstance(warnings, list):
        warnings = [warnings]

    bank_warnings = check_bank(roll)
    if not isinstance(bank_warnings, list):
        bank_warnings = [bank_warnings]

    short_map = {
        # Customize your warning texts here:
        "STALL WARNING": "STALL STALL",  # Example: add spaces for shifting/centering
        "BANK ANGLE WARNING": "BANK ANGLE",   # Example: add arrows or symbols
        "CRASH!": "!!! CRASH !!!"               # Example: add exclamation marks
    }
    all_warnings = []
    seen = set()
    for w in warnings + bank_warnings:
        if not w:
            continue
        w_str = str(w).upper()
        for key, short in short_map.items():
            if key in w_str:
                w_str = short
        if w_str not in seen:
            all_warnings.append(w_str)
            seen.add(w_str)

    all_warnings = add_crash_warning(all_warnings, crashed)
    return all_warnings, pitch, stall_start_time, stall_stage, stall_active

def add_crash_warning(warnings, crashed):
    if crashed and "CRASH" not in warnings:
        warnings = ["CRASH"]
    return warnings
    if crashed and "CRASH" not in warnings:
        warnings = ["CRASH"]
    return warnings
