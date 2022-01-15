# References:
# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#coordinates
# https://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/
# https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont

# Logging into a file on the server
import logging
LOG_FORMAT = "%(levelname)s %(asctime)s -- %(message)s"
logging.basicConfig(filename='watermark.log', level=logging.INFO, format=LOG_FORMAT, filemode='a')

original_img = ""
logo_img = ""


# ---------------------------- Watermark ------------------------------- #
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
        im.save(filename_list[0] + "_watermark." + filename_list[-1])


def add_logo(org_img, lgo_img):
    """Add logo watermark to the original image"""

    filename_list = org_img.split(".")

    with Image.open(org_img) as im1:
        with Image.open(lgo_img) as im2:
            im1.paste(im2, (0, 0))
            im1.save(filename_list[0] + "_watermark." + filename_list[-1])


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


# ---------------------------- Tkinter function calls ---------------------------- #
def select_file(file_type):
    """Ask the user to select the original image and logo image"""
    global original_img
    global logo_img
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if file_type == "original":
        original_img = filename
        original_entry.insert(0, filename)
    elif file_type == "logo":
        logo_img = filename
        logo_entry.insert(0, filename)
    else:
        messagebox.showinfo(title="Incorrect file", message="Select file again.")


def add_watermark():
    """Add either text or logo watermark to the original image"""
    watermark_text = text_entry.get()
    watermark_logo = logo_img
    try:
        if watermark_logo:
            # add_logo(original_img, watermark_logo)
            add_logo_transparent(original_img, watermark_logo)
            messagebox.showinfo(title="Success", message="Watermark Logo added. "
                                                         "Check the new file with _watermark name in the same folder.")

        if watermark_text:
            add_text(original_img, watermark_text)
            messagebox.showinfo(title="Success", message="Watermark Text added. "
                                                         "Check the new file with _watermark name in the same folder.")
    except OSError as err:
        messagebox.showinfo(title="Error!!", message="Error!! Please try again.")
        logging.exception(err)

    except ValueError as err:
        messagebox.showinfo(title="Error!!", message="Error!! Please try again.")
        logging.exception(err)

    except Exception as err:
        messagebox.showinfo(title="Error!!", message="Error!! Please try again.")
        logging.exception(err)

# ---------------------------- Tkinter UI SETUP ------------------------------- #

window = Tk()
window.title("Add Watermark")
window.config(padx=10, pady=20)

canvas = Canvas(height=380, width=370)
# logo_img = PhotoImage(file="logo.png")
# canvas.create_image(200, 200, image=logo_img)
# canvas.grid(row=0, column=0, columnspan=3)

# Labels
choice_label = Label(text="Enter the watermark text or logo")
choice_label.grid(row=2, column=0, columnspan=3)
original_label = Label(text="Original Image")
original_label.grid(row=4, column=1)
text_label = Label(text="Watermark Text")
text_label.grid(row=5, column=1)
logo_label = Label(text="Watermark Logo")
logo_label.grid(row=6, column=1)

# Entries
original_entry = Entry(width=50)
original_entry.grid(row=4, column=2, sticky="EW")
text_entry = Entry(width=50)
text_entry.grid(row=5, column=2, sticky="EW")  # sticky="EW" ensures the alignment of subsequent columns
logo_entry = Entry(width=50)
logo_entry.grid(row=6, column=2, sticky="EW")

original_entry.focus()

# Buttons
original_upload_button = Button(text="Select Image", command=lambda: select_file("original"))
original_upload_button.grid(row=4, column=3, sticky="EW")
logo_upload_button = Button(text="Select Image", command=lambda: select_file("logo"))
logo_upload_button.grid(row=6, column=3, sticky="EW")
add_button = Button(text="Add Watermark", command=add_watermark)
add_button.grid(row=7, column=2, sticky="EW")

window.mainloop()
