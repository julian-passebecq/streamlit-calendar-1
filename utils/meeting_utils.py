import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, is_night=False):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_hour = random.randint(20, 23) if meeting_type == "Security" else random.randint(22, 23)
    else:
        meeting_type = random.choice(["Maintenance", "FireTest", "Security"])
        start_hour = random.randint(8, 19)
    
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

def generate_meetings(start_date, num_clients=5):
    events = []
    for client in range(1, num_clients + 1):
        for day in range(7):
            current_date = start_date + datetime.timedelta(days=day)
            for _ in range(random.randint(2, 3)):
                events.append(generate_meeting(current_date, client, is_night=False))
            if random.choice([True, False]):
                events.append(generate_meeting(current_date, client, is_night=True))
    return events