class finder:
    def get_vehicle(world):
        vehicles = world.get_actors().filter('vehicle.*')

        if vehicles:
            vehicle = vehicles[0]
            print(f"Verbunden mit vorhandenem Fahrzeug: {vehicle.type_id}")
        else:
            print("Es wurden keine Autos gefunden!")
        
        return vehicle