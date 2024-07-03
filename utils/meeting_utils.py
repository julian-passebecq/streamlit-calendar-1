import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, is_night, shift_duration, night_start_time):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_hour = random.randint(night_start_time, 23)
    else:
        meeting_type = random.choice(["Maintenance", "FireTest", "Security"])
        start_hour = random.randint(8, 19)

    start_time = datetime.time(hour=start_hour)
    duration = datetime.timedelta(hours=shift_duration)
    end_time = (datetime.datetime.combine(date, start_time) + duration).time()
    
    return {
        "title": f"Client {client}: {meeting_type}" + (" (Night)" if is_night else ""),
        "start": f"{date}T{start_time}",
        "end": f"{date}T{end_time}",
        "backgroundColor": meeting_types[meeting_type]["color"],
        "borderColor": meeting_types[meeting_type]["color"],
        "client": f"Client {client}",
        "type": meeting_type,
        "is_night": is_night
    }

def generate_meetings(start_date, num_clients, date_range, num_night_shifts, num_day_shifts, shift_duration, night_start_time):
    events = []
    for day in range(date_range):
        current_date = start_date + datetime.timedelta(days=day)
        for client in range(1, num_clients + 1):
            for _ in range(num_day_shifts):
                events.append(generate_meeting(current_date, client, is_night=False, shift_duration=shift_duration, night_start_time=night_start_time))
            for _ in range(num_night_shifts):
                events.append(generate_meeting(current_date, client, is_night=True, shift_duration=shift_duration, night_start_time=night_start_time))
    return events
