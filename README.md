# media-audio-stream-inspector

cli tool in python for streaming audio processing (100ms chunks), hot RMS/LUFS calc, and zero-melt transient gating.

## why this exists
if you're building media monitoring pipelines, you can't run heavy inference or dump full files into ram. you need a cheap edge gate that says "something's happening here" before wasting compute downstream.

## what it does
- chunks the stream into 100ms fixed buffers.
- computes rms using vectorized numpy.
- maps to log scale (lufs proxy).
- tracks energy diff between current and prev chunk ($E_t - E_{t-1}$). spikes hard -> flags `TRANSIENT!`.

## quickstart

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# generate a quick test wav with a spike at t=2s
python3 -c "import numpy as np, soundfile as sf; sr=44100; t=np.linspace(0, 5, sr*5); data=0.1*np.sin(2*np.pi*440*t); data[sr*2:sr*2+500]*=10; sf.write('test.wav', data, sr)"

# test with real wav
python3 -m src.cli --file test.wav

# or synthetic demo
python3 -m src.cli --demo
