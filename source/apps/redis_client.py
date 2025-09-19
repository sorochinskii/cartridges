import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Self

from config import settings
from logger_config import logger

from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import RedisError


class RedisClient:
    def __init__(self, url: str, token_lifetime: int):
        self.client: Redis | None = None
        self.url = url
        self.token_lifetime = token_lifetime

    async def init_redis(self) -> Self | None:
        if self.client:
            await self.close()
        try:
            self.client = Redis.from_url(
                str(self.url),
                decode_responses=True,
            )
            await self.client.ping()

        except RedisConnectionError as e:
            logger.error(
                "Failed to establish Redis connection",
                exc_info=e,
                extra={"redis_url": self.url},
            )
            raise
        except RedisError as e:
            logger.error(f"Redis error: {e}")
            raise RuntimeError(f"Redis initialization failed: {e}") from e

        except Exception as e:
            logger.exception("Unexpected error during Redis initialization")
            raise RuntimeError("Unexpected Redis error") from e
        return self

    async def close(self):
        await self.client.close()

    async def save_refresh_token(
        self, user_id: str, refresh_token: str, user_agent: Optional[str] = None
    ):
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self.token_lifetime
        )
        token_data = {
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
            "user_agent": user_agent,
        }
        await self.client.set(
            f"refresh_token:{refresh_token}",
            json.dumps(token_data),
            ex=timedelta(seconds=self.token_lifetime),
        )
        await self.client.sadd(f"user_refresh_tokens: {user_id}", refresh_token)

    async def get_refresh_token(self, refresh_token: str) -> Optional[dict]:
        token_data = await self.client.get(f"refresh_token:{refresh_token}")
        if not token_data:
            return None
        return json.loads(token_data)

    async def delete_refresh_token(self, refresh_token: str):
        token_data = await self.get_refresh_token(refresh_token)
        if token_data:
            await self.client.delete(f"refresh_token:{refresh_token}")
            await self.client.srem(
                f"user_refresh_tokens:{token_data['user_id']}", refresh_token
            )

    async def delete_all_user_refresh_tokens(self, user_id: str):
        tokens: set[str] = await self.client.smembers(
            f"user_refresh_tokens:{user_id}"
        )
        for token in tokens:
            await self.client.delete(f"refresh_token:{token}")
        await self.client.delete(f"user_refresh_tokens:{user_id}")

    async def verify_token(self, token: str) -> int | None:
        async for key in self.client.scan_iter("tg:*"):
            if self.client.hget(key, "access") == token:
                return int(key.split(":")[1])
        return None

    async def get_user_id(self, token: str) -> int | None:
        if token is None:
            return None
        user_id = await self.client.get(f"refresh_token:{token}")
        if user_id is None:
            return None
        return user_id

    async def revoke_refresh_token(self, token: str):
        await self.client.delete(f"refresh_token:{token}")

    async def store_refresh_token(
        self, user_id: str, token: str, expires_in_days: int
    ):
        await self.client.setex(
            f"refresh_token:{token}",
            settings.REFRESH_TOKEN_LIFETIME,
            user_id,
        )


async def get_redis_client() -> RedisClient:
    redis = RedisClient(
        url=settings.REDIS_URL, token_lifetime=settings.REFRESH_TOKEN_LIFETIME
    )
    await redis.init_redis()
    return redis
