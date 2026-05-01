def compare_roi(current_roi, alt_roi):

    if current_roi > alt_roi:
        return "Current property performs better."

    elif alt_roi > current_roi:
        return "Alternative scenario performs better."

    return "Both scenarios are similar."