def check_bank(roll):
    warnings = []
    max_safe_bank = 30  # degrees
    
    if abs(roll) > max_safe_bank:
        warnings.append(f"BANK ANGLE WARNING! {roll}°")
        
    return warnings