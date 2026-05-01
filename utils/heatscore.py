def location_heat_score(schools, hospitals, transport):

    score = (
        schools * 3 +
        hospitals * 3 +
        transport * 4
    )

    return min(score, 100)