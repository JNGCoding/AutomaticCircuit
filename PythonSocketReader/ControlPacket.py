class ControlPacket(object):
    def __init__(self) -> None:
        self.relay1 = False
        self.relay2 = False
        self.auto_mode = False
        self.temperature = 0.0
        self.humidity = 0.0
        self.light = 0.0
    
    def set(self, relay1: bool, relay2: bool, auto_mode: bool, temperature: float, humidity: float, light: float) -> None:
        self.relay1 = relay1
        self.relay2 = relay2
        self.auto_mode = auto_mode
        self.temperature = temperature
        self.humidity = humidity
        self.light = light

    def __str__(self) -> str:
        return f"ControlPacket(\n\trelay1 = {self.relay1}\n\trelay2 = {self.relay2}\n\tauto_mode = {self.auto_mode}\n\ttemperature = {self.temperature}\n\thumidity = {self.humidity}\n\tlight = {self.light}\n)"