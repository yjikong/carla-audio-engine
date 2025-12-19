import carla
import time
import math

class Carla_client:
    def get_weather():
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)

        world = client.get_world()
        weather_parameters = world.get_weather()
        return weather_parameters

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

    # Continuously track and print speed
    try:
        while True:
            time.sleep(1)
            weather = Carla_client.get_weather()
            rain = weather.precipitation
            wind = weather.wind_intensity
            print(f"Rain: {rain}, Wind: {wind}")

            # Always overwrite with the newest data
            with open("weather_data.txt", "w") as f:
                f.write(f"{rain},{wind}")
    except KeyboardInterrupt:
        print("\nStopped tracking.")

if __name__ == "__main__":
    main()
