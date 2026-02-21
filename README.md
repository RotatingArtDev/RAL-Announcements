# RAL-Announcements

This is the Announcement repo of Rotating Art Launcher

## Helper Scripts

Use `scripts/announcement_manager.py` to manage announcements.

Install dependency:

```bash
python3 -m pip install prompt_toolkit
```

Show commands:

```bash
python3 scripts/announcement_manager.py --help
```

Open interactive action menu:

```bash
python3 scripts/announcement_manager.py
```

Run command-specific flows:

```bash
python3 scripts/announcement_manager.py create
python3 scripts/announcement_manager.py rebuild
python3 scripts/announcement_manager.py validate
```

`create` is interactive and accepts optional defaults:

```bash
python3 scripts/announcement_manager.py create \
  --title-zh "公告标题" \
  --tags launcher,announcement
```

Tags are selected via an interactive checkbox checklist of available tags (Up/Down to move, Space to toggle, Enter to confirm), with an extra "Custom tags" choice that prompts for comma-separated values.
