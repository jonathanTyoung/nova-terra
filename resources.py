class Resource:
    """
    Base class for all resources in the game.
    All specific resource types (Food, Energy, Minerals, Oil) inherit from this.
    """
    
    def __init__(self, name, quantity=0, production_rate=0, consumption_rate=0):
        """
        Initialize a resource.
        
        Args:
            name (str): Name of the resource
            quantity (int): Current amount available
            production_rate (int): Amount produced per turn
            consumption_rate (int): Amount consumed per turn
        """
        self.name = name
        self.quantity = quantity
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
    
    def produce(self):
        """Increase quantity based on production rate."""
        self.quantity += self.production_rate
        return self.quantity
    
    def consume(self):
        """Decrease quantity based on consumption rate."""
        self.quantity = max(0, self.quantity - self.consumption_rate)
        return self.quantity
    
    def transfer(self, amount, target_resource):
        """
        Transfer resources to another resource instance.
        
        Args:
            amount (int): How much to transfer
            target_resource (Resource): The resource object receiving the transfer
            
        Returns:
            bool: True if transfer succeeded, False if insufficient resources
        """
        if self.quantity >= amount:
            self.quantity -= amount
            target_resource.quantity += amount
            return True
        return False
    
    def __str__(self):
        """String representation for easy printing."""
        return f"{self.name}: {self.quantity} (produces {self.production_rate}/turn, consumes {self.consumption_rate}/turn)"


class Food(Resource):
    """
    Food resource - consumed by colony population.
    Has a spoilage rate where some food is lost each turn.
    """
    
    def __init__(self, quantity=0, production_rate=10, consumption_rate=5):
        super().__init__("Food", quantity, production_rate, consumption_rate)
        self.spoilage_rate = 0.05  # 5% of food spoils each turn
    
    def consume(self):
        """Override consume to include spoilage."""
        # Normal consumption
        super().consume()
        # Additional loss from spoilage
        spoilage = int(self.quantity * self.spoilage_rate)
        self.quantity = max(0, self.quantity - spoilage)
        return self.quantity


class Energy(Resource):
    """
    Energy resource - powers colony systems.
    Has a maximum storage capacity.
    """
    
    def __init__(self, quantity=0, production_rate=15, consumption_rate=8):
        super().__init__("Energy", quantity, production_rate, consumption_rate)
        self.max_storage = 200  # Can't store more than this
    
    def produce(self):
        """Override produce to respect storage limit."""
        super().produce()
        # Cap at max storage
        if self.quantity > self.max_storage:
            excess = self.quantity - self.max_storage
            self.quantity = self.max_storage
            print(f"  Warning: {excess} energy wasted due to storage limits!")
        return self.quantity


# TODO: Add Minerals class (for Jon to build)
# TODO: Add Oil class (for Chris to build)