import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, start_hour, end_hour, meeting_type=None):
    if meeting_type is None:
        meeting_type = random.choice(list(meeting_types.keys()))
    
    start_time = datetime.time(hour=random.randint(start_hour, end_hour - meeting_types[meeting_type]["duration"]))
    duration = datetime.timedelta(hours=meeting_types[meeting_type]["duration"])
    end_time = (datetime.datetime.combine(date, start_time) + duration).time()
    
    return {
        "title": f"Client {client}: {meeting_type}",
        "start": f"{date}T{start_time}",
        "end": f"{date}T{end_time}",
        "backgroundColor": meeting_types[meeting_type]["color"],
        "borderColor": meeting_types[meeting_type]["color"],
        "client": f"Client {client}",
        "type": meeting_type
    }

def generate_meetings(start_date, num_days, num_clients, meetings_per_day, night_shift_ratio, day_start_hour, day_end_hour, night_start_hour, night_end_hour):
    events = []
    for day in range(num_days):
        current_date = start_date + datetime.timedelta(days=day)
        for _ in range(meetings_per_day):
            client = random.randint(1, num_clients)
            is_night = random.random() < night_shift_ratio
            if is_night:
                meeting = generate_meeting(current_date, client, night_start_hour, night_end_hour, meeting_type=random.choice(["Security", "Monitoring"]))
            else:
                meeting = generate_meeting(current_date, client, day_start_hour, day_end_hour)
            events.append(meeting)
    return events