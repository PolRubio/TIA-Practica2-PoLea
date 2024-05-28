import random

class Order:
    def __init__(self, priority, weight):
        self.priority = priority
        self.weight = weight

def hill_climbing(orders, weight_limit, max_iterations):
    def fitness(orders, weight_limit):
        total_weight = 0
        num_orders = 0
        priority_sum = 0
        for order in orders:
            if total_weight + order.weight > weight_limit:
                break
            num_orders += 1
            total_weight += order.weight
            priority_sum += order.priority*0.9**num_orders
        return (-priority_sum, num_orders)

    def generate_neighbors(orders):
        neighbors = []
        for i in range(len(orders)):
            for j in range(i + 1, len(orders)):
                neighbor = orders[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors
    
    current_solution = orders[:]
    current_fitness = fitness(current_solution, weight_limit)
    repeat = 0
    for i in range(max_iterations):
        neighbors = generate_neighbors(current_solution)
        neighbor_fitnesses = [(fitness(neighbor, weight_limit), neighbor) for neighbor in neighbors]
        best_fitness, best_neighbor = max(neighbor_fitnesses, key=lambda x: x[0])
        if best_fitness > current_fitness:
            current_solution = best_neighbor
            current_fitness = best_fitness
            repeat = 0
        else:
            repeat += 1
            if repeat > max_iterations*0.1:
                break
    
    total_weight = 0
    valid_orders = []
    for order in current_solution:
        if total_weight + order.weight > weight_limit:
            break
        total_weight += order.weight
        valid_orders.append(order)
    
    return valid_orders

# Example usage
possible_tipe_of_order = [
    Order(35, 400),
    Order(38, 380),
    Order(25, 425),
    Order(24, 450),
    Order(15, 400),
    Order(17, 395),
    Order(12, 410),
    Order(20, 440),
    Order(30, 300),
    Order(18, 370),
    Order(16, 405),
    Order(19, 385),
    Order(28, 395),
    Order(32, 350)
]

orders = random.choices(possible_tipe_of_order, k=20)

weight_limit = 30000000
max_iterations = 100


print()
print("Initial Orders:")
for order in orders:
    print(f"\tPriority: {order.priority}, Weight: {order.weight}")

total_weight = 0
print()
print("Sorted Orders Hill Climbing:")
orders2 = orders[:]
while len(orders2) > 0:
    sorted_orders = hill_climbing(orders2, weight_limit, max_iterations)
    for order in sorted_orders:
        orders2.remove(order)
        print(f"\tPriority: {order.priority}, Weight: {order.weight}")
    print("-------------------------------------------")


print()
print(f"Total weight: {total_weight}")


print()
print("Sorted Orders Real Answer:")
sorted_orders = sorted(orders, key=lambda x: x.priority)
total_weight = 0
for order in sorted_orders:
    if total_weight + order.weight > weight_limit:
        print("-------------------------------------------")
        total_weight = 0
        # break
    total_weight += order.weight
    print(f"\tPriority: {order.priority}, Weight: {order.weight}")