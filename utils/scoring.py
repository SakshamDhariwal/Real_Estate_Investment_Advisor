def investment_rating(roi):

    if roi >= 35:
        return "🟢 Strong Buy"

    elif roi >= 20:
        return "🟢 Buy"

    elif roi >= 10:
        return "🟡 Hold"

    elif roi >= 0:
        return "🟠 Cautious"

    else:
        return "🔴 Avoid"