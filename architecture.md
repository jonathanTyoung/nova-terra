# Space Colonies - Architecture & Code Explanation

## Project Overview

This is a CLI-based space colony simulation built to practice Object-Oriented Programming concepts in Python, specifically:
- **Inheritance** (child classes inherit from parent classes)
- **Composition** (objects contain other objects)
- **Polymorphism** (same method names, different behaviors)
- **Encapsulation** (data stored inside objects)

---

## What We've Built So Far

### 1. Resource System (`resources.py`)

#### Resource (Base Class)
The blueprint that all resource types inherit from.

**Attributes:**
- `name` - What the resource is called
- `quantity` - How much we currently have
- `production_rate` - How much is created each turn
- `consumption_rate` - How much is used each turn

**Methods:**
- `produce()` - Adds production_rate to quantity
- `consume()` - Subtracts consumption_rate from quantity
- `transfer(amount, target)` - Moves resources to another Resource object
- `__str__()` - Makes printing the resource look nice

**Why it's a base class:** Every resource (Food, Energy, Minerals, Oil) needs these same basic properties and behaviors. Instead of rewriting this code 4 times, we write it once and let child classes inherit it.

#### Food (Subclass of Resource)
**Inherits:** Everything from Resource (all attributes and methods)

**Adds:**
- `spoilage_rate` - Percentage of food that spoils each turn (5%)

**Overrides:**
- `consume()` - Calls parent's consume(), THEN adds spoilage loss

**Why override?** Food has unique behavior - it spoils. Energy doesn't spoil. So Food needs its own version of consume() that adds this extra step.
```python
class Food(Resource):
    def __init__(self, quantity=0, production_rate=10, consumption_rate=5):
        super().__init__("Food", quantity, production_rate, consumption_rate)
        self.spoilage_rate = 0.05
    
    def consume(self):
        super().consume()  # Do normal consumption first
        spoilage = int(self.quantity * self.spoilage_rate)  # Calculate spoilage
        self.quantity = max(0, self.quantity - spoilage)  # Apply spoilage
```

**Key concept - `super()`:** Calls the parent class's method. Here it says "do Resource's consume() first, then I'll add my spoilage behavior."

#### Energy (Subclass of Resource)
**Inherits:** Everything from Resource

**Adds:**
- `max_storage` - Can't store more than 200 energy

**Overrides:**
- `produce()` - Calls parent's produce(), THEN checks storage limit

**Why override?** Energy has a storage cap. If we produce more than we can store, we waste it.

---

### 2. Colony System (`colony.py`)

#### Colony (Base Class)
The blueprint that all nation types inherit from.

**Attributes:**
- `name` - Colony's name (e.g., "Alpha Station")
- `population` - Number of people
- `resources` - Dictionary storing Resource objects (e.g., `{"Food": Food_object, "Energy": Energy_object}`)

**Methods:**
- `add_resource(resource)` - Stores a Resource object in the dictionary
- `get_resource(name)` - Retrieves a specific resource
- `tick()` - Processes one turn (calls produce() and consume() on all resources)
- `display_stats()` - Prints colony info

**Why use a dictionary for resources?** We can look up resources by name: `colony.resources["Food"]` is faster and cleaner than searching through a list.

**This is COMPOSITION:** A Colony *has* Resources. It contains them. This is different from inheritance where a class *is a* type of another class.

#### TerranEmpire (Subclass of Colony)
**Inherits:** Everything from Colony

**Adds:**
- `nation` - Name of the nation ("Terran Empire")
- `food_bonus` - 1.2 multiplier (20% bonus to food production)

**Overrides:**
- `add_resource()` - Calls parent's add_resource(), THEN applies food bonus if it's Food
- `display_stats()` - Shows nation name and special abilities

**Why override add_resource()?** When we add Food to a Terran colony, we want to automatically boost its production. This happens once when the resource is added.
```python
def add_resource(self, resource):
    super().add_resource(resource)  # Store it normally first
    if resource.name == "Food":  # Then check if it's food
        resource.production_rate = int(resource.production_rate * self.food_bonus)
```

---

### 3. Demo (`main.py`)

Shows everything working together:

1. **Creates a TerranEmpire colony**
```python
   alpha_station = TerranEmpire(name="Alpha Station", population=150)
```

2. **Adds resources to it**
```python
   alpha_station.add_resource(Food(quantity=100, production_rate=10, consumption_rate=5))
```
   - Food starts at 100 units
   - Would normally produce 10/turn, but Terran bonus makes it 12/turn
   - Consumes 5/turn + 5% spoilage

3. **Simulates 5 turns**
```python
   alpha_station.tick()  # Processes one turn
```
   - Each turn: all resources produce, then consume
   - Food: +12 (production) -5 (consumption) -~5 (spoilage) = net +2 per turn
   - Energy: +15 (production) -8 (consumption) = net +7 per turn (until hitting 200 cap)

---

## Key OOP Concepts Demonstrated

### 1. Inheritance
```
Resource
├── Food (inherits from Resource)
└── Energy (inherits from Resource)

Colony
└── TerranEmpire (inherits from Colony)
```

**Why?** Avoid code duplication. Food and Energy share 90% of their code (from Resource), only differing in their special behaviors.

### 2. Method Overriding
Child class replaces parent's method with its own version.

**Example:** Food overrides `consume()` to add spoilage behavior that Resource doesn't have.

### 3. `super()` Function
Calls the parent class's version of a method.

**When to use:**
- In `__init__()` - Let parent initialize its attributes first
- In overridden methods - Do parent's behavior, then add your own

### 4. Composition
One object contains other objects.

