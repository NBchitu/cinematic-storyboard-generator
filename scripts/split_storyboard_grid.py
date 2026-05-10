#!/usr/bin/env python3
"""Split a 3x3 storyboard sheet into nine ordered storyboard frames."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import NamedTuple

from PIL import Image


class Ratio(NamedTuple):
    width: int
    height: int


def parse_ratio(value: str | None) -> Ratio | None:
    if value is None:
        return None
    parts = value.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Aspect ratio must look like 16:9")
    width = int(parts[0])
    height = int(parts[1])
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("Aspect ratio values must be positive")
    return Ratio(width=width, height=height)


def center_crop_to_ratio(box: tuple[int, int, int, int], ratio: Ratio) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    target = ratio.width / ratio.height
    current = width / height

    if abs(current - target) < 0.001:
        return box

    if current > target:
        new_width = round(height * target)
        offset = (width - new_width) // 2
        return (left + offset, top, left + offset + new_width, bottom)

    new_height = round(width / target)
    offset = (height - new_height) // 2
    return (left, top + offset, right, top + offset + new_height)


def split_grid(
    input_path: Path,
    output_dir: Path,
    *,
    sheet_index: int,
    start_index: int,
    prefix: str,
    aspect_ratio: Ratio | None,
    image_format: str,
) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    with Image.open(input_path) as image:
        source = image.convert("RGBA")
        width, height = source.size

        for row in range(3):
            for col in range(3):
                panel_index = row * 3 + col + 1
                shot_index = start_index + panel_index - 1
                box = (
                    round(col * width / 3),
                    round(row * height / 3),
                    round((col + 1) * width / 3),
                    round((row + 1) * height / 3),
                )
                crop_box = center_crop_to_ratio(box, aspect_ratio) if aspect_ratio else box
                frame = source.crop(crop_box)

                extension = image_format.lower()
                filename = f"{prefix}_{shot_index:03d}_s{sheet_index:02d}_p{panel_index:02d}.{extension}"
                output_path = output_dir / filename
                save_image = frame.convert("RGB") if extension in {"jpg", "jpeg"} else frame
                save_image.save(output_path)

                manifest.append(
                    {
                        "shot_index": shot_index,
                        "sheet_index": sheet_index,
                        "panel_index": panel_index,
                        "row": row + 1,
                        "column": col + 1,
                        "source": str(input_path),
                        "output": str(output_path),
                        "crop_box": crop_box,
                        "size": list(frame.size),
                    }
                )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a 3x3 storyboard sheet into nine frames.")
    parser.add_argument("input", type=Path, help="Path to the 3x3 storyboard sheet image.")
    parser.add_argument("--output-dir", type=Path, help="Output directory. Defaults to <image-stem>_shots.")
    parser.add_argument("--sheet-index", type=int, default=1, help="Storyboard sheet number, starting at 1.")
    parser.add_argument("--start-index", type=int, default=1, help="First global shot number for this sheet.")
    parser.add_argument("--prefix", default="shot", help="Filename prefix.")
    parser.add_argument(
        "--aspect-ratio",
        type=parse_ratio,
        help="Optional center-crop ratio for each frame, such as 16:9, 9:16, or 2.39:1.",
    )
    parser.add_argument("--format", choices=["png", "jpg", "jpeg", "webp"], default="png", help="Output format.")
    args = parser.parse_args()

    input_path = args.input.expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input image does not exist: {input_path}")

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = input_path.with_name(f"{input_path.stem}_shots")
    output_dir = output_dir.expanduser().resolve()

    manifest = split_grid(
        input_path,
        output_dir,
        sheet_index=args.sheet_index,
        start_index=args.start_index,
        prefix=args.prefix,
        aspect_ratio=args.aspect_ratio,
        image_format=args.format,
    )
    print(json.dumps({"output_dir": str(output_dir), "frames": len(manifest)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
