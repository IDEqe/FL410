def get_warnings(pitch, roll, stall_start_time, stall_stage, stall_active, crashed):
    from stall import check_stall
    from bank import check_bank
    warnings, pitch, stall_start_time, stall_stage, stall_active = check_stall(
        pitch, stall_start_time, stall_stage, stall_active)

    # Ensure warnings is a list
    if not isinstance(warnings, list):
        warnings = [warnings]

    bank_warnings = check_bank(roll)
    # Ensure bank_warnings is a list
    if not isinstance(bank_warnings, list):
        bank_warnings = [bank_warnings]

    warnings.extend(bank_warnings)

    warnings = add_crash_warning(warnings, crashed)

    return warnings, pitch, stall_start_time, stall_stage, stall_active

def add_crash_warning(warnings, crashed):
    if crashed and "CRASH!" not in warnings:
        warnings = ["CRASH!"]
    return warnings
