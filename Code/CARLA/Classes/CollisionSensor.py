import weakref
import collections
import math
import carla

class CollisionSensor(object):
    collision_counter = 0
    intensity = 0

    def __init__(self, parent_actor):
        self.sensor = None
        self.history = []
        if parent_actor is not None:
            self._parent = parent_actor
            self.world = self._parent.get_world()
            print(self.world)
            bp = self.world.get_blueprint_library().find('sensor.other.collision')
            self.sensor = self.world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
            # We need to pass the lambda a weak reference to self to avoid circular
            # reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda event: CollisionSensor._on_collision(weak_self, event))

    def get_collision_history(self):
        history = collections.defaultdict(int)
        for frame, intensity in self.history:
            history[frame] += intensity
        return history

    @staticmethod
    def _on_collision(weak_self, event):
        CollisionSensor.collision_counter = CollisionSensor.collision_counter + 1
        self = weak_self()
        if not self:
            return
        impulse = event.normal_impulse
        CollisionSensor.intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)
        self.history.append((event.frame, CollisionSensor.intensity))
        if len(self.history) > 4000:
            self.history.pop(0)