import random
import datetime

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, day_shift_1_start, day_shift_1_end,
                     day_shift_2_start, day_shift_2_end, night_shift_start, night_shift_end,
                     meeting_types):
    is_night = random.random() < 0.2  # 20% chance of night shift
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_hour = random.randint(night_shift_start.hour, 23)
    else:
        meeting_type = random.choice(list(meeting_types.keys()))
        if random.choice([True, False]):
            start_hour = random.randint(day_shift_1_start.hour, day_shift_1_end.hour - 1)
        else:
            start_hour = random.randint(day_shift_2_start.hour, day_shift_2_end.hour - 1)
    
    start_time = datetime.time(hour=start_hour, minute=random.choice([0, 30]))
    duration = meeting_types[meeting_type]["duration"]
    start_datetime = datetime.datetime.combine(date, start_time)
    end_datetime = start_datetime + datetime.timedelta(hours=duration)
    
    return {
        "title": f"Client {client}: {meeting_type}" + (" (Night)" if is_night else ""),
        "start": start_datetime.isoformat(),
        "end": end_datetime.isoformat(),
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
    current_year = datetime.datetime.now().year
    start_date = start_date.replace(year=current_year)
    hours_per_day = total_hours / 6  # Distribute over 6 days (Monday to Saturday)
    print(f"Generating meetings for {total_hours} total hours, {hours_per_day} hours per day")
    for day in range(6):  # Monday to Saturday
        current_date = start_date + datetime.timedelta(days=day)
        daily_hours = 0
        daily_meetings = 0
        while daily_hours < hours_per_day:
            client = random.randint(1, num_clients)
            meeting = generate_meeting(current_date, client, day_shift_1_start, day_shift_1_end,
                                       day_shift_2_start, day_shift_2_end, night_shift_start, night_shift_end,
                                       meeting_types)
            meeting_duration = meeting_types[meeting['type']]['duration']
            if daily_hours + meeting_duration <= hours_per_day:
                events.append(meeting)
                daily_hours += meeting_duration
                daily_meetings += 1
            else:
                break
        print(f"Day {day + 1}: Generated {daily_meetings} meetings, total {daily_hours} hours")
    
    # Add night shift for Sunday
    sunday = start_date + datetime.timedelta(days=6)
    sunday_meetings = 0
    for _ in range(int(hours_per_day / 4)):  # Approximately 1/4 of daily meetings for night shift
        client = random.randint(1, num_clients)
        meeting = generate_meeting(sunday, client, day_shift_1_start, day_shift_1_end,
                                   day_shift_2_start, day_shift_2_end, night_shift_start, night_shift_end,
                                   meeting_types)
        meeting['is_night'] = True  # Force Sunday meetings to be night shifts
        events.append(meeting)
        sunday_meetings += 1
    print(f"Sunday: Generated {sunday_meetings} night meetings")
    
    print(f"Total meetings generated: {len(events)}")
    return events