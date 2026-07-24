#!/usr/bin/env python3
"""Probe fal queue status endpoints for Banana edit job."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
RID = "019f8d9a-4691-7fc3-892c-6df929c8dfff"
EP = "fal-ai/nano-banana-pro/edit"


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def main() -> None:
    load_env()
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    urls = [
        f"https://queue.fal.run/{EP}/requests/{RID}/status",
        f"https://queue.fal.run/{EP}/requests/{RID}",
        f"https://rest.alpha.fal.ai/fal-ai/nano-banana-pro/edit/requests/{RID}/status",
    ]
    for url in urls:
        for method in ("GET", "POST"):
            req = urllib.request.Request(
                url,
                data=b"{}" if method == "POST" else None,
                headers={
                    "Authorization": f"Key {key}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                method=method,
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    body = resp.read()[:400]
                    print(method, resp.status, url)
                    print(" ", body[:300])
            except urllib.error.HTTPError as e:
                print(method, e.code, url, e.read()[:200])
            except Exception as e:
                print(method, "EXC", url, e)

    try:
        import fal_client  # type: ignore

        print("fal_client status:", fal_client.status(EP, RID, with_logs=True))
    except Exception as e:
        print("fal_client fail:", e)


if __name__ == "__main__":
    main()
