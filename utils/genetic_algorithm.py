import random
from typing import List, Dict, Tuple
import datetime

class Agent:
    def __init__(self, id: int, skills: List[str]):
        self.id = id
        self.skills = skills

class Meeting:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, required_skill: str):
        self.start = start
        self.end = end
        self.required_skill = required_skill

    @property
    def duration(self):
        return (self.end - self.start).total_seconds() / 3600

class Schedule:
    def __init__(self, agents: List[Agent], meetings: List[Meeting]):
        self.agents = agents
        self.meetings = meetings
        self.assignments: Dict[Meeting, Agent] = {}

def initialize_population(pop_size: int, agents: List[Agent], meetings: List[Meeting]) -> List[Schedule]:
    population = []
    for _ in range(pop_size):
        schedule = Schedule(agents, meetings)
        for meeting in meetings:
            eligible_agents = [agent for agent in agents if
                               meeting.required_skill in agent.skills or meeting.required_skill == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)
        population.append(schedule)
    return population

def fitness(schedule: Schedule, penalty_wrong_skill: int, penalty_overlap: int, penalty_consecutive: int,
            penalty_overwork: int, penalty_long_shift: int) -> float:
    score = 0
    agent_schedules = {agent: [] for agent in schedule.agents}

    for meeting, agent in schedule.assignments.items():
        if meeting.required_skill not in agent.skills and meeting.required_skill != 'Monitoring':
            score -= penalty_wrong_skill

        agent_schedules[agent].append(meeting)

    for agent, meetings in agent_schedules.items():
        meetings.sort(key=lambda m: m.start)
        for i in range(len(meetings)):
            if i > 0:
                time_between = (meetings[i].start - meetings[i-1].end).total_seconds() / 3600
                if time_between < 0.5:  # Less than 30 minutes between meetings
                    score -= penalty_consecutive
                elif time_between < 0:  # Overlapping meetings
                    score -= penalty_overlap

        work_hours = sum(meeting.duration for meeting in meetings)
        if work_hours > 8:
            score -= (work_hours - 8) * penalty_overwork

        # Check for long shifts (more than 3 hours without a break)
        current_shift = datetime.timedelta()
        last_end_time = None
        for meeting in meetings:
            if last_end_time and (meeting.start - last_end_time).total_seconds() / 3600 >= 1:
                current_shift = datetime.timedelta()
            current_shift += meeting.end - meeting.start
            if current_shift.total_seconds() / 3600 > 3:
                score -= penalty_long_shift
                current_shift = datetime.timedelta()
            last_end_time = meeting.end

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
            eligible_agents = [agent for agent in schedule.agents if
                               meeting.required_skill in agent.skills or meeting.required_skill == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)

def genetic_algorithm(agents: List[Agent], meetings: List[Meeting], pop_size: int, generations: int,
                      mutation_rate: float, penalty_wrong_skill: int, penalty_overlap: int, penalty_consecutive: int,
                      penalty_overwork: int, penalty_long_shift: int) -> Schedule:
    population = initialize_population(pop_size, agents, meetings)

    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, penalty_wrong_skill, penalty_overlap,
                                                              penalty_consecutive, penalty_overwork,
                                                              penalty_long_shift), reverse=True)
        new_population = population[:2]  # Keep the two best schedules

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:pop_size // 2], 2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=lambda x: fitness(x, penalty_wrong_skill, penalty_overlap,
                                                 penalty_consecutive, penalty_overwork, penalty_long_shift))