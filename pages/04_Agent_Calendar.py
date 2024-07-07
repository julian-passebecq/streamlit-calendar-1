import streamlit as st
import plotly.graph_objects as go
from utils.genetic_algorithm import Agent, Meeting
from streamlit_calendar import calendar
import datetime

st.title("Agent Calendars")

if 'best_schedule' not in st.session_state:
    st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
    st.stop()

best_schedule = st.session_state.best_schedule

# Sidebar for agent selection
st.sidebar.title("Agent Selection")
selected_agent_id = st.sidebar.selectbox("Select Agent", options=[agent.id for agent in best_schedule.agents])

# Get the selected agent's schedule
selected_agent = next(agent for agent in best_schedule.agents if agent.id == selected_agent_id)
agent_meetings = [meeting for meeting, agent in best_schedule.assignments.items() if agent.id == selected_agent_id]

# Create calendar events for the agent
start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
events = []
for meeting in agent_meetings:
    day = meeting.start_slot // (24 * 2)  # 48 slots per day
    slot_in_day = meeting.start_slot % (24 * 2)
    start_time = datetime.time(hour=slot_in_day // 2, minute=(slot_in_day % 2) * 30)
    end_time = (datetime.datetime.combine(datetime.date.min, start_time) + datetime.timedelta(minutes=30 * meeting.duration)).time()
    event_date = start_date + datetime.timedelta(days=day)
    events.append({
        "title": meeting.required_skill,
        "start": f"{event_date}T{start_time}",
        "end": f"{event_date}T{end_time}",
        "backgroundColor": "#FF9999",  # You can assign colors based on skill if desired
        "borderColor": "#FF9999",
    })

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

st.subheader(f"Calendar for Agent {selected_agent_id}")
cal = calendar(events=events, options=calendar_options, custom_css=custom_css)
st.write(cal)

# Display agent details
st.subheader(f"Agent {selected_agent_id} Details")
st.write(f"Skills: {', '.join(selected_agent.skills)}")
st.write(f"Total meetings: {len(agent_meetings)}")

# Display meeting details
st.subheader("Meeting Details")
for meeting in agent_meetings:
    day = meeting.start_slot // (24 * 2)
    slot_in_day = meeting.start_slot % (24 * 2)
    start_time = f"{slot_in_day // 2:02d}:{(slot_in_day % 2) * 30:02d}"
    st.write(f"Day: {day+1}, Start Time: {start_time}, Duration: {meeting.duration * 30} minutes, Skill: {meeting.required_skill}")

# Workload distribution
workload = [0] * 7  # 7 days
for meeting in agent_meetings:
    day = meeting.start_slot // (24 * 2)
    workload[day] += meeting.duration / 2  # Convert to hours

fig = go.Figure(data=[go.Bar(x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], y=workload)])
fig.update_layout(title='Daily Workload', xaxis_title='Day', yaxis_title='Hours')
st.plotly_chart(fig)