def investment_rating(roi, prediction):

    if prediction == 1 and roi >= 20:
        return "Strong Buy"

    elif roi >= 20:
        return "Buy"

    elif roi >= 10:
        return "Hold"

    elif roi >= 0:
        return "Cautious"

    else:
        return "Avoid"
    
def roi_color(roi):
    if roi >= 20:
        return "#22c55e"   # green
    elif roi >= 10:
        return "#eab308"   # yellow
    elif roi >= 0:
        return "#f97316"   # orange
    else:
        return "#ef4444"   # red