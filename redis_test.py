import asyncio
import os
import json
import time

from typing import Any, Iterable, Optional

try:
    import valkey.asyncio as valkey
except ImportError:
    valkey = None


class GlobalTTLCache:
    def __init__(
        self,
        ttl: float,
        maxsize: int = 200_000,
        *,
        connection_string: Optional[str] = None,
        prefix: str = "idLoaderCache:",
        decode_responses: bool = True,
    ):
        self.ttl = ttl
        self.maxsize = maxsize
        self.prefix = prefix

        self._use_valkey = connection_string is not None and valkey is not None

        # --- Valkey backend ---
        if self._use_valkey:
            self._client = valkey.from_url(
                connection_string,
                decode_responses=decode_responses,
            )
        else:
            self._client = None

        # --- In-memory backend ---
        self._data = {}
        self._lock = asyncio.Lock()

    # ========================
    # Helpers
    # ========================

    def _now(self):
        return time.time()

    def _full_key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    def _serialize(self, value: Any) -> str:
        return json.dumps(value, separators=(",", ":"), ensure_ascii=False)

    def _deserialize(self, raw: str) -> Any:
        return json.loads(raw)

    # ========================
    # Public API
    # ========================

    async def get_many(self, keys: Iterable[str]) -> dict[str, Any]:
        keys = list(keys)
        if not keys:
            return {}

        # --- Valkey path ---
        if self._use_valkey:
            full_keys = [self._full_key(k) for k in keys]
            values = await self._client.mget(full_keys)

            return {
                k: self._deserialize(v)
                for k, v in zip(keys, values)
                if v is not None
            }

        # --- In-memory path ---
        now = self._now()
        hit = {}

        async with self._lock:
            for k in keys:
                item = self._data.get(k)
                if not item:
                    continue

                exp, val = item
                if exp <= now:
                    self._data.pop(k, None)
                    continue

                hit[k] = val

        return hit

    async def set_many(self, mapping: dict[str, Any]) -> None:
        if not mapping:
            return

        # --- Valkey path ---
        if self._use_valkey:
            ttl_seconds = max(1, int(self.ttl))

            async with self._client.pipeline(transaction=False) as pipe:
                for key, value in mapping.items():
                    await pipe.set(
                        self._full_key(key),
                        self._serialize(value),
                        ex=ttl_seconds,
                    )
                await pipe.execute()
            return

        # --- In-memory path ---
        now = self._now()

        async with self._lock:
            if len(self._data) > self.maxsize:
                self._data.clear()

            exp = now + self.ttl
            for k, v in mapping.items():
                self._data[k] = (exp, v)

    async def invalidate(self, key: str) -> None:
        # --- Valkey ---
        if self._use_valkey:
            await self._client.delete(self._full_key(key))
            return

        # --- Memory ---
        async with self._lock:
            self._data.pop(key, None)

    async def invalidate_many(self, keys: Iterable[str]) -> None:
        keys = list(keys)
        if not keys:
            return

        # --- Valkey ---
        if self._use_valkey:
            await self._client.delete(*[self._full_key(k) for k in keys])
            return

        # --- Memory ---
        async with self._lock:
            for k in keys:
                self._data.pop(k, None)

    async def close(self) -> None:
        if self._use_valkey and self._client:
            await self._client.aclose()

################################################################
async def expensive_fetch(user_id: int):
    print(f"→ fetch z DB pro user {user_id}")
    await asyncio.sleep(1)
    return {
        "id": user_id,
        "score": user_id * 10,
        "ts": time.time(),
    }


async def get_users(cache, user_ids):
    keys = [f"user:{uid}" for uid in user_ids]

    cached = await cache.get_many(keys)

    missing = [uid for uid in user_ids if f"user:{uid}" not in cached]

    if missing:
        print("MISS pro:", missing)

        # paralelní fetch
        results = await asyncio.gather(
            *(expensive_fetch(uid) for uid in missing)
        )

        mapping = {
            f"user:{uid}": value
            for uid, value in zip(missing, results)
        }

        await cache.set_many(mapping)

        cached.update(mapping)

    return cached

async def worker(cache, wid):
    print(f"\n[worker {wid}] start")
    data = await get_users(cache, [1, 2, 3])
    print(f"[worker {wid}] done")
    return data


async def test_concurrency(cache):
    print("\n=== CONCURRENCY TEST ===")

    start = time.time()

    await asyncio.gather(
        *(worker(cache, i) for i in range(5))
    )

    end = time.time()

    print(f"\nCelkový čas: {end - start:.2f}s")


async def test_invalidate(cache):
    print("\n=== INVALIDATE TEST ===")

    await cache.set_many({
        "user:99": {"name": "ToDelete"}
    })

    print("before:", await cache.get_many(["user:99"]))

    await cache.invalidate("user:99")

    print("after:", await cache.get_many(["user:99"]))


async def main():
    cache = GlobalTTLCache(
        ttl=5,
        connection_string= os.environ.get("valkey://localhost:31123/0"),
    )

    try:
        await test_concurrency(cache)
        await test_invalidate(cache)
    finally:
        await cache.close()


if __name__ == "__main__":
    asyncio.run(main())