def property_alerts(price, sqft, age, roi):

    alerts = []

    if price > 200:
        alerts.append("High ticket property.")

    if sqft < 500:
        alerts.append("Compact area size.")

    if age > 20:
        alerts.append("Older property; maintenance risk.")

    if roi < 10:
        alerts.append("Weak return potential.")

    return alerts