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


# ---- users.json: dict[dc_id, dict[device, {"username", "password"}]] ----
# per-(Discord user, device) SSH login used to query only that person's own
# processes on that device, instead of one shared identity for everyone.

async def get_user_credential(dc_id: str, device: str) -> dict | None:
    async with _users_lock:
        users = _read_json(config.USERS_FILE, {})
        return users.get(dc_id, {}).get(device)


async def list_user_credentials(dc_id: str) -> dict[str, dict]:
    """Returns {device: {"username": str}} for this Discord user (no passwords)."""
    async with _users_lock:
        users = _read_json(config.USERS_FILE, {})
        return {
            device: {"username": cred["username"]}
            for device, cred in users.get(dc_id, {}).items()
        }


async def set_user_credential(dc_id: str, device: str, username: str, password: str) -> bool:
    """Returns True if this is a new registration, False if it overwrote an existing one."""
    async with _users_lock:
        users = _read_json(config.USERS_FILE, {})
        devices = users.setdefault(dc_id, {})
        is_new = device not in devices
        devices[device] = {"username": username, "password": password}
        _write_json(config.USERS_FILE, users)
        return is_new


async def remove_user_credential(dc_id: str, device: str) -> bool:
    """Returns False if there was no registration for this (dc_id, device)."""
    async with _users_lock:
        users = _read_json(config.USERS_FILE, {})
        devices = users.get(dc_id, {})
        if device not in devices:
            return False
        del devices[device]
        if not devices:
            users.pop(dc_id, None)
        _write_json(config.USERS_FILE, users)
        return True


# ---- devices.json: list[dict] ----
# each device: {"name": str, "ip": str, "port": int}
# SSH credentials are not stored here — see users.json, keyed per (Discord user, device)

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
