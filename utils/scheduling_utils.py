import random
from typing import List, Dict, Callable
import datetime

class Agent:
    def __init__(self, id: int, name: str, skills: List[str]):
        self.id = id
        self.name = name
        self.skills = skills

class Schedule:
    def __init__(self, agents: List[Agent], meetings: List[Dict]):
        self.agents = agents
        self.meetings = meetings
        self.assignments = {}  # {meeting: agent}
        self.fitness = 0

def initialize_population(pop_size: int, agents: List[Agent], meetings: List[Dict]) -> List[Schedule]:
    population = []
    for _ in range(pop_size):
        schedule = Schedule(agents, meetings)
        for meeting in meetings:
            eligible_agents = [agent for agent in agents if meeting['type'] in agent.skills or meeting['type'] == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)
        population.append(schedule)
    return population

def fitness(schedule: Schedule) -> float:
    score = 0
    agent_schedules = {agent: [] for agent in schedule.agents}

    for meeting, agent in schedule.assignments.items():
        if meeting['type'] not in agent.skills and meeting['type'] != 'Monitoring':
            score -= 100

        meeting_start = datetime.datetime.fromisoformat(meeting['start'])
        meeting_end = datetime.datetime.fromisoformat(meeting['end'])
        
        for existing_meeting in agent_schedules[agent]:
            existing_start = datetime.datetime.fromisoformat(existing_meeting['start'])
            existing_end = datetime.datetime.fromisoformat(existing_meeting['end'])
            
            if (meeting_start < existing_end and meeting_end > existing_start):
                score -= 500  # Overlap penalty
            elif abs((meeting_start - existing_end).total_seconds()) < 1800:  # Less than 30 minutes between meetings
                score -= 50

        agent_schedules[agent].append(meeting)

    for agent, meetings in agent_schedules.items():
        if len(meetings) > 0:
            meetings.sort(key=lambda x: datetime.datetime.fromisoformat(x['start']))
            first_meeting = datetime.datetime.fromisoformat(meetings[0]['start'])
            last_meeting = datetime.datetime.fromisoformat(meetings[-1]['end'])
            shift_duration = (last_meeting - first_meeting).total_seconds() / 3600  # in hours
            
            if shift_duration > 8:
                score -= (shift_duration - 8) * 10  # Penalty for shifts longer than 8 hours

    return score

def crossover(parent1: Schedule, parent2: Schedule) -> Schedule:
    child = Schedule(parent1.agents, parent1.meetings)
    for meeting in child.meetings:
        if random.random() < 0.5:
            child.assignments[meeting] = parent1.assignments.get(meeting)
        else:
            child.assignments[meeting] = parent2.assignments.get(meeting)
    return child

def mutate(schedule: Schedule, mutation_rate: float):
    for meeting in schedule.meetings:
        if random.random() < mutation_rate:
            eligible_agents = [agent for agent in schedule.agents if meeting['type'] in agent.skills or meeting['type'] == 'Monitoring']
            if eligible_agents:
                schedule.assignments[meeting] = random.choice(eligible_agents)

def genetic_algorithm(agents: List[Agent], meetings: List[Dict], pop_size: int, generations: int, mutation_rate: float, progress_callback: Callable[[int, float], None] = None) -> Schedule:
    population = initialize_population(pop_size, agents, meetings)

    for generation in range(generations):
        for schedule in population:
            schedule.fitness = fitness(schedule)
        
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
        best_fitness = population[0].fitness

        if progress_callback:
            progress_callback(generation + 1, best_fitness)

        new_population = population[:2]  # Keep the two best schedules

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:pop_size // 2], 2)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    return max(population, key=lambda x: x.fitness)