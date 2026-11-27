"""校验 GitHub 工具箱的 registry.json 索引完整性（仅用标准库）。"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry.json"

REQUIRED_FIELDS = ("id", "name", "source", "triggers", "best_for", "install")


def main() -> int:
    errors = []
    if not REGISTRY.exists():
        print("ERROR: registry.json not found")
        return 1

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}")
        return 1

    items = data.get("items")
    if not isinstance(items, list) or not items:
        print("ERROR: 'items' must be a non-empty list")
        return 1

    seen_ids = set()
    for index, item in enumerate(items):
        for field in REQUIRED_FIELDS:
            if field not in item or not item[field]:
                errors.append(f"items[{index}]: missing field '{field}'")

        item_id = item.get("id")
        if item_id in seen_ids:
            errors.append(f"items[{index}]: duplicate id '{item_id}'")
        seen_ids.add(item_id)

        if not isinstance(item.get("triggers"), list):
            errors.append(f"items[{index}]: 'triggers' must be a list")

        if item.get("source") == "local":
            rel = item.get("path")
            if not rel:
                errors.append(f"items[{index}]: local item missing 'path'")
            elif not (ROOT / rel).exists():
                errors.append(f"items[{index}]: path not found: {rel}")
        elif item.get("source") != "marketplace":
            errors.append(f"items[{index}]: unknown source '{item.get('source')}'")

    if errors:
        print("FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(items)} registry items validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
