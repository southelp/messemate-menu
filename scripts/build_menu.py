#!/usr/bin/env python3
"""Build the static customer menu from the captured Mailbean product export."""
from __future__ import annotations

import json
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path.home() / "Downloads" / "mailbean-menu-products.json"
IMAGE_DIR = ROOT / "assets" / "menu"
OUTPUT = ROOT / "menu-data.js"


def main() -> None:
    source_items = json.loads(SOURCE.read_text(encoding="utf-8"))
    visible_items = [item for item in source_items if item["shown"]]
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    output_items = []
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; StarChorongCafeMenu/1.0)"

    for item in visible_items:
        image_name = f'{item["order"]:02d}-{item["id"]}.webp'
        image_path = IMAGE_DIR / image_name
        if not image_path.exists():
            response = session.get(item["image"], timeout=30, allow_redirects=True)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise RuntimeError(f'{item["name"]}: expected image, got {content_type}')

            source_path = IMAGE_DIR / f'.{item["id"]}-source'
            source_path.write_bytes(response.content)
            with Image.open(source_path) as image:
                image.thumbnail((720, 900), Image.Resampling.LANCZOS)
                image.save(image_path, "WEBP", quality=84, method=6)
            source_path.unlink()

        output_items.append(
            {
                "order": item["order"],
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "category": item["category"],
                "image": f"assets/menu/{image_name}",
                "soldout": item["soldout"],
            }
        )

    data = json.dumps(output_items, ensure_ascii=False, separators=(",", ":"))
    OUTPUT.write_text(f"window.MENU_ITEMS={data};\n", encoding="utf-8")
    print(f"built_items={len(output_items)}")
    print(f"downloaded_images={len(list(IMAGE_DIR.iterdir()))}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
