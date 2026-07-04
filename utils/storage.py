import asyncio
import json
import os

import config

_users_lock = asyncio.Lock()
_devices_lock = asyncio.Lock()
_filters_lock = asyncio.Lock()


def _read_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return default
        return json.loads(content)


def _write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        open(path, "a", encoding="utf-8").close()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---- users.json: list[str] ----

async def load_users() -> list[str]:
    async with _users_lock:
        return _read_json(config.USERS_FILE, [])


async def add_user(username: str) -> bool:
    """Returns False if the user already exists."""
    async with _users_lock:
        users = _read_json(config.USERS_FILE, [])
        if username in users:
            return False
        users.append(username)
        _write_json(config.USERS_FILE, users)
        return True


async def remove_user(username: str) -> bool:
    """Returns False if the user was not found."""
    async with _users_lock:
        users = _read_json(config.USERS_FILE, [])
        if username not in users:
            return False
        users.remove(username)
        _write_json(config.USERS_FILE, users)
        return True


# ---- devices.json: list[dict] ----
# each device: {"name": str, "ip": str, "port": int}
# SSH credentials are not stored per-device; see SSH_DEFAULT_* in config.py

async def load_devices() -> list[dict]:
    async with _devices_lock:
        return _read_json(config.DEVICES_FILE, [])


async def get_device(name: str) -> dict | None:
    devices = await load_devices()
    for device in devices:
        if device["name"] == name:
            return device
    return None


async def add_device(device: dict) -> bool:
    """Returns False if a device with the same name already exists."""
    async with _devices_lock:
        devices = _read_json(config.DEVICES_FILE, [])
        if any(d["name"] == device["name"] for d in devices):
            return False
        devices.append(device)
        _write_json(config.DEVICES_FILE, devices)
        return True


async def remove_device(name: str) -> bool:
    """Returns False if the device was not found."""
    async with _devices_lock:
        devices = _read_json(config.DEVICES_FILE, [])
        remaining = [d for d in devices if d["name"] != name]
        if len(remaining) == len(devices):
            return False
        _write_json(config.DEVICES_FILE, remaining)
        return True


# ---- filters.json: dict[str, list[str]] ----
# maps a process owner (username) to the list of process names hidden for them

async def load_filters() -> dict[str, list[str]]:
    async with _filters_lock:
        return _read_json(config.FILTERS_FILE, {})


async def get_user_filter(username: str) -> list[str]:
    filters = await load_filters()
    return filters.get(username, [])


async def add_filter(username: str, name: str) -> bool:
    """Returns False if the name is already filtered for this user."""
    async with _filters_lock:
        filters = _read_json(config.FILTERS_FILE, {})
        names = filters.setdefault(username, [])
        if name in names:
            return False
        names.append(name)
        _write_json(config.FILTERS_FILE, filters)
        return True


async def remove_filter(username: str, name: str) -> bool:
    """Returns False if the name was not filtered for this user."""
    async with _filters_lock:
        filters = _read_json(config.FILTERS_FILE, {})
        names = filters.get(username, [])
        if name not in names:
            return False
        names.remove(name)
        if names:
            filters[username] = names
        else:
            filters.pop(username, None)
        _write_json(config.FILTERS_FILE, filters)
        return True
