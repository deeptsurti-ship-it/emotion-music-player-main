import os
import sys
import wave
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

output_dir = 'downloaded_songs'
os.makedirs(output_dir, exist_ok=True)
sample_rate = 44100

def create_tone(freqs, duration, style='smooth'):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    signal = np.zeros_like(t)
    
    if style == 'arpeggio':
        note_dur = duration / len(freqs)
        for i, f in enumerate(freqs):
            start = int(i * note_dur * sample_rate)
            end = int((i + 1) * note_dur * sample_rate)
            sub_t = t[start:end] - t[start]
            env = np.sin(np.pi * sub_t / note_dur) ** 0.5 * np.exp(-sub_t * 1.5)
            # Fundamental + soft harmonics
            harm = np.sin(2 * np.pi * f * sub_t) + 0.3 * np.sin(4 * np.pi * f * sub_t)
            signal[start:end] += env * harm
    elif style == 'chord':
        env = np.sin(np.pi * t / duration)
        for f in freqs:
            signal += (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * env
    elif style == 'bass':
        note_dur = 0.5
        num_beats = int(duration / note_dur)
        for b in range(num_beats):
            f = freqs[b % len(freqs)]
            start = int(b * note_dur * sample_rate)
            end = int((b + 1) * note_dur * sample_rate)
            sub_t = t[start:end] - t[start]
            env = np.exp(-sub_t * 4.0)
            signal[start:end] += (np.sin(2 * np.pi * f * sub_t) + 0.5 * np.sin(2 * np.pi * (f*1.5) * sub_t)) * env
    else: # ambient
        env = np.sin(np.pi * t / duration) ** 1.5
        for f in freqs:
            lfo = 1.0 + 0.1 * np.sin(2 * np.pi * 0.5 * t)
            signal += np.sin(2 * np.pi * f * t * lfo) * env
            
    # Normalize
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val * 0.85
    return (signal * 32767).astype(np.int16)

emotions_audio = {
    'happy': ([523.25, 659.25, 783.99, 1046.50, 783.99, 1046.50], 8.0, 'arpeggio'), # C Major uplifting
    'sad': ([220.00, 261.63, 329.63, 220.00], 10.0, 'chord'), # A Minor somber
    'angry': ([110.00, 116.54, 110.00, 123.47], 8.0, 'bass'), # Low pounding bass
    'fear': ([185.00, 233.08, 277.18, 311.13], 9.0, 'ambient'), # Suspense drone
    'surprise': ([440.00, 554.37, 659.25, 880.00, 1108.73], 6.0, 'arpeggio'), # A Major ascending sparkle
    'disgust': ([233.08, 246.94, 293.66, 311.13], 8.0, 'chord'), # Dissonant / moody blues
    'neutral': ([261.63, 329.63, 392.00, 493.88], 10.0, 'chord') # Calm serene lofi
}

for emotion, (freqs, dur, style) in emotions_audio.items():
    filepath = os.path.join(output_dir, f"{emotion}.wav")
    audio = create_tone(freqs, dur, style)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    print(f"Generated {filepath}")

print("All sample audio files generated successfully!")
