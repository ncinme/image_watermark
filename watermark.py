from PIL import Image, ImageDraw, ImageFont


class Watermark:

    @staticmethod
    def add_text(filename, text):
        """Add text watermark to the original image"""

        filename_list = filename.split(".")

        with Image.open(filename) as im:
            # get a font
            font = ImageFont.truetype("arial.ttf", 25)

            # get a drawing context
            d = ImageDraw.Draw(im)

            # draw text
            d.text((0, 0), text=text, font=font, fill=(8, 110, 125))

            # im.show()
            # save output file
            im.save(filename_list[0] + "_watermark." + filename_list[-1])

    @staticmethod
    def add_logo(org_img, lgo_img):
        """Add logo watermark to the original image"""

        filename_list = org_img.split(".")

        with Image.open(org_img) as im1:
            with Image.open(lgo_img) as im2:
                im1.paste(im2, (0, 0))
                im1.save(filename_list[0] + "_watermark." + filename_list[-1])

    @staticmethod
    def add_logo_transparent(org_img, lgo_img):
        """Add transparent logo watermark to the original image"""

        filename_list = org_img.split(".")

        with Image.open(org_img).convert("RGBA") as im1:            # convert the image in same RGBA format, otherwise mask will not work
            with Image.open(lgo_img).convert("RGBA") as im2:
                width, height = im1.size

                transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                transparent.paste(im1, (0, 0))
                transparent.paste(im2, (0, 0), mask=im2)
                # transparent.paste(im2, (0, 0), mask=im2.split()[3])
                # transparent.paste(im2, (0, 0))

                transparent.save(filename_list[0] + "_watermark" + ".png")    # .png supports transparency

