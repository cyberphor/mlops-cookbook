import ray

# Init a "ray cluster."
ray.init()

# This Python function (aka "Ray Task") will be executed on the ray cluster.
# This Python function is considered "stateless" because it does not save state
# between invocations. 
@ray.remote
def square(x):
    return x * x

# Call the function using the decorator that was added to it. Each invocation 
# will produce an "object reference."
object_refs = []
for value in range(4):
    object_refs.append(square.remote(value))

# Get all objects using the references generated above.
objects = ray.get(object_refs)

# Print the results.
print(objects)
