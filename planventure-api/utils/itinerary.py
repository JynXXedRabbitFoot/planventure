from datetime import datetime, timedelta

def generate_itinerary_template(start_date: datetime, end_date: datetime) -> dict:
    """Generate a default itinerary template for the trip duration."""
    itinerary = {}
    current_date = start_date
    day_count = 1

    while current_date <= end_date:
        day_key = f"day{day_count}"
        date_str = current_date.strftime("%Y-%m-%d")
        
        itinerary[day_key] = {
            "date": date_str,
            "schedule": {
                "morning": {
                    "time": "09:00",
                    "activity": "Plan your morning activity",
                    "notes": ""
                },
                "afternoon": {
                    "time": "14:00",
                    "activity": "Plan your afternoon activity",
                    "notes": ""
                },
                "evening": {
                    "time": "19:00",
                    "activity": "Plan your evening activity",
                    "notes": ""
                }
            },
            "notes": "",
            "accommodation": ""
        }
        
        current_date += timedelta(days=1)
        day_count += 1

    return itinerary
