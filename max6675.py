from machine import Pin, SoftSPI, SPI # type: ignore
import time

# MAX6675 thermocouple sensor
class MAX6675:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, value=1)

    def read(self):
        self.cs.value(0)
        self.spi.write(b'\xFF\xFF')
        d = self.spi.read(2)
        self.cs.value(1)
        if d[1] & 0x04:
            return float('NaN')
        return (d[0] << 8 | d[1]) >> 3
    
    def read_temp(self):
        return self.read() * 0.25
    
    def read_fahrenheit(self):
        return self.read_temp() * 9.0 / 5.0 + 32
    
