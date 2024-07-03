import random
from typing import List, Dict, Tuple

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