import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state for missions if not exists
if 'missions' not in st.session_state:
    st.session_state.missions = pd.DataFrame(columns=['Client', 'Type', 'Start Time', 'Duration', 'Required Skill'])

def mission_management_page():
    st.header("Mission Management")

    # Add new mission
    with st.form("new_mission"):
        st.subheader("Add New Mission")
        client = st.text_input("Client Name")
        mission_type = st.selectbox("Mission Type", ["Monitoring", "Security", "Fire", "Maintenance"])
        start_time = st.time_input("Start Time")
        duration = st.number_input("Duration (hours)", min_value=1, max_value=8, value=1)
        required_skill = st.selectbox("Required Skill", ["None", "Security", "Fire", "Maintenance"])
        
        if st.form_submit_button("Add Mission"):
            new_mission = pd.DataFrame({
                'Client': [client],
                'Type': [mission_type],
                'Start Time': [start_time],
                'Duration': [duration],
                'Required Skill': [required_skill]
            })
            st.session_state.missions = pd.concat([st.session_state.missions, new_mission], ignore_index=True)
            st.success(f"Mission for {client} added successfully!")

    # Display and edit missions
    st.subheader("Current Missions")
    for i, mission in st.session_state.missions.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3,2,2,1,2,1])
        with col1:
            st.write(mission['Client'])
        with col2:
            mission_type = st.selectbox("Type", ["Monitoring", "Security", "Fire", "Maintenance"], index=["Monitoring", "Security", "Fire", "Maintenance"].index(mission['Type']), key=f"type_{i}")
        with col3:
            start_time = st.time_input("Start", value=mission['Start Time'], key=f"start_{i}")
        with col4:
            duration = st.number_input("Duration", min_value=1, max_value=8, value=mission['Duration'], key=f"duration_{i}")
        with col5:
            required_skill = st.selectbox("Skill", ["None", "Security", "Fire", "Maintenance"], index=["None", "Security", "Fire", "Maintenance"].index(mission['Required Skill']), key=f"skill_{i}")
        with col6:
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.missions = st.session_state.missions.drop(i).reset_index(drop=True)
                st.experimental_rerun()
        
        # Update mission information
        st.session_state.missions.at[i, 'Type'] = mission_type
        st.session_state.missions.at[i, 'Start Time'] = start_time
        st.session_state.missions.at[i, 'Duration'] = duration
        st.session_state.missions.at[i, 'Required Skill'] = required_skill

    # Display mission dataframe
    st.subheader("Mission Overview")
    st.dataframe(st.session_state.missions)