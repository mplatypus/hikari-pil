import os, dotenv

import hikari, lightbulb

import asyncio, functools

import images

import io

import random

import aiofiles

from datetime import datetime

dotenv.load_dotenv(".env")

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN", ""),
    banner=None,
)


def test_executor(id: int) -> int:
    return id * 2

@bot.command
@lightbulb.command("join", "generate a join banner of you!")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.Context) -> None:
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    start = datetime.now()

    async with ctx.author.display_avatar_url.stream() as stream:
        data = await stream.read()

    current = datetime.now()

    time_in_sec = (current - start).total_seconds()

    print("streamed data in: " + str(time_in_sec))

    file_name = "temp_pfp_" + str(random.randint(0, 9999)).zfill(4)

    new_start = datetime.now()

    async with aiofiles.open("images_storage/pfp_images/" + file_name + ".png", "wb") as file:
        await file.write(data)

    current = datetime.now()

    time_in_sec = (current - new_start).total_seconds()

    print("saved data in: " + str(time_in_sec))

    new_start = datetime.now()

    member_count: int = 0
    if ctx.guild_id != None:
        member_count = len(await bot.rest.fetch_members(ctx.guild_id))

    banner_data = images.bannerData(
        banner_type=images.bannerType.JOIN,
        username=ctx.author.username,
        user_descriminator=ctx.author.discriminator,
        pfp_file_name=file_name,
        member_count=member_count
    )

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(None, functools.partial(images.banner_create, data=banner_data))

    current = datetime.now()

    time_in_sec = (current - new_start).total_seconds()

    time_in_sec = (current - start).total_seconds()

    print("created and saved image in: " + str(time_in_sec))
    
    if result != None and result.strip() != "":
        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            "Here you go! took `" + str(time_in_sec * 1000) + "`ms or `" + str(time_in_sec) + "`s",
            attachment=hikari.File(f"images_storage/join_banners/{result}.png"),
        )
    
    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
        "Something went wrong.",
    )




if __name__ == "__main__":
    bot.run()