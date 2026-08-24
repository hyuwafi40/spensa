def calculate_grade(daily_score, midterm_score, final_score):
    try:
        daily = float(daily_score or 0)
        mid = float(midterm_score or 0)
        final = float(final_score or 0)
    except (TypeError, ValueError):
        return None, ""
    total = daily * 0.4 + mid * 0.3 + final * 0.3
    total = round(total, 2)
    if total >= 90:
        letter = "A"
    elif total >= 80:
        letter = "B"
    elif total >= 70:
        letter = "C"
    elif total >= 60:
        letter = "D"
    else:
        letter = "E"
    return total, letter
