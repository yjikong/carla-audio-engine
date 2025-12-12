import carla

client = carla.Client()
world = client.get_world()
settings = world.get_settings()
settings.no_rendering_mode = True
world.apply_settings(settings)
