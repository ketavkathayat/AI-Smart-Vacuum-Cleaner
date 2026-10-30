
from environment import Environment

from agents.goal_agent import choose_target as goal_agent
from agents.utility_agent import choose_target as utility_agent


env = Environment()

start = env.start

algorithm = "A*"


print("\nAI VACUUM CLEANER - INTELLIGENT AGENTS")

print("Starting Position:", start)

print("Available Dirty Areas:", len(env.dirty_areas))


# Goal Based Agent

print("\n--- GOAL BASED AGENT ---")

target, path, explored, cost = goal_agent(
    env, start, algorithm
)

print("Selected Target:", target)
print("Selected Path:", path)
print("Nodes Explored:", explored)
print("Path Cost:", cost)


# Utility Based Agent

print("\n--- UTILITY BASED AGENT ---")

target, path, explored, utility = utility_agent(
    env, start, algorithm
)

print("Selected Target:", target)
print("Selected Path:", path)
print("Nodes Explored:", explored)
print("Utility Score:", utility)
