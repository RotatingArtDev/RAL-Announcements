#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.shortcuts import checkboxlist_dialog
except ImportError as exc:
    print(
        "Missing dependency. Install with:\n"
        "  python3 -m pip install prompt_toolkit",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


ROOT = Path(__file__).resolve().parents[1]
ANNOUNCEMENTS_DIR = ROOT / "announcements"
INDEX_FILE = ROOT / "announcements.json"
ID_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-(\d+)$")
DEFAULT_TAGS = [
    "⭐",
    "启动器",
    "公告",
    "广告",
    ]
HAS_TTY = sys.stdin.isatty() and sys.stdout.isatty()


# ---------- Core data helpers ----------
def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=4)
        handle.write("\n")


def parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def normalize_iso8601(value: str) -> str:
    parsed = parse_iso8601(value)
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_announcement_id(announcement_id: str) -> tuple[str, int]:
    match = ID_PATTERN.fullmatch(announcement_id)
    if not match:
        raise ValueError("Announcement id must match YYYY-MM-DD-N, e.g. 2026-02-21-1")
    return match.group(1), int(match.group(2))


def sort_announcements(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (parse_iso8601(str(item.get("publishedAt", ""))), str(item.get("id", ""))),
        reverse=True,
    )


def load_index() -> dict[str, Any]:
    if not INDEX_FILE.exists():
        return {"version": 1, "announcements": []}

    data = read_json(INDEX_FILE)
    if not isinstance(data, dict):
        raise ValueError(f"{INDEX_FILE} must be a JSON object")
    if "announcements" not in data or not isinstance(data["announcements"], list):
        raise ValueError(f"{INDEX_FILE} must contain an 'announcements' list")
    if "version" not in data:
        data["version"] = 1
    return data


def next_id_for_date(date_str: str) -> str:
    max_seq = 0
    if ANNOUNCEMENTS_DIR.exists():
        for entry in ANNOUNCEMENTS_DIR.iterdir():
            if not entry.is_dir():
                continue
            match = ID_PATTERN.fullmatch(entry.name)
            if match and match.group(1) == date_str:
                max_seq = max(max_seq, int(match.group(2)))

    index = load_index()
    for item in index.get("announcements", []):
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        match = ID_PATTERN.fullmatch(item_id)
        if match and match.group(1) == date_str:
            max_seq = max(max_seq, int(match.group(2)))

    return f"{date_str}-{max_seq + 1}"


def list_manifests() -> list[Path]:
    if not ANNOUNCEMENTS_DIR.exists():
        return []
    return sorted(ANNOUNCEMENTS_DIR.glob("*/manifest.json"))


def validate_item(item: dict[str, Any], source: str) -> list[str]:
    errors: list[str] = []
    item_id = item.get("id")
    published_at = item.get("publishedAt")
    meta = item.get("meta")

    if not isinstance(item_id, str):
        errors.append(f"{source}: missing string 'id'")
    else:
        try:
            validate_announcement_id(item_id)
        except ValueError as exc:
            errors.append(f"{source}: {exc}")

    if not isinstance(published_at, str):
        errors.append(f"{source}: missing string 'publishedAt'")
    else:
        try:
            normalize_iso8601(published_at)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{source}: invalid publishedAt '{published_at}': {exc}")

    if not isinstance(meta, dict):
        errors.append(f"{source}: missing object 'meta'")
    return errors


def split_tags(raw: str) -> list[str]:
    tags = [part.strip() for part in re.split(r"[,，]", raw)]
    return [tag for tag in tags if tag]


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def available_tags() -> list[str]:
    tags = list(DEFAULT_TAGS)
    known = set(tags)
    try:
        index = load_index()
    except Exception:  # noqa: BLE001
        return tags

    for item in index.get("announcements", []):
        meta = item.get("meta")
        if not isinstance(meta, dict):
            continue
        for locale_meta in meta.values():
            if not isinstance(locale_meta, dict):
                continue
            raw_tags = locale_meta.get("tags")
            if not isinstance(raw_tags, list):
                continue
            for raw_tag in raw_tags:
                if not isinstance(raw_tag, str):
                    continue
                tag = raw_tag.strip()
                if tag and tag not in known:
                    tags.append(tag)
                    known.add(tag)
    return tags


