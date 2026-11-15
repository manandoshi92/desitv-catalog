import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "episodes.json"
OUTPUT = ROOT / "docs" / "catalog.json"

CHANNELS = [
    "Star Plus", "Colors TV", "Zee TV", "Sony TV",
    "SAB TV", "Dangal TV", "Star Jalsha", "JioHotstar"
]

def valid_url(value):
    return value is None or (
        isinstance(value, str) and
        value.startswith("https://")
    )

data = json.loads(SOURCE.read_text(encoding="utf-8"))
episodes = {}
for ep in data["episodes"]:
    for key in ("id", "channel", "show", "title", "releaseDate"):
        if not isinstance(ep.get(key), str) or not ep[key]:
            raise ValueError(f"Missing or invalid {key}: {ep}")
    if ep["channel"] not in CHANNELS:
        raise ValueError(f"Unknown channel: {ep['channel']}")
    datetime.strptime(ep["releaseDate"], "%Y-%m-%d")
    for key in ("thumbnail", "pageUrl", "streamUrl"):
        if not valid_url(ep.get(key)):
            raise ValueError(f"Invalid {key}: {ep['id']}")
    episodes[ep["id"]] = ep

ordered = sorted(
    episodes.values(),
    key=lambda ep: (ep["releaseDate"], ep["id"]),
    reverse=True
)

catalog = {
    "version": 1,
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "channels": CHANNELS,
    "episodes": ordered
}

OUTPUT.write_text(
    json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)
print(f"Published {len(ordered)} episodes")
