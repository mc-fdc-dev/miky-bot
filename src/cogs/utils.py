from aiomysql import Pool
from cryptography.fernet import Fernet

from os import getenv


fernet = Fernet(getenv("SECRETKEY").encode())


async def get_userdata(user_id: int, pool: Pool) -> tuple[str, str] | None:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT host, token FROM User WHERE id = %s", (user_id,))
            data = await cur.fetchone()
            if data:
                return (data[0], fernet.decrypt(data[1].encode()).decode())
