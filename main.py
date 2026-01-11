from colony import Colony, TerranEmpire
from resources import Food, Energy

def main():
    """
    Demo of the space colony system.
    Creates a Terran colony, adds resources, and simulates a few turns.
    """
    
    print("\n" + "="*60)
    print("SPACE COLONIES - Demo")
    print("="*60)
    
    # Create a Terran Empire colony
    print("\nCreating Alpha Station (Terran Empire)...")
    alpha_station = TerranEmpire(name="Alpha Station", population=150)
    
    # Add resources to the colony
    print("\nAdding resources...")
    alpha_station.add_resource(Food(quantity=100, production_rate=10, consumption_rate=5))
    alpha_station.add_resource(Energy(quantity=50, production_rate=15, consumption_rate=8))
    
    # Display initial state
    print("\n" + "="*60)
    print("INITIAL STATE")
    alpha_station.display_stats()
    
    # Simulate 5 turns
    print("\n" + "="*60)
    print("SIMULATING 5 TURNS")
    print("="*60)
    
    for turn in range(1, 6):
        print(f"\n>>> TURN {turn} <<<")
        alpha_station.tick()
        alpha_station.display_stats()
        
        # Show what happened
        food = alpha_station.get_resource("Food")
        energy = alpha_station.get_resource("Energy")
        
        if food and food.quantity < 50:
            print("⚠️  WARNING: Food supplies running low!")
        if energy and energy.quantity < 30:
            print("⚠️  WARNING: Energy reserves critical!")
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    
    # Show what your brother needs to build
    print("\nTODO for collaboration:")
    print("- Add Minerals and Oil resource classes")
    print("- Add MartianFederation nation class")
    print("- Add Trade class for resource transfers")
    print("- Add Game class to manage multiple colonies")
    print("- Build interactive CLI menu system")


if __name__ == "__main__":
    main()