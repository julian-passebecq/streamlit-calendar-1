import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_calendar import calendar
import datetime
import random
from utils.meeting_utils import generate_meetings, meeting_types
from utils.genetic_algorithm import Agent, Meeting, Schedule, genetic_algorithm, fitness

st.set_page_config(page_title="Security Firm Scheduling App", layout="wide")

# Sidebar for global settings
st.sidebar.title("Global Settings")
num_agents = st.sidebar.number_input("Number of Agents", min_value=1, max_value=10, value=5)
num_clients = st.sidebar.number_input("Number of Clients", min_value=1, max_value=20, value=5)

# Function to generate agents based on user input
def generate_agents(num_agents):
    skills = ["Fire", "Security", "Maintenance"]
    agents = []
    for i in range(num_agents):
        agent_skills = st.sidebar.multiselect(f"Skills for Agent {i+1}", skills, default=random.sample(skills, 1))
        agents.append(Agent(i, agent_skills))
    return agents

# Generate agents
agents = generate_agents(num_agents)

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

def show_calendar_page():
    st.title("Calendar View")

    # Calendar settings
    col1, col2 = st.columns(2)
    with col1:
        day_shift_1_start = st.time_input("Day Shift 1 Start", datetime.time(7, 0))
        day_shift_1_end = st.time_input("Day Shift 1 End", datetime.time(16, 0))
    with col2:
        day_shift_2_start = st.time_input("Day Shift 2 Start", datetime.time(13, 0))
        day_shift_2_end = st.time_input("Day Shift 2 End", datetime.time(22, 0))

    night_shift_start = st.time_input("Night Shift Start", datetime.time(22, 0))
    night_shift_end = st.time_input("Night Shift End", datetime.time(7, 0))

    meetings_per_day = st.slider("Meetings per day", 1, 10, 5)

    if 'calendar_events' not in st.session_state:
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week, num_clients, meetings_per_day,
                                                             day_shift_1_start, day_shift_1_end,
                                                             day_shift_2_start, day_shift_2_end,
                                                             night_shift_start, night_shift_end)

    all_clients = sorted(set(event['client'] for event in st.session_state.calendar_events))
    all_types = sorted(list(meeting_types.keys()))

    selected_clients = st.multiselect("Select Clients", all_clients, default=all_clients)
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
            "Day Appointments": day_appointments,
            "Night Appointments": night_appointments
        })

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

    if st.button("Generate New Events"):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week, num_clients, meetings_per_day,
                                                             day_shift_1_start, day_shift_1_end,
                                                             day_shift_2_start, day_shift_2_end,
                                                             night_shift_start, night_shift_end)
        st.experimental_rerun()

def show_genetic_algorithm_page():
    st.title("Genetic Algorithm Scheduling")

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

    # Genetic Algorithm Parameters
    st.subheader("Genetic Algorithm Parameters")
    pop_size = st.number_input("Population Size", min_value=10, max_value=1000, value=50)
    generations = st.number_input("Number of Generations", min_value=10, max_value=1000, value=100)
    mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

    # Run genetic algorithm
    if st.button("Run Genetic Algorithm"):
        progress_bar = st.progress(0)
        best_fitness_history = []
        avg_fitness_history = []

        for i in range(generations):
            best_schedule = genetic_algorithm(agents, meetings, pop_size, 1, mutation_rate)
            best_fitness = fitness(best_schedule)
            avg_fitness = sum(fitness(schedule) for schedule in [best_schedule]) / 1

            best_fitness_history.append(best_fitness)
            avg_fitness_history.append(avg_fitness)

            progress_bar.progress((i + 1) / generations)

        st.session_state.best_schedule = best_schedule
        st.session_state.best_fitness_history = best_fitness_history
        st.session_state.avg_fitness_history = avg_fitness_history

        st.success("Genetic algorithm completed. View results in the Results page.")

def show_results_page():
    st.title("Scheduling Results")

    if 'best_schedule' not in st.session_state:
        st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
        return

    best_schedule = st.session_state.best_schedule
    best_fitness_history = st.session_state.best_fitness_history
    avg_fitness_history = st.session_state.avg_fitness_history

    st.subheader("Best Schedule")
    st.write(f"Fitness Score: {fitness(best_schedule)}")

    for meeting, agent in best_schedule.assignments.items():
        st.write(
            f"Meeting (Slot {meeting.start_slot}, Duration {meeting.duration}, Skill {meeting.required_skill}) assigned to Agent {agent.id}")

    # Fitness History Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=best_fitness_history, mode='lines', name='Best Fitness'))
    fig.add_trace(go.Scatter(y=avg_fitness_history, mode='lines', name='Average Fitness'))
    fig.update_layout(title='Fitness History', xaxis_title='Generation', yaxis_title='Fitness Score')
    st.plotly_chart(fig)

    # Agent Workload
    agent_workload = {agent.id: 0 for agent in best_schedule.agents}
    for meeting, agent in best_schedule.assignments.items():
        agent_workload[agent.id] += meeting.duration

    fig = go.Figure(data=[go.Bar(x=list(agent_workload.keys()), y=list(agent_workload.values()))])
    fig.update_layout(title='Agent Workload', xaxis_title='Agent ID', yaxis_title='Total Hours')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()