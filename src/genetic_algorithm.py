import random
from deap import base, creator, tools, algorithms
import numpy as np
from datetime import datetime, timedelta

# Define global constants
SHIFT_DURATION = 8  # hours
BREAK_DURATION = 1  # hour
MIN_REST_BETWEEN_SHIFTS = 8  # hours
TRANSPORT_TIME_MIN = 0.5  # hours
TRANSPORT_TIME_MAX = 1  # hour

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def initialize_individual(agents, missions):
    return creator.Individual([random.choice(agents.index) if random.random() > 0.2 else -1 for _ in range(len(missions))])

def evaluate(individual, agents, missions):
    schedule = {agent: [] for agent in agents.index}
    score = 0
    
    for i, agent_id in enumerate(individual):
        if agent_id == -1:  # Unassigned mission
            score -= 10
            continue
        
        mission = missions.iloc[i]
        agent = agents.iloc[agent_id]
        
        # Check if agent has required skill
        if mission['Required Skill'] != 'None' and not agent[mission['Required Skill']]:
            score -= 5
        else:
            score += 1
        
        # Check for overlapping missions
        mission_start = datetime.combine(datetime.today(), mission['Start Time'])
        mission_end = mission_start + timedelta(hours=mission['Duration'])
        
        for other_mission in schedule[agent_id]:
            other_start = datetime.combine(datetime.today(), other_mission['Start Time'])
            other_end = other_start + timedelta(hours=other_mission['Duration'])
            
            if (mission_start < other_end and mission_end > other_start) or \
               (other_start < mission_end and other_end > mission_start):
                score -= 20
                break
        else:
            schedule[agent_id].append(mission)
            score += 2
    
    # Check for minimum rest between shifts
    for agent_schedule in schedule.values():
        sorted_schedule = sorted(agent_schedule, key=lambda x: x['Start Time'])
        for i in range(len(sorted_schedule) - 1):
            current_end = datetime.combine(datetime.today(), sorted_schedule[i]['Start Time']) + timedelta(hours=sorted_schedule[i]['Duration'])
            next_start = datetime.combine(datetime.today(), sorted_schedule[i+1]['Start Time'])
            if (next_start - current_end).total_seconds() / 3600 < MIN_REST_BETWEEN_SHIFTS:
                score -= 15
    
    return (score,)

def mutate(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.randint(-1, len(agents) - 1)
    return individual,

def generate_schedule(agents, missions, population_size, generations, mutation_rate, crossover_rate):
    toolbox = base.Toolbox()
    toolbox.register("individual", initialize_individual, agents, missions)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, agents=agents, missions=missions)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate, indpb=mutation_rate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)
    
    algorithms.eaSimple(population, toolbox, cxpb=crossover_rate, mutpb=mutation_rate, 
                        ngen=generations, stats=None, halloffame=None, verbose=False)
    
    best_individual = tools.selBest(population, k=1)[0]
    return best_individual

def decode_schedule(individual, agents, missions):
    schedule = {agent: [] for agent in agents.index}
    for i, agent_id in enumerate(individual):
        if agent_id != -1:
            schedule[agent_id].append(missions.iloc[i])
    return schedule

# This function will be called from the schedule generation page
def generate_and_optimize_schedule(agents, missions, population_size, generations, mutation_rate, crossover_rate):
    best_individual = generate_schedule(agents, missions, population_size, generations, mutation_rate, crossover_rate)
    optimized_schedule = decode_schedule(best_individual, agents, missions)
    return optimized_schedule