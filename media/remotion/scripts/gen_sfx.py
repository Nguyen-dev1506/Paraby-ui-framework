"""
Synthesizes a full sound-design track for media/remotion/out/ParabyIntro.mp4
and muxes it onto the ALREADY-RENDERED video via ffmpeg stream copy — the
video frames are never touched (no Remotion re-render), only an audio
track is added on top.

All sounds are procedurally generated (sine/noise + envelopes), not sourced
from any external library, so there's no licensing question.

Usage (from media/remotion/):
    python scripts/gen_sfx.py
"""
import numpy as np
from scipy.io import wavfile
import subprocess
import os

SR = 44100
DURATION = 135.06  # matches ffprobe duration of the rendered mp4

master = np.zeros(int(SR * DURATION), dtype=np.float64)


def _place(sound, t):
    start = int(t * SR)
    end = start + len(sound)
    if end > len(master):
        sound = sound[: len(master) - start]
        end = len(master)
    master[start:end] += sound


def _fade_env(n, attack, release):
    env = np.ones(n)
    a = min(attack, n // 2)
    r = min(release, n // 2)
    if a > 0:
        env[:a] = (1 - np.cos(np.linspace(0, np.pi, a))) / 2
    if r > 0:
        env[-r:] = (1 - np.cos(np.linspace(np.pi, 0, r))) / 2
    return env


def pop(freq=550, duration=0.14, vol=0.5):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sweep = freq * (1 + 1.8 * np.exp(-t * 26))
    phase = 2 * np.pi * np.cumsum(sweep) / SR
    sig = np.sin(phase)
    env = np.exp(-t * 22) * _fade_env(n, int(SR * 0.002), int(SR * 0.08))
    return sig * env * vol


def tick(freq=1400, duration=0.045, vol=0.28):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * freq * t) + 0.4 * np.random.default_rng(int(freq)).standard_normal(n)
    env = np.exp(-t * 90) * _fade_env(n, int(SR * 0.001), int(SR * 0.03))
    return sig * env * vol


def whoosh(duration=0.4, vol=0.3, rise=True):
    n = int(SR * duration)
    t = np.arange(n) / SR
    rng = np.random.default_rng(42)
    noise = rng.standard_normal(n)
    # crude band-pass: difference of two exponential moving averages, with a
    # slowly swept center via amplitude modulation to fake a "whoosh" sweep.
    b, a = 0.06, 0.985
    fast = np.zeros(n)
    slow = np.zeros(n)
    for i in range(1, n):
        fast[i] = fast[i - 1] * 0.55 + noise[i] * 0.45
        slow[i] = slow[i - 1] * a + noise[i] * (1 - a)
    band = fast - slow
    sweep_shape = np.linspace(0, 1, n) if rise else np.linspace(1, 0, n)
    env = _fade_env(n, int(SR * 0.05), int(SR * 0.15)) * (0.4 + 0.6 * np.sin(np.pi * sweep_shape))
    return band * env * vol


def chime(freq=880, duration=0.8, vol=0.4):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sig = (
        np.sin(2 * np.pi * freq * t)
        + 0.5 * np.sin(2 * np.pi * freq * 2 * t)
        + 0.25 * np.sin(2 * np.pi * freq * 3 * t)
    )
    env = np.exp(-t * 3.2) * _fade_env(n, int(SR * 0.005), int(SR * 0.05))
    return sig * env * vol / 1.75


def lowtone(freq=140, duration=0.8, vol=0.35):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 0.5 * t)
    env = np.exp(-t * 2.2) * _fade_env(n, int(SR * 0.02), int(SR * 0.2))
    return sig * env * vol


def swell(freq=220, duration=1.2, vol=0.3):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * freq * t) + 0.6 * np.sin(2 * np.pi * (freq * 1.5) * t)
    env = _fade_env(n, int(SR * duration * 0.35), int(SR * duration * 0.55))
    return sig * env * vol


def alert(freq=310, duration=0.3, vol=0.32):
    n = int(SR * duration)
    t = np.arange(n) / SR
    sig = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5 + np.sin(2 * np.pi * freq * t) * 0.5
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 18 * t)
    env = _fade_env(n, int(SR * 0.01), int(SR * 0.08))
    return sig * trem * env * vol


def resolve(vol=0.38):
    a = chime(660, 0.22, vol)
    b = chime(880, 0.5, vol)
    gap = np.zeros(int(SR * 0.06))
    return np.concatenate([a, gap, b])


def zip_sound(duration=0.3, vol=0.35):
    n = int(SR * duration)
    t = np.arange(n) / SR
    freq = 300 + 2600 * (t / duration)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    sig = np.sin(phase)
    env = _fade_env(n, int(SR * 0.01), int(SR * 0.15))
    return sig * env * vol


CUES = [
    (0.3, whoosh, {}),
    (7.2, pop, {"freq": 500}),
    (9.9, swell, {"freq": 200, "duration": 1.0, "vol": 0.28}),
    (14.1, chime, {"freq": 880}),
    (18.7, swell, {"freq": 180, "duration": 1.3, "vol": 0.24}),
    (22.3, lowtone, {"freq": 140, "duration": 0.8}),
    (27.0, chime, {"freq": 660, "duration": 0.9}),
    (28.7, pop, {"freq": 550}),
    (31.7, whoosh, {}),
    (34.7, tick, {}),
    (38.7, whoosh, {}),
    (41.7, tick, {}),
    (45.7, whoosh, {}),
    (48.7, tick, {}),
    (52.7, whoosh, {}),
    (55.7, tick, {}),
    (60.3, tick, {}), (60.6, tick, {}), (60.87, tick, {}), (61.13, tick, {}),
    (61.4, tick, {}), (61.67, tick, {}), (61.93, tick, {}), (62.2, tick, {}), (62.47, tick, {}),
    (66.7, whoosh, {}),
    (68.6, alert, {"freq": 300}),
    (73.7, whoosh, {}),
    (80.8, alert, {"freq": 320}),
    (83.6, resolve, {}),
    (87.9, pop, {"freq": 700}),
    (93.3, whoosh, {}),
    (96.4, tick, {}),
    (100.8, zip_sound, {}),
    (105.7, swell, {"freq": 220, "duration": 1.0, "vol": 0.26}),
    (106.3, swell, {"freq": 260, "duration": 1.0, "vol": 0.26}),
    (110.7, swell, {"freq": 200, "duration": 1.5, "vol": 0.26}),
    (116.0, whoosh, {}),
    (123.0, swell, {"freq": 220, "duration": 1.2, "vol": 0.26}),
    (128.1, chime, {"freq": 784, "duration": 1.0}),
    (128.5, swell, {"freq": 260, "duration": 1.5, "vol": 0.26}),
]

for t, fn, kwargs in CUES:
    _place(fn(**kwargs), t)

peak = np.max(np.abs(master))
if peak > 0:
    master = master / peak * 0.85

stereo = np.stack([master, master], axis=1)
pcm16 = (stereo * 32767).astype(np.int16)

script_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(script_dir, "..", "out")
wav_path = os.path.join(out_dir, "sfx.wav")
wavfile.write(wav_path, SR, pcm16)
print(f"Wrote {wav_path}")

video_in = os.path.join(out_dir, "ParabyIntro.mp4")
video_out = os.path.join(out_dir, "ParabyIntro_sound.mp4")
subprocess.run(
    [
        "ffmpeg", "-y",
        "-i", video_in,
        "-i", wav_path,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        video_out,
    ],
    check=True,
)
print(f"Wrote {video_out}")
