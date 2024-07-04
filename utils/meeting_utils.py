import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, is_night=False, day_shift_1_start, day_shift_1_end,
                     day_shift_2_start, day_shift_2_end, night_shift_start, night_shift_end, meeting_types):
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

def generate_meetings(start_date, num_clients, total_hours,
                      day_shift_1_start, day_shift_1_end,
                      day_shift_2_start, day_shift_2_end,
                      night_shift_start, night_shift_end,
                      meeting_types):
    events = []
    hours_per_day = total_hours / 5  # Distribute over 5 workdays
    for day in range(5):  # Monday to Friday
        current_date = start_date + datetime.timedelta(days=day)
        daily_hours = 0
        while daily_hours < hours_per_day:
            client = random.randint(1, num_clients)
            is_night = random.choice([True, False]) if daily_hours >= hours_per_day * 0.8 else False
            meeting = generate_meeting(current_date, client, is_night,
                                       day_shift_1_start, day_shift_1_end,
                                       day_shift_2_start, day_shift_2_end,
                                       night_shift_start, night_shift_end,
                                       meeting_types)
            meeting_duration = meeting_types[meeting['type']]['duration']
            if daily_hours + meeting_duration <= hours_per_day:
                events.append(meeting)
                daily_hours += meeting_duration
            else:
                break
    
    # Add night shift for Saturday
    saturday = start_date + datetime.timedelta(days=5)
    for _ in range(int(hours_per_day / 4)):  # Approximately 1/4 of daily meetings for night shift
        client = random.randint(1, num_clients)
        meeting = generate_meeting(saturday, client, True,
                                   day_shift_1_start, day_shift_1_end,
                                   day_shift_2_start, day_shift_2_end,
                                   night_shift_start, night_shift_end,
                                   meeting_types)
        events.append(meeting)
    
    return events