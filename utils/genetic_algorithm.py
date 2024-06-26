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
    # Implementation here

def fitness(schedule: Schedule) -> float:
    # Implementation here

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    # Implementation here

def mutate(schedule: Schedule, mutation_rate: float):
    # Implementation here

def genetic_algorithm(agents: List[Agent], meetings: List[Meeting], pop_size: int, generations: int, mutation_rate: float) -> Schedule:
    # Implementation here