from aiomysql import Pool


async def get_userdata(user_id: int, pool: Pool) -> tuple[str, str] | None:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT host, token FROM User WHERE id = %s", (user_id,))
            return await cur.fetchone()
