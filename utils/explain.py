def explain_prediction(price_per_bhk, transport, schools, age):

    reasons = []

    if price_per_bhk < 30:
        reasons.append("Attractive price per BHK")

    if transport >= 7:
        reasons.append("Strong transport connectivity")

    if schools >= 7:
        reasons.append("Good educational access")

    if age <= 10:
        reasons.append("Relatively newer property")

    if not reasons:
        reasons.append("Mixed fundamentals detected")

    return reasons