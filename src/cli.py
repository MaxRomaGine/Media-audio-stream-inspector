import argparse
import time
import numpy as np
import soundfile as sf
from rich.console import Console
from src.stream_processor import StreamAudioInspector

console = Console()

def process_stream(data: np.ndarray, inspector: StreamAudioInspector, source_label: str):
    chunk_size = inspector.chunk_size
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # downmix estéreo/multicanal a mono
        
    console.print(f"[bold green]=== Streaming: {source_label} ({len(data)} samples) ===[/bold green]")
    
    ptr = 0
    try:
        while ptr < len(data) - chunk_size:
            chunk = data[ptr:ptr+chunk_size]
            ptr += chunk_size
            
            telemetry = inspector.process_chunk(chunk)
            norm_val = int(max(0, min(40, (telemetry.lufs_proxy + 70) * 0.57)))
            bar = "█" * norm_val + "░" * (40 - norm_val)
            
            status = "[bold red]TRANSIENT![/bold red]" if telemetry.is_transient else "[dim]OK      [/dim]"
            console.print(f"LUFS: {telemetry.lufs_proxy:6.2f} dB | [{bar}] | {status}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")

def run_demo():
    inspector = StreamAudioInspector()
    chunk_size = inspector.chunk_size
    num_chunks = 40  # 4 segundos
    np.random.seed(42)
    data = np.random.randn(num_chunks * chunk_size).astype(np.float32) * 0.05
    data[15*chunk_size:15*chunk_size+220] *= 8.0  # inyecta pico
    process_stream(data, inspector, "Synthetic Demo")

def run_file(file_path: str):
    inspector = StreamAudioInspector()
    data, sr = sf.read(file_path)
    process_stream(data.astype(np.float32), inspector, file_path)

def main():
    parser = argparse.ArgumentParser(description="Media Audio Stream Inspector CLI")
    parser.add_argument("--demo", action="store_true", help="Run synthetic live demo stream")
    parser.add_argument("--file", type=str, help="Path to real .wav file")
    args = parser.parse_args()
    
    if args.file:
        run_file(args.file)
    elif args.demo:
        run_demo()
    else:
        console.print("[yellow]Pass --demo or --file <path.wav>[/yellow]")

if __name__ == "__main__":
    main()