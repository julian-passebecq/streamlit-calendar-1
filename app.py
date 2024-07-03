import streamlit as st
from streamlit_calendar import calendar
import datetime
import random
import pandas as pd
from typing import List, Dict, Tuple

st.set_page_config(page_title="Scheduling App", layout="wide")

# Define meeting types and their properties
meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

# Calendar page functions
def generate_meeting(date, client, is_night=False):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_hour = random.randint(20, 23) if meeting_type == "Security" else random.randint(22, 23)
    else:
        meeting_type = random.choice(list(meeting_types.keys()))
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
    for day in range(7):
        current_date = start_date + datetime.timedelta(days=day)
        daily_hours = 0
        while daily_hours < 40:  # 5 agents * 8 hours
            client = random.randint(1, num_clients)
            is_night = random.choice(
                [True, False]) if daily_hours >= 32 else False  # Allow night meetings only in the last 8 hours
            meeting = generate_meeting(current_date, client, is_night)
            meeting_duration = meeting_types[meeting['type']]['duration']
            if daily_hours + meeting_duration <= 40:
                events.append(meeting)
                daily_hours += meeting_duration
            else:
                break
    return events

def show_calendar_page():
    st.title("Calendar View")

    if 'calendar_events' not in st.session_state:
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week)

    all_clients = sorted(set(event['client'] for event in st.session_state.calendar_events))
    all_types = sorted(list(meeting_types.keys()))

    col1, col2 = st.columns(2)
    with col1:
        selected_clients = st.multiselect("Select Clients", all_clients, default=all_clients)
    with col2:
        selected_types = st.multiselect("Select Appointment Types", all_types, default=all_types)

    filtered_events = [
        event for event in st.session_state.calendar_events
        if event['client'] in selected_clients and event['type'] in selected_types
    ]

    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "initialView": "timeGridWeek",
        "slotMinTime": "06:00:00",
        "slotMaxTime": "30:00:00",  # 6:00 AM next day
        "expandRows": True,
        "height": "650px",
        "dayMaxEvents": True,
        "allDaySlot": False,
        "scrollTime": "08:00:00",  # Start scrolled to 8:00 AM
        "nowIndicator": True,
    }

    custom_css = """
        .fc-event-past { opacity: 0.8; }
        .fc-event-time { font-weight: bold; }
        .fc-event-title { font-style: italic; }
    """

    cal = calendar(events=filtered_events, options=calendar_options, custom_css=custom_css)
    st.write(cal)

    st.subheader("Meeting Types and Durations")
    for meeting_type, info in meeting_types.items():
        st.markdown(
            f'<span style="color:{info["color"]}">■</span> {meeting_type} ({info["duration"]} hour{"s" if info["duration"] > 1 else ""})',
            unsafe_allow_html=True)

    if isinstance(cal, dict) and 'eventClick' in cal:
        event = cal['eventClick']['event']
        st.subheader("Selected Event")
        st.write(f"Title: {event['title']}")
        st.write(f"Start: {event['start']}")
        st.write(f"End: {event['end']}")

    # Summary Table
    st.subheader("Summary Table")

    summary_data = []
    start_date = min(datetime.datetime.fromisoformat(event['start']).date() for event in filtered_events)

    for day in range(7):
        current_date = start_date + datetime.timedelta(days=day)
        day_events = [event for event in filtered_events if
                      datetime.datetime.fromisoformat(event['start']).date() == current_date]

        total_hours = sum(meeting_types[event['type']]['duration'] for event in day_events)
        required_agents = len(day_events)
        night_appointments = sum(
            1 for event in day_events if event['is_night'] or int(event['start'].split('T')[1].split(':')[0]) >= 20)
        day_appointments = required_agents - night_appointments

        summary_data.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Total Hours": total_hours,
            "Required Agents": required_agents,
            "Day Appointments (6AM-8PM)": day_appointments,
            "Night Appointments (After 8PM)": night_appointments
        })

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

    if st.button("Generate New Events"):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week)
        st.experimental_rerun()

# Genetic Algorithm classes and functions
class Agent:
    def __init__(self, id: int, skills: List[str]):
        self.id = id
        self.skills = skills

class Meeting:
    def __init__(self, start_slot: int, duration: int, required_skill: str):
        self.start_slot = start_slot
        self.duration = duration
        self.required_skill = required_skill

class Schedule:
    def __init__(self, agents: List[Agent], meetings: List[Meeting]):
        self.agents = agents
        self.meetings = meetings
        self.assignments = {}  # {meeting: agent}

def initialize_population(pop_size: int, agents: List[Agent], meetings: List[Meeting]) -> List[Schedule]:
    population = []
    for _ in range(pop_size):
        schedule = Schedule(agents, meetings)
        for meeting in meetings:
            eligible_agents = [agent for agent in agents if meeting.required_skill in agent.skills or meeting.required_skill == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)
        population.append(schedule)
    return population

