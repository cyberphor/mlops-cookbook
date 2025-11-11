import ray

ray.init()

# This "task" will be ran "remotely" (on the "ray cluster").
@ray.remote
def square(x):
    return x * x

# Run the task for the number of times specified. The demonstrates dynamically 
# setting the number of parallel tasks to run. It also demonstrates passing 
# unique values to each task instance.  
objects = [square.remote(i) for i in range(4)]

# Get the results from each object.
results = ray.get(objects)

# Print the results.
print(results)
