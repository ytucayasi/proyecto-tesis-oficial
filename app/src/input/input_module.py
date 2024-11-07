from nest.core import Module
from .input_controller import InputController
from .input_service import InputService

@Module(
    controllers=[InputController],
    providers=[InputService]
)
class InputModule:
    pass