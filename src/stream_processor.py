import numpy as np
from dataclasses import dataclass

@dataclass
class FrameTelemetry:
    rms: float
    lufs_proxy: float
    delta_energy: float
    is_transient: bool

class StreamAudioInspector:
    def __init__(self, sample_rate: int = 44100, chunk_ms: int = 100, transient_threshold: float = 0.002):
        self.sample_rate = sample_rate
        self.chunk_size = int(sample_rate * (chunk_ms / 1000.0))
        self.threshold = transient_threshold
        self.prev_energy = 0.0

    def process_chunk(self, chunk: np.ndarray) -> FrameTelemetry:
        if len(chunk) == 0:
            rms = 0.0
        else:
            rms = float(np.sqrt(np.mean(chunk.astype(np.float32)**2)))
            
        lufs_proxy = -70.0 if rms < 1e-6 else float(20 * np.log10(rms))
        current_energy = rms ** 2
        diff = current_energy - self.prev_energy
        is_transient = diff > self.threshold
        self.prev_energy = current_energy

        return FrameTelemetry(
            rms=rms,
            lufs_proxy=lufs_proxy,
            delta_energy=max(0.0, diff),
            is_transient=is_transient
        )