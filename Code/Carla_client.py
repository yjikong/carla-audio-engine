import carla
import time
import math

def get_speed(vehicle):
    """Calculate speed of a vehicle in km/h"""
    vel = vehicle.get_velocity()
    speed = math.sqrt(vel.x**2 + vel.y**2 + vel.z**2)  # in m/s
    return speed * 3.6  # convert to km/h

def main():
    # Connect to CARLA server
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    # Wait until the player-controlled vehicle (role_name='hero') appears
    player_vehicle = None
    while player_vehicle is None:
        vehicles = world.get_actors().filter('vehicle.*')
        for v in vehicles:
            if v.attributes.get('role_name') == 'hero':
                player_vehicle = v
                break
        if player_vehicle is None:
            print("Waiting for player vehicle to spawn...")
            time.sleep(1)

    print(f"Tracking speed of vehicle: {player_vehicle.type_id}")

    # Continuously track and print speed
    try:
        while True:
            speed = get_speed(player_vehicle)
            print(f"Current speed: {speed:.2f} km/h")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped tracking.")

if __name__ == "__main__":
    main()