**Example:** Colony has a dictionary of Resources. Colony doesn't inherit from Resource - it *contains* Resources.

---

## How Data Flows

### Creating a Colony with Resources:
```python
# 1. Create the colony instance
alpha = TerranEmpire("Alpha Station", population=150)
# Calls TerranEmpire.__init__()
#   Which calls Colony.__init__() via super()
#     Sets name="Alpha Station", population=150, resources={}

# 2. Create a Food resource
food = Food(quantity=100, production_rate=10, consumption_rate=5)
# Calls Food.__init__()
#   Which calls Resource.__init__() via super()
#     Sets name="Food", quantity=100, production_rate=10, consumption_rate=5
#   Then sets spoilage_rate=0.05

# 3. Add Food to colony
alpha.add_resource(food)
# Calls TerranEmpire.add_resource()
#   Which calls Colony.add_resource() via super()
#     Stores food in resources dict: resources["Food"] = food
#   Then checks if it's Food and applies bonus:
#     food.production_rate = 10 * 1.2 = 12
```

### Processing a Turn:
```python
alpha.tick()
# Colony.tick() loops through all resources and calls:

# For Food:
food.produce()
# Resource.produce() adds 12 to quantity

food.consume()
# Food.consume() (not Resource.consume()!)
#   Calls Resource.consume() via super() - subtracts 5
#   Then calculates spoilage: quantity * 0.05
#   Subtracts spoilage from quantity

# For Energy:
energy.produce()
# Energy.produce() (not Resource.produce()!)
#   Calls Resource.produce() via super() - adds 15
#   Then checks if quantity > 200, caps it if so

energy.consume()
# Resource.consume() - subtracts 8
```

---

## What Your Brother Should Build

### 1. Additional Resource Subclasses
**File:** `resources.py`
```python
class Minerals(Resource):
    """
    Mining resources - used for construction.
    Could have: extraction_efficiency, depletion_rate, etc.
    """
    pass

class Oil(Resource):
    """
    Fuel resource - powers ships/machinery.
    Could have: refining_rate, volatility, etc.
    """
    pass
```

**Follow the pattern:** Inherit from Resource, add unique attributes/methods if needed.

### 2. Additional Nation Subclasses
**File:** `colony.py`
```python
class MartianFederation(Colony):
    """
    Mars-based colonies.
    Could have: Energy production bonus (fusion tech)
    """
    def __init__(self, name, population=100):
        super().__init__(name, population)
        self.nation = "Martian Federation"
        self.energy_bonus = 1.3  # 30% energy bonus
    
    def add_resource(self, resource):
        super().add_resource(resource)
        if resource.name == "Energy":
            resource.production_rate = int(resource.production_rate * self.energy_bonus)
```

### 3. Trade System
**File:** `trade.py`
```python
class Trade:
    """
    Handles resource transfers between colonies.
    """
    def __init__(self, from_colony, to_colony, resource_name, amount):
        self.from_colony = from_colony
        self.to_colony = to_colony
        self.resource_name = resource_name
        self.amount = amount
    
    def validate(self):
        """Check if trade is possible."""
        # Does from_colony have enough of the resource?
        pass
    
    def execute(self):
        """Perform the trade if valid."""
        pass
```

### 4. Game Manager
**File:** `game.py`
```python
class Game:
    """
    Manages the overall game state and loop.
    """
    def __init__(self):
        self.colonies = []  # List of all Colony objects
        self.turn_number = 0
    
    def add_colony(self, colony):
        """Add a colony to the game."""
        self.colonies.append(colony)
    
    def next_turn(self):
        """Process one turn for all colonies."""
        self.turn_number += 1
        for colony in self.colonies:
            colony.tick()
    
    def display_all(self):
        """Show stats for all colonies."""
        for colony in self.colonies:
            colony.display_stats()
```

### 5. Interactive CLI Menu
**File:** `main.py` (expand it)
```python
def game_loop():
    """Main interactive game loop."""
    game = Game()
    
    while True:
        print("\n=== SPACE COLONIES ===")
        print("1. View all colonies")
        print("2. Create new colony")
        print("3. Trade resources")
        print("4. Next turn")
        print("5. Exit")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            game.display_all()
        elif choice == "2":
            # Code to create a colony
            pass
        # ... etc
```

---

## Testing Your Understanding

Try these exercises:

1. **Create a new resource type** (e.g., Water) that has a purification process
2. **Create a new nation** (e.g., JupiterConsortium) with a mining bonus
3. **Add a method to Colony** that calculates total resource value
4. **Override tick()** in a nation class to add unique turn behavior
5. **Make resources tradeable** - use the `transfer()` method between colonies

---

## Common Questions

**Q: When do I use inheritance vs composition?**
- Inheritance = "is a" relationship (Food *is a* Resource)
- Composition = "has a" relationship (Colony *has* Resources)

**Q: When should I override a method?**
- When the child class needs different behavior than the parent
- Example: Food's consume() needs spoilage, Resource's doesn't

**Q: What does `super()` do?**
- Calls the parent class's version of a method
- Lets you reuse parent's code and add to it

**Q: Why use `__init__` with `super().__init__()`?**
- Parent class needs to initialize its attributes first
- Then child can add its own attributes

---

## Next Steps

1. **Study this file together** - trace through the code examples
2. **Run the demo** - watch the output, understand what's happening each turn
3. **Experiment** - change values, add print statements, break things
4. **Plan together** - decide who builds what from the TODO list
5. **Build incrementally** - one class at a time, test as you go
6. **Integrate** - combine your work and make it all work together

Good luck! 🚀