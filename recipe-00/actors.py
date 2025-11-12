import ray

# Init a "ray cluster."
ray.init()

# This Python class (aka "Ray Actor") is considered "stateful" because it saves
# state as its method are invocated. 
@ray.remote
class Agent:
    def __init__(self):
        self.number = 0

    def get(self):
        return self.number

    def increment(self, value):
        self.number += value

# Declare an instance of the Python class using the decorator that was added to it. 
agent = Agent.remote()

# Call to the Ray Actor (a process). Each call will be ran asynchronously but in 
# the order they were submitted. 
for number in range(10):
    agent.increment.remote(number)

# Get all objects using the object references saved in the Ray Actor's state. 
objects = ray.get(agent.get.remote())

# Print the results.
print(objects)
