from PIL import ImageDraw, Image, ImageFilter, ImageOps, ImageEnhance, ImageFont

import PIL

import random, asyncio

import io

<<<<<<< Updated upstream
class bannerType:
    JOIN = 1
    LEAVE = 0
=======

class bannerType(int, enum.Enum):
    JOIN = 0
    LEAVE = 1
    LEVEL = 2
>>>>>>> Stashed changes


def background_create(colour: str) -> Image:
    base_image = Image.open("./images/default_background.png")

    base_image = base_image.convert("RGBA")
    base_image = base_image.resize((1024, 415))

    # Create a new image with the same size as the base image and fill it with the target color
    color_image = Image.new(
        "RGBA", base_image.size, colour
    )  # Ensure it matches the size of the base_image

    # Blend the two images
    blended_image = Image.blend(
        base_image, color_image, alpha=0.5
    )  # Adjust the alpha value as needed

    enhancer = ImageEnhance.Brightness(blended_image)

    brightness_factor = 1.25
    brightened_image = enhancer.enhance(brightness_factor)

    return brightened_image


def round_corners(image: Image, radius: int) -> Image:
    circle = Image.new("L", (radius * 2, radius * 2), "BLACK")
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    # Create a new RGBA image with a transparent background
    alpha = Image.new("L", image.size, 255)
    w, h = image.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(
        circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius)
    )

    rgba_image = image  # .convert("RGBA")

    rgba_image.putalpha(alpha)

    return rgba_image


class bannerData:
    def __init__(
        self,
        *,
        banner_type: bannerType | int,
        username: str,
        user_descriminator: str | None = None,
        pfp_bytes: bytes,
        member_count: int,
    ) -> None:
        self._banner_type: bannerType | int = banner_type
        self._username: str = username
        self._user_descriminator: str | None = user_descriminator
        self._pfp_bytes: bytes = pfp_bytes
        self._member_count: int = member_count

    @property
    def banner_type(self) -> bannerType | int:
        return self._banner_type

    @property
    def username(self) -> str:
        return self._username

    @property
    def user_descriminator(self) -> str | None:
        return self._user_descriminator

    @property
    def pfp_bytes(self) -> bytes:
        return self._pfp_bytes

    @property
    def member_count(self) -> int:
        return self._member_count
    
    
    




# This is only for Joins and Leaving.
def banner_create(data: bannerData) -> None | bytes:
    base_image: Image

    banner_message = ""
    if data.banner_type == bannerType.JOIN:
        base_image = background_create("GREEN")
        banner_message = "Welcome,"
    elif data.banner_type == bannerType.LEAVE:
        base_image = background_create("RED")
        banner_message = "Leave,"
    else:
        return
    
    draw = ImageDraw.Draw(base_image)

    padding = 25  # default is 25, anything else may result in errors, or problems.

    rectangle_coordinates = [
        padding,
        padding,
        base_image.size[0] - padding,
        base_image.size[1] - padding,
    ]

    draw.rectangle(rectangle_coordinates, outline="BLACK", fill="BLACK")

    profile_image = Image.open(io.BytesIO(data.pfp_bytes))

    profile_image = profile_image.resize(
        (base_image.size[1] - (padding * 4), base_image.size[1] - (padding * 4))
    )
    profile_image = profile_image.convert("RGBA")

    profile_image.putalpha(255)

    profile_image = round_corners(profile_image, int(profile_image.size[0] / 2))

    image_copy = base_image.copy()  #type: ignore | error is with .copy, it will exist.

    image_copy.paste(profile_image, (padding * 2, padding * 2))

    # following code is for text.

    draw = ImageDraw.Draw(image_copy)

    font_large = ImageFont.truetype(
        "images/fonts/main_font.ttf", int((image_copy.size[1] - (padding * 4)) / 5)
    )
    font_small = ImageFont.truetype(
        "images/fonts/main_font.ttf", int((image_copy.size[1] - (padding * 4)) / 7)
    )

    max_chars = 22


    print(data.user_descriminator)
    print(type(data.user_descriminator))
    if (
        data.user_descriminator != None
        and data.user_descriminator != ""
        and data.user_descriminator != "0"
    ):
        user_name = user_name + "#" + data.user_descriminator

    if len(user_name) >= max_chars:
        max_chars -= 2
        user_name = user_name[:max_chars] + "..."

    if data.banner_type == bannerType.JOIN or data.banner_type == bannerType.LEAVE:
        draw.text(
            ((padding * 3) + profile_image.size[0], padding * 2),
            banner_message,
            "WHITE",
            font_large,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 3) + profile_image.size[0],
                int(padding * 2 + int(padding / 2 * 2) + font_large.size),
            ),
            user_name,
            "WHITE",
            font_small,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 3) + profile_image.size[0],
                int(
                    padding * 2
                    + int(padding / 2 * 3)
                    + font_large.size
                    + font_small.size
                ),
            ),
            "We now have " + str(data.member_count) + " members.",
            "WHITE",
            font_small,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 3) + profile_image.size[0],
                int(
                    padding * 2
                    + int(padding / 2 * 3)
                    + font_large.size
                    + (font_small.size * 2)
                ),
            ),
            "_",
            "WHITE",
            font_large,
        )  # type: ignore | error is with .size, it will exist.

    elif data.banner_type == bannerType.LEVEL:
        draw.text(
            ((padding * 3) + profile_image.size[0], padding * 2),
            user_name,
            "WHITE",
            font_large,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 3) + profile_image.size[0],
                int(padding * 2 + int(padding / 2 * 2) + font_large.size),
            ),
            "Current level:",
            "WHITE",
            font_small,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 13) + profile_image.size[0],
                int(padding * 2 + int(padding / 2 * 2) + font_large.size),
            ),
            "@Apple",
            "YELLOW",
            font_small,
        )  # type: ignore | error is with .size, it will exist.
        draw.text(
            (
                (padding * 3) + profile_image.size[0],
                int(
                    padding * 2
                    + int(padding / 2 * 3)
                    + font_large.size
                    + font_small.size
                ),
            ),
            "Next level:",
            "WHITE",
            font_small,
        )
        draw.text(
            (
                (padding * 13) + profile_image.size[0],
                int(
                    padding * 2
                    + int(padding / 2 * 3)
                    + font_large.size
                    + font_small.size
                ),
            ),
            "@Banana",
            "MAGENTA",
            font_small,
        )  # type: ignore | error is with .size, it will exist.

        start_x_y = (
            (padding * 3) + profile_image.size[0],
            int(
                padding * 2
                + int(padding / 2 * 3)
                + font_large.size
                + (font_small.size * 2)
                + (padding * 2)
            ),
        )
        end_x_y = (image_copy.size[0] - (padding * 2), start_x_y[1] + (padding * 2))
        main_x_y = (start_x_y, end_x_y)

        draw.rectangle(main_x_y, "GRAY")

        random_percentage = random.randint(0, 1000)

        random_percentage = 500

        end_pos = (
            (random_percentage / 1000) * (end_x_y[0] - start_x_y[0])
        ) + start_x_y[0]

        end_progress_x_y = (end_pos, end_x_y[1])
        progress_x_y = (start_x_y, end_progress_x_y)

        draw.rectangle(progress_x_y, "WHITE")

    img_byte_array = io.BytesIO()

    image_copy.save(img_byte_array, format="PNG")

    return img_byte_array.getvalue()