def fitness(schedule: Schedule) -> float:
    score = 0
    agent_schedules = {agent: [0] * (24 * 2) for agent in schedule.agents}  # 48 30-minute slots

    for meeting, agent in schedule.assignments.items():
        if meeting.required_skill not in agent.skills and meeting.required_skill != 'Monitoring':
            score -= 100

        for slot in range(meeting.start_slot, meeting.start_slot + meeting.duration):
            if agent_schedules[agent][slot] == 1:
                score -= 50
            agent_schedules[agent][slot] = 1

        if meeting.start_slot > 0 and agent_schedules[agent][meeting.start_slot - 1] == 1:
            score -= 25

    for agent, schedule in agent_schedules.items():
        work_slots = sum(schedule)
        if work_slots > 16:  # 8 hours
            score -= (work_slots - 16) * 10

        work_periods = [sum(schedule[i:i + 6]) for i in range(0, len(schedule), 6)]
        if max(work_periods) > 3:  # More than 3 hours without a break
            score -= 50

    return score

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    child1, child2 = Schedule(parent1.agents, parent1.meetings), Schedule(parent2.agents, parent2.meetings)
    crossover_point = random.randint(0, len(parent1.meetings))

    child1.assignments = {**dict(list(parent1.assignments.items())[:crossover_point]),
                          **dict(list(parent2.assignments.items())[crossover_point:])}
    child2.assignments = {**dict(list(parent2.assignments.items())[:crossover_point]),
                          **dict(list(parent1.assignments.items())[crossover_point:])}

    return child1, child2

def mutate(schedule: Schedule, mutation_rate: float):
    for meeting in schedule.meetings:
        if random.random() < mutation_rate:
            eligible_agents = [agent for agent in schedule.agents if meeting.required_skill in agent.skills or meeting.required_skill == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)

def genetic_algorithm(agents: List[Agent], meetings: List[Meeting], pop_size: int, generations: int, mutation_rate: float) -> Schedule:
    population = initialize_population(pop_size, agents, meetings)

    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        new_population = population[:2]  # Keep the two best schedules

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:pop_size // 2], 2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=lambda x: fitness(x))

def show_genetic_algorithm_page():
    st.title("Genetic Algorithm Scheduling")

    # Predefined agents with fixed skills
    agents = [
        Agent(0, ["Fire", "Maintenance"]),
        Agent(1, ["Security"]),
        Agent(2, ["Fire"]),
        Agent(3, ["Security", "Maintenance"]),
        Agent(4, ["Security", "Fire"])
    ]

    st.subheader("Agent Skills")
    for agent in agents:
        st.write(f"Agent {agent.id}: {', '.join(agent.skills)}")

    # Input for meetings
    st.subheader("Meetings")
    num_meetings = st.number_input("Number of Meetings", min_value=1, max_value=50, value=20)
    meetings = []
    for i in range(num_meetings):
        col1, col2, col3 = st.columns(3)
        with col1:
            start_slot = st.number_input(f"Meeting {i + 1} Start Slot", min_value=0, max_value=47, value=0,
                                         key=f"start_{i}")
        with col2:
            duration = st.number_input(f"Meeting {i + 1} Duration", min_value=1, max_value=4, value=1,
                                       key=f"duration_{i}")
        with col3:
            required_skill = st.selectbox(f"Meeting {i + 1} Required Skill",
                                          ["Fire", "Security", "Maintenance", "Monitoring"], key=f"skill_{i}")
        meetings.append(Meeting(start_slot, duration, required_skill))

    # Run genetic algorithm
    if st.button("Run Genetic Algorithm"):
        best_schedule = genetic_algorithm(agents, meetings, pop_size=50, generations=100, mutation_rate=0.1)
        st.session_state.best_schedule = best_schedule
        st.success("Genetic algorithm completed. View results in the Results page.")

def show_results_page():
    st.title("Scheduling Results")

    if 'best_schedule' not in st.session_state:
        st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
        return

    best_schedule = st.session_state.best_schedule

    st.subheader("Best Schedule")
    st.write(f"Fitness Score: {fitness(best_schedule)}")

    for meeting, agent in best_schedule.assignments.items():
        st.write(
            f"Meeting (Slot {meeting.start_slot}, Duration {meeting.duration}, Skill {meeting.required_skill}) assigned to Agent {agent.id}")

    # Here you can add more visualizations of the schedule, such as a calendar view or Gantt chart

# Main app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Calendar", "Genetic Algorithm", "Results"])

    if page == "Calendar":
        show_calendar_page()
    elif page == "Genetic Algorithm":
        show_genetic_algorithm_page()
    elif page == "Results":
        show_results_page()

if __name__ == "__main__":
    main()
