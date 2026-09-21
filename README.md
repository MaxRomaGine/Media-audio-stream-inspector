# Media Audio Stream Inspector

Lightweight, zero-bloat CLI streaming audio inspector designed for low-latency broadcast telemetry (RMS loudness proxy + derivative energy transient gating).

## Architecture / Data Flow
```text
[Audio Stream / 100ms Chunk] 
       │
       ▼
[RMS Energy (Vectorized NumPy)] ──┬──> [LUFS Proxy Scale (-70 to 0 dB)]
                                  │
                                  └──> [Derivative Gate (Et - Et-1)] ──> [Transient Flag]
## Why this exists
Instead of running heavy inference or expensive framing on full streams, this acts as a lightweight edge gate/trigger for media monitoring pipelines (ingestion pre-filter).

## Quickstart
pip install -r requirements.txt
python -m src.cli --demo
