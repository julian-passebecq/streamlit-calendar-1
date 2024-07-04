import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, is_night=False, day_shift_1_start=datetime.time(7, 0), day_shift_1_end=datetime.time(16, 0),
                     day_shift_2_start=datetime.time(13, 0), day_shift_2_end=datetime.time(22, 0),
                     night_shift_start=datetime.time(22, 0), night_shift_end=datetime.time(7, 0)):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_hour = random.randint(night_shift_start.hour, 23) if night_shift_start.hour != 0 else random.randint(0, night_shift_end.hour)
    else:
        meeting_type = random.choice(list(meeting_types.keys()))
        if random.choice([True, False]):
            start_hour = random.randint(day_shift_1_start.hour, day_shift_1_end.hour - 1)
        else:
            start_hour = random.randint(day_shift_2_start.hour, day_shift_2_end.hour - 1)
    
    start_time = datetime.time(hour=start_hour)
    duration = datetime.timedelta(hours=meeting_types[meeting_type]["duration"])
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

def generate_meetings(start_date, num_clients=5, meetings_per_day=5,
                      day_shift_1_start=datetime.time(7, 0), day_shift_1_end=datetime.time(16, 0),
                      day_shift_2_start=datetime.time(13, 0), day_shift_2_end=datetime.time(22, 0),
                      night_shift_start=datetime.time(22, 0), night_shift_end=datetime.time(7, 0)):
    events = []
    for day in range(7):
        current_date = start_date + datetime.timedelta(days=day)
        for _ in range(meetings_per_day):
            client = random.randint(1, num_clients)
            is_night = random.choice([True, False])
            events.append(generate_meeting(current_date, client, is_night,
                                           day_shift_1_start, day_shift_1_end,
                                           day_shift_2_start, day_shift_2_end,
                                           night_shift_start, night_shift_end))
    return events