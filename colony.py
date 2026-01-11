from resources import Resource


class Colony:
    """
    Base class for all colonies.
    Nations like TerranEmpire, MartianFederation inherit from this.
    """

    def __init__(self, name, population=100):
        """
        Initialize a colony.

        Args:
            name (str): Name of the colony
            population (int): Number of people in the colony
        """
        self.name = name
        self.population = population
        self.resources = {}  # Dictionary to store Resource objects

    def add_resource(self, resource):
        """
        Add a resource to the colony's resource pool.

        Args:
            resource (Resource): A Resource object (Food, Energy, etc.)
        """
        self.resources[resource.name] = resource

    def get_resource(self, resource_name):
        """
        Get a specific resource by name.

        Args:
            resource_name (str): Name of resource to retrieve

        Returns:
            Resource or None: The resource if it exists, None otherwise
        """
        return self.resources.get(resource_name)

    def tick(self):
        """
        Process one turn for this colony.
        All resources produce and consume.
        """
        print(f"\n--- {self.name} processing turn ---")
        for resource in self.resources.values():
            resource.produce()
            resource.consume()

    def display_stats(self):
        """Show colony information and all resources."""
        print(f"\n{'='*50}")
        print(f"{self.name}")
        print(f"Population: {self.population}")
        print(f"{'-'*50}")
        if self.resources:
            for resource in self.resources.values():
                print(f"  {resource}")
        else:
            print("  No resources")
        print(f"{'='*50}")


class TerranEmpire(Colony):
    """
    Terran Empire - Earth-based colonies.
    Bonus: 20% increased food production (advanced agriculture)
    """

    def __init__(self, name, population=100):
        super().__init__(name, population)
        self.nation = "Terran Empire"
        self.food_bonus = 1.2  # 20% food production bonus

    def add_resource(self, resource):
        """Override to apply Terran bonuses when adding resources."""
        super().add_resource(resource)
        # Apply food bonus if it's a Food resource
        if resource.name == "Food":
            resource.production_rate = int(resource.production_rate * self.food_bonus)
            print(
                f"  Terran agriculture bonus applied! Food production: {resource.production_rate}/turn"
            )

    def display_stats(self):
        """Override to show nation affiliation."""
        print(f"\n{'='*50}")
        print(f"{self.name} [{self.nation}]")
        print(f"Population: {self.population}")
        print(f"Special: +20% Food Production")
        print(f"{'-'*50}")
        if self.resources:
            for resource in self.resources.values():
                print(f"  {resource}")
        else:
            print("  No resources")
        print(f"{'='*50}")


# TODO: Add MartianFederation class (for Jon to build)
# Suggestion: Could have energy production bonus (advanced fusion tech)
# Some starter code below:
class MartianFederation(Colony):
    def __init__(self, name, population=100):
        super().__init__(name, population)
        self.nation = "Martian Federation"
        self.energy_bonus = 1.3  # 30% energy bonus

    def add_resource(self, resource):
        super().add_resource(resource)
        if resource.name == "Energy":
            resource.production_rate = int(resource.production_rate * self.energy_bonus)


# TODO: Add JupiterConsortium class (for Chris to build)
# Suggestion: Could have mining/minerals bonus (gas giant mining operations)
