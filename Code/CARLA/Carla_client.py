import carla
import math
import time
import socket
import json

# Socket Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    try:
        # 1. Verbindung aufbauen
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        # 2. Ein Fahrzeug finden (entweder ein vorhandenes oder neu spawnen)
        vehicles = world.get_actors().filter('vehicle.*')
        
        if vehicles:
            vehicle = vehicles[0]
            print(f"Verbunden mit vorhandenem Fahrzeug: {vehicle.type_id}")
        else:
            # Falls kein Auto da ist, eines spawnen
            bp = world.get_blueprint_library().find('vehicle.tesla.model3')
            spawn_point = world.get_map().get_spawn_points()[0]
            vehicle = world.spawn_actor(bp, spawn_point)
            vehicle.set_autopilot(True)
            print("Neues Fahrzeug gespawnt und Autopilot aktiviert.")

        print("Lese Geschwindigkeit aus... (Strg+C zum Beenden)")

        # 3. Endlosschleife zur Geschwindigkeitsmessung
        while True:
            # Den Velocity-Vektor abrufen
            v = vehicle.get_velocity()
            
            # Die physikalische Geschwindigkeit berechnen: sqrt(x^2 + y^2 + z^2)
            # CARLA liefert m/s, wir rechnen in km/h um
            kmh = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
            control = vehicle.get_control()

            data_packet = {
                "speed": round(kmh, 2),
                "throttle": round(control.throttle, 2),
                "brake": round(control.brake, 2),
                "timestamp": time.time()
            }

            message = json.dumps(data_packet).encode()
            sock.sendto(message, (UDP_IP, UDP_PORT))

            # Ausgabe in der Konsole (\r sorgt dafür, dass die Zeile überschrieben wird)
            print(f"Aktuelle Geschwindigkeit: {kmh:6.2f} km/h", end='\r')
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nMessung durch Benutzer beendet.")
    except Exception as e:
        print(f"\nFehler: {e}")

if __name__ == '__main__':
    main()