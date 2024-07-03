import random
from typing import List, Dict
import pandas as pd

def initialize_population(population_size: int, chromosome_length: int) -> List[List[int]]:
    return [random.choices(range(-1, 5), k=chromosome_length) for _ in range(population_size)]

def fitness(chromosome: List[int], agents: pd.DataFrame, missions: pd.DataFrame) -> float:
    score = 0
    agent_schedules = {i: [] for i in range(len(agents))}

    for i, agent_id in enumerate(chromosome):
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
        for other_mission in agent_schedules[agent_id]:
            if (mission['Start Time'] < other_mission['End Time'] and 
                mission['Start Time'] + mission['Duration'] > other_mission['Start Time']):
                score -= 20
                break
        else:
            agent_schedules[agent_id].append({
                'Start Time': mission['Start Time'],
                'End Time': mission['Start Time'] + mission['Duration']
            })
            score += 2

    return score

def crossover(parent1: List[int], parent2: List[int]) -> tuple:
    split = random.randint(0, len(parent1) - 1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

def mutate(chromosome: List[int], mutation_rate: float, num_agents: int) -> List[int]:
    return [random.randint(-1, num_agents - 1) if random.random() < mutation_rate else gene for gene in chromosome]

def genetic_algorithm(agents: pd.DataFrame, missions: pd.DataFrame, population_size: int, generations: int, mutation_rate: float, crossover_rate: float) -> List[int]:
    population = initialize_population(population_size, len(missions))
    
    for _ in range(generations):
        # Evaluate fitness
        fitness_scores = [fitness(chrom, agents, missions) for chrom in population]
        
        # Select parents
        parents = random.choices(population, weights=fitness_scores, k=len(population))
        
        # Create next generation
        next_generation = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                if random.random() < crossover_rate:
                    child1, child2 = crossover(parents[i], parents[i+1])
                else:
                    child1, child2 = parents[i], parents[i+1]
                next_generation.extend([mutate(child1, mutation_rate, len(agents)),
                                        mutate(child2, mutation_rate, len(agents))])
        
        population = next_generation

    # Return the best solution
    best_solution = max(population, key=lambda chrom: fitness(chrom, agents, missions))
    return best_solution

def generate_schedule(agents: pd.DataFrame, missions: pd.DataFrame, population_size: int, generations: int, mutation_rate: float, crossover_rate: float) -> Dict[int, List[Dict]]:
    best_solution = genetic_algorithm(agents, missions, population_size, generations, mutation_rate, crossover_rate)
    
    schedule = {i: [] for i in range(len(agents))}
    for i, agent_id in enumerate(best_solution):
        if agent_id != -1:
            mission = missions.iloc[i]
            schedule[agent_id].append({
                'Client': mission['Client'],
                'Type': mission['Type'],
                'Start Time': mission['Start Time'],
                'Duration': mission['Duration']
            })
    
    return schedule