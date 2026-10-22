
#!/usr/bin/env python3
"""Measure audio energy and pause candidates; never infer words or subtitle times."""

import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import wave


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def measure(wav_path, threshold_db, min_pause):
    values, pauses = [], []
    low_start = None
    with wave.open(str(wav_path), 'rb') as f:
        rate = f.getframerate()
        if f.getnchannels() != 1 or f.getsampwidth() != 2:
            raise ValueError('Expected decoded mono PCM16')
        total = f.getnframes() / rate
        if total <= 0:
            raise ValueError('Audio is empty')
        cursor = 0
        while True:
            raw = f.readframes(round(rate * .02))
            if not raw:
                break
            samples = array.array('h', raw)
            if sys.byteorder != 'little':
                samples.byteswap()
            start, end = cursor / rate, (cursor + len(samples)) / rate
            cursor += len(samples)
            rms = math.sqrt(sum(x * x for x in samples) / len(samples)) / 32768
            db = max(-120., 20 * math.log10(max(rms, 1e-6)))
            values.append({'start': start, 'end': end, 'rms_dbfs': round(db, 3)})
            if db <= threshold_db:
                if low_start is None:
                    low_start = start
            elif low_start is not None:
                if start - low_start + 1e-9 >= min_pause:
                    pauses.append({'start': low_start, 'end': start})
                low_start = None
        if low_start is not None and total - low_start + 1e-9 >= min_pause:
            pauses.append({'start': low_start, 'end': total})
    return total, values, pauses


def svg(total, values, pauses):
    width, left, right = 1200, 60, 1180
    x = lambda t: left + (right - left) * t / total
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280">',
             '<rect width="1200" height="280" fill="#10202d"/>',
             '<g font-family="sans-serif" font-size="14" fill="#e5edf3">',
             '<text x="60" y="24">Audio energy and low-energy candidates — NOT speech boundaries</text>']
    for pause in pauses:
        parts.append(f'<rect x="{x(pause["start"]):.2f}" y="42" width="{x(pause["end"])-x(pause["start"]):.2f}" height="170" fill="#c99b4b" opacity=".25"/>')
    for db in (0, -20, -40, -60, -80):
        y = 42 + -db / 80 * 170
        parts.append(f'<path d="M60 {y}H1180" stroke="#344a58"/><text x="4" y="{y+5}">{db}</text>')
    # Retain the maximum energy per display bin; measurements remain in JSON.
    bins = [-120.] * (right-left)
    for v in values:
        first = min(len(bins)-1, int(v['start'] / total * len(bins)))
        last = min(len(bins), math.ceil(v['end'] / total * len(bins)))
        for idx in range(first, max(first+1, last)):
            bins[idx] = max(bins[idx], v['rms_dbfs'])
    points = ' '.join(f'{left+i},{42 + min(80,max(0,-db))/80*170:.2f}' for i,db in enumerate(bins))
    parts.append(f'<polyline points="{points}" fill="none" stroke="#66cfca" stroke-width="1.5"/>')
    for i in range(9):
        t = total*i/8
        parts.append(f'<text x="{x(t):.2f}" y="236" text-anchor="middle">{t:.2f}s</text>')
    parts.append('<text x="60" y="266">20 ms RMS windows, dBFS; confirm every word boundary by listening.</text></g></svg>')
    return '\n'.join(parts)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audio', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--threshold-db', type=float, default=-38., help='Low-energy threshold in dBFS; not a speech classifier')
    p.add_argument('--min-pause', type=float, default=.12, help='Minimum candidate duration in seconds')
    args = p.parse_args()
    try:
        if not math.isfinite(args.threshold_db) or not -120 < args.threshold_db < 0:
            raise ValueError('threshold-db must be finite and between -120 and 0')
        if not math.isfinite(args.min_pause) or args.min_pause < .02:
            raise ValueError('min-pause must be finite and at least 0.02 seconds')
        source = Path(args.audio).expanduser().resolve()
        if not source.is_file():
            raise ValueError('Input audio file does not exist')
        ffmpeg = shutil.which('ffmpeg')
        if not ffmpeg:
            raise ValueError('ffmpeg is required')
        out = Path(args.output_dir).expanduser().resolve()
        targets = [out/'candidates.json', out/'waveform.svg']
        if any(t.exists() for t in targets):
            raise ValueError('Output exists; use a new review directory')
        original_hash = digest(source)
        with tempfile.TemporaryDirectory(prefix='audio-energy-') as temp:
            decoded = Path(temp)/'review.wav'
            result = subprocess.run([ffmpeg, '-nostdin', '-v', 'error', '-n', '-i', str(source), '-map', '0:a:0', '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(decoded)], capture_output=True, text=True)
            if result.returncode:
                raise ValueError('Audio decode failed: '+result.stderr[-1600:])
            total, values, pauses = measure(decoded, args.threshold_db, args.min_pause)
        if digest(source) != original_hash:
            raise ValueError('Source changed during analysis')
        warnings = []
        if not pauses:
            warnings.append('No low-energy candidates; locate sentence boundaries by listening.')
        if all(v['rms_dbfs'] <= args.threshold_db for v in values):
            warnings.append('Entire file is below the threshold; this does not establish speech exists.')
        report = {'schema_version': 1, 'status': 'diagnostic_only', 'audio': str(source), 'audio_sha256': original_hash,
                  'duration': total, 'window_seconds': .02, 'threshold_dbfs': args.threshold_db,
                  'min_pause_seconds': args.min_pause, 'pause_candidates': pauses, 'energy': values,
                  'warnings': warnings, 'scope': 'No ASR, words, sentence boundaries, SRT or synchronization verdict. Silence and energy cannot align a transcript.'}
        out.mkdir(parents=True, exist_ok=True)
        targets[0].write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        targets[1].write_text(svg(total, values, pauses))
        print(json.dumps({'ok': True, 'status': 'diagnostic_only', 'duration': total, 'pause_candidates': len(pauses), 'files': [str(t) for t in targets], 'warnings': warnings}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, wave.Error) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())