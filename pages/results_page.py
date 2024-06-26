import streamlit as st
from utils.genetic_algorithm import fitness

def show():
    st.title("Scheduling Results")
    
    if 'best_schedule' not in st.session_state:
        st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
        return
    
    best_schedule = st.session_state.best_schedule
    
    st.subheader("Best Schedule")
    st.write(f"Fitness Score: {fitness(best_schedule)}")
    
    for meeting, agent in best_schedule.assignments.items():
        st.write(f"Meeting (Slot {meeting.start_slot}, Duration {meeting.duration}, Skill {meeting.required_skill}) assigned to Agent {agent.id}")
    
    # Here you can add more visualizations of the schedule, such as a calendar view or Gantt chart