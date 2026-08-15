import numpy as np

class GVFFieldGenerator:
    """
    Generates time-dependent dynamic AC threshold waves for SNN membrane arrays.
    Formula: Threshold(t) = Base + Amplitude * sin(2*pi * Frequency * t + Phase)
    """
    def __init__(self, v_base: float = 1.0, amplitude: float = 0.4, frequency: float = 0.05, phase: float = 0.0):
        self.v_base = v_base
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def get_threshold(self, time_step: int) -> float:
        """Calculates dynamic threshold voltage at a discrete time-step t."""
        if self.amplitude == 0.0 or self.frequency == 0.0:
            return self.v_base
            
        sine_term = np.sin(2 * np.pi * self.frequency * time_step + self.phase)
        return self.v_base + (self.amplitude * sine_term)