def readme_name(locale: str) -> str:
    return f"README.{locale}.md"


def build_readme(title: str) -> str:
    return f"# {title}\n\nWrite announcement details here.\n"


# ---------- Prompt toolkit helpers ----------
def ask_text(label: str, default: str = "") -> str:
    message = f"{label}: "
    if HAS_TTY:
        return prompt(message, default=default).strip()

    if default:
        print(f"{label} [{default}]: ", end="", flush=True)
    else:
        print(message, end="", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("No input available on stdin")
    value = line.strip()
    return value if value else default


def ask_required_text(label: str, default: str = "") -> str:
    while True:
        value = ask_text(label, default=default)
        if value:
            return value
        print(f"{label} is required.", file=sys.stderr)


def ask_choice(label: str, choices: list[str], default: str) -> str:
    while True:
        if HAS_TTY:
            completer = WordCompleter(choices, ignore_case=True)
            value = prompt(f"{label}: ", default=default, completer=completer).strip()
        else:
            value = ask_text(label, default=default)
        for choice in choices:
            if value.lower() == choice.lower():
                return choice
        print(f"Choose one of: {', '.join(choices)}", file=sys.stderr)


def ask_iso8601(label: str, default: str) -> str:
    while True:
        raw = ask_text(label, default=default)
        try:
            return normalize_iso8601(raw)
        except Exception as exc:  # noqa: BLE001
            print(f"Invalid timestamp: {exc}", file=sys.stderr)


def ask_id_with_default(suggested_id: str) -> str:
    while True:
        raw = ask_text("id (leave empty for auto)", default="")
        value = raw if raw else suggested_id
        try:
            validate_announcement_id(value)
            return value
        except Exception as exc:  # noqa: BLE001
            print(f"Invalid id: {exc}", file=sys.stderr)


def ask_yes_no(label: str, default: bool = False) -> bool:
    default_raw = "y" if default else "n"
    hint = "Y/n" if default else "y/N"
    while True:
        value = ask_text(f"{label} [{hint}]", default=default_raw).strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer y or n.", file=sys.stderr)


def ask_tags(default_tags: list[str] | None = None) -> list[str]:
    known_tags = available_tags()
    known_tag_set = set(known_tags)
    custom_defaults = [tag for tag in (default_tags or []) if tag not in known_tag_set]
    selected: list[str] = []
    custom_tags: list[str] = []

    if HAS_TTY:
        values = [(f"tag:{tag}", tag) for tag in known_tags]
        values.append(("custom", "Custom tags"))

        selected_set = set(default_tags or [])
        default_values = [f"tag:{tag}" for tag in known_tags if tag in selected_set]
        if custom_defaults:
            default_values.append("custom")

        picked = checkboxlist_dialog(
            title="Select tags",
            text="Use Up/Down to move, Space to toggle, Enter to confirm.",
            values=values,
            default_values=default_values,
        ).run()
        if picked is None:
            raise ValueError("Tag selection cancelled")

        selected = [value.removeprefix("tag:") for value in picked if value.startswith("tag:")]
        if "custom" in picked:
            custom_input = ask_text("custom tags (comma-separated)", default=",".join(custom_defaults))
            custom_tags = split_tags(custom_input)
    else:
        selected_set = set(default_tags or [])
        for tag in known_tags:
            if ask_yes_no(f"Use tag '{tag}'?", default=tag in selected_set):
                selected.append(tag)

        use_custom = ask_yes_no("Add custom tags?", default=bool(custom_defaults))
        if use_custom:
            custom_input = ask_text("custom tags (comma-separated)", default=",".join(custom_defaults))
            custom_tags = split_tags(custom_input)

    tags = dedupe_keep_order(selected + custom_tags)
    if not tags:
        raise ValueError("At least one tag is required")
    return tags


# ---------- Announcement operations ----------
def create_announcement(
    title_zh: str,
    published_at: str,
    custom_id: str | None,
    tags: list[str],
) -> str:
    ANNOUNCEMENTS_DIR.mkdir(parents=True, exist_ok=True)

    published_at = normalize_iso8601(published_at)
    announcement_id = custom_id.strip() if custom_id else ""
    if announcement_id:
        validate_announcement_id(announcement_id)
    else:
        announcement_id = next_id_for_date(parse_iso8601(published_at).strftime("%Y-%m-%d"))

    if not tags:
        raise ValueError("At least one tag is required")

    index = load_index()
    if any(item.get("id") == announcement_id for item in index["announcements"]):
        raise ValueError(f"id already exists in announcements.json: {announcement_id}")

    announcement_dir = ANNOUNCEMENTS_DIR / announcement_id
    if announcement_dir.exists():
        raise ValueError(f"directory already exists: {announcement_dir}")
    announcement_dir.mkdir(parents=True, exist_ok=False)

    meta: dict[str, dict[str, object]] = {"zh-CN": {"title": title_zh.strip(), "tags": tags}}

    announcement = {"id": announcement_id, "publishedAt": published_at, "meta": meta}
    write_json(announcement_dir / "manifest.json", announcement)

    (announcement_dir / readme_name("zh-CN")).write_text(build_readme(title_zh.strip()), encoding="utf-8")

    index["announcements"].append(announcement)
    index["announcements"] = sort_announcements(index["announcements"])
    write_json(INDEX_FILE, index)

    print(f"Created announcement: {announcement_id}")
    print(f"- {announcement_dir / 'manifest.json'}")
    print(f"- {announcement_dir / readme_name('zh-CN')}")

    return announcement_id


def rebuild_index() -> None:
    manifests: list[dict[str, Any]] = []
    for path in list_manifests():
        item = read_json(path)
        if not isinstance(item, dict):
            raise ValueError(f"{path} must be a JSON object")
        errors = validate_item(item, str(path))
        if errors:
            raise ValueError(errors[0])
        item["publishedAt"] = normalize_iso8601(item["publishedAt"])
        manifests.append(item)

    existing = load_index()
    rebuilt = {"version": existing.get("version", 1), "announcements": sort_announcements(manifests)}
    write_json(INDEX_FILE, rebuilt)
    print(f"Rebuilt index: {INDEX_FILE}")
    print(f"Announcements: {len(manifests)}")


def validate_all() -> bool:
    errors: list[str] = []
    index = load_index()

    announcements = index.get("announcements", [])
    index_by_id: dict[str, dict[str, Any]] = {}
    for pos, item in enumerate(announcements, start=1):
        source = f"{INDEX_FILE} item #{pos}"
        errors.extend(validate_item(item, source))
        item_id = item.get("id")
        if isinstance(item_id, str):
            if item_id in index_by_id:
                errors.append(f"{INDEX_FILE}: duplicate id '{item_id}'")
            else:
                index_by_id[item_id] = item

    manifest_ids: set[str] = set()
    for manifest_path in list_manifests():
        item = read_json(manifest_path)
        if not isinstance(item, dict):
            errors.append(f"{manifest_path}: not a JSON object")
            continue

        errors.extend(validate_item(item, str(manifest_path)))
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        manifest_ids.add(item_id)

        if manifest_path.parent.name != item_id:
            errors.append(f"{manifest_path}: directory name does not match id")

        idx_item = index_by_id.get(item_id)
        if idx_item is None:
            errors.append(f"{manifest_path}: id missing from {INDEX_FILE}")
        else:
            left = {
                "id": idx_item.get("id"),
                "publishedAt": normalize_iso8601(str(idx_item.get("publishedAt"))),
                "meta": idx_item.get("meta"),
            }
            right = {
                "id": item.get("id"),
                "publishedAt": normalize_iso8601(str(item.get("publishedAt"))),
                "meta": item.get("meta"),
            }
            if left != right:
                errors.append(f"{manifest_path}: content mismatch with {INDEX_FILE}")

        meta = item.get("meta")
        if isinstance(meta, dict):
            for locale in meta.keys():
                if not isinstance(locale, str):
                    errors.append(f"{manifest_path}: non-string locale in meta")
                    continue
                readme = manifest_path.parent / readme_name(locale)
                if not readme.exists():
                    errors.append(f"{manifest_path}: missing {readme.name}")
                elif readme.stat().st_size == 0:
                    errors.append(f"{manifest_path}: empty {readme.name}")

    for item_id in sorted(set(index_by_id.keys()) - manifest_ids):
        errors.append(f"{INDEX_FILE}: id '{item_id}' has no matching manifest")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for issue in errors:
            print(f"- {issue}", file=sys.stderr)
        return False

    print("Validation passed.")
    print(f"Announcements indexed: {len(index_by_id)}")
    return True


# ---------- Command runners ----------
def run_create_interactive(args: argparse.Namespace) -> int:
    title_zh_default = args.title_zh or ""
    title_zh = ask_required_text("zh-CN title", default=title_zh_default)

    published_at = ask_iso8601("publishedAt (ISO8601 UTC)", default=args.published_at or utc_now_iso())
    suggested_id = next_id_for_date(parse_iso8601(published_at).strftime("%Y-%m-%d"))
    announcement_id = args.announcement_id or ask_id_with_default(suggested_id)

    tags_default = split_tags(args.tags) if args.tags is not None else []
    tags = ask_tags(default_tags=tags_default)

    create_announcement(
        title_zh=title_zh,
        published_at=published_at,
        custom_id=announcement_id,
        tags=tags,
    )
    return 0


def run_rebuild_interactive(_args: argparse.Namespace) -> int:
    rebuild_index()
    return 0


def run_validate_interactive(_args: argparse.Namespace) -> int:
    return 0 if validate_all() else 1


def interactive_menu() -> int:
    choices = ["create", "rebuild", "validate", "exit"]
    while True:
        action = ask_choice("Action (create/rebuild/validate/exit)", choices=choices, default="create")
        if action == "create":
            try:
                run_create_interactive(
                    argparse.Namespace(
                        title_zh=None,
                        published_at=None,
                        announcement_id=None,
                        tags=None,
                    )
                )
                return 0
            except Exception as exc:  # noqa: BLE001
                print(f"Error: {exc}", file=sys.stderr)
        elif action == "rebuild":
            try:
                run_rebuild_interactive(argparse.Namespace())
            except Exception as exc:  # noqa: BLE001
                print(f"Error: {exc}", file=sys.stderr)
        elif action == "validate":
            try:
                run_validate_interactive(argparse.Namespace())
            except Exception as exc:  # noqa: BLE001
                print(f"Error: {exc}", file=sys.stderr)
        else:
            return 0


# ---------- CLI ----------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Announcement manager for this repository")
    subparsers = parser.add_subparsers(dest="command")

    create = subparsers.add_parser("create", help="Create a new announcement (interactive prompts)")
    create.add_argument("--title-zh", help="Default zh-CN title shown in prompt")
    create.add_argument("--published-at", help="Default ISO8601 timestamp shown in prompt")
    create.add_argument("--id", dest="announcement_id", help="Default announcement id shown in prompt")
    create.add_argument("--tags", help="Comma-separated tags pre-selected in prompt")

    subparsers.add_parser("rebuild", help="Rebuild announcements.json")
    subparsers.add_parser("validate", help="Validate announcements")
    subparsers.add_parser("interactive", help="Open interactive action menu")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command is None or args.command == "interactive":
            return interactive_menu()

        if args.command == "create":
            return run_create_interactive(args)

        if args.command == "rebuild":
            return run_rebuild_interactive(args)

        if args.command == "validate":
            return run_validate_interactive(args)

        parser.print_help()
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
