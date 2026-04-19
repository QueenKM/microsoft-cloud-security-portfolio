#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an animated GIF from an ordered set of image frames."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing ordered frame images.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Target GIF file path.",
    )
    parser.add_argument(
        "--duration-ms",
        type=int,
        default=700,
        help="Frame duration in milliseconds.",
    )
    parser.add_argument(
        "--pause-last-ms",
        type=int,
        default=1400,
        help="Extra pause duration for the last frame in milliseconds.",
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=0,
        help="GIF loop count. Use 0 for infinite loop.",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1400,
        help="Resize frames down to this width while preserving aspect ratio.",
    )
    return parser.parse_args()


def iter_frames(input_dir: Path) -> Iterable[Path]:
    patterns = ("*.png", "*.jpg", "*.jpeg", "*.webp")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(sorted(input_dir.glob(pattern)))
    return sorted(files)


def resize_frame(image: Image.Image, max_width: int) -> Image.Image:
    if image.width <= max_width:
        return image.convert("P", palette=Image.ADAPTIVE)
    scale = max_width / image.width
    size = (max_width, max(1, int(image.height * scale)))
    return image.resize(size, Image.LANCZOS).convert("P", palette=Image.ADAPTIVE)


def main() -> int:
    args = parse_args()
    frames = list(iter_frames(args.input_dir))
    if not frames:
        raise SystemExit(f"No frame images found in {args.input_dir}")

    images: list[Image.Image] = []
    durations: list[int] = []

    for frame_path in frames:
        with Image.open(frame_path) as image:
            images.append(resize_frame(image, args.max_width))
            durations.append(args.duration_ms)

    durations[-1] = max(args.duration_ms, args.pause_last_ms)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        args.output,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=args.loop,
        optimize=True,
        disposal=2,
    )
    print(f"Created {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
