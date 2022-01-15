# References:
# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#coordinates
# https://www.blog.pythonlibrary.org/2017/10/17/how-to-watermark-your-photos-with-python/
# https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white

# Features that can be added:
# Show the final image on Tkinter
# Display the logo at the specified location e.g. in the middle of the base image

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from watermark import Watermark

# Logging into a file on the server
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s -- %(message)s"
logging.basicConfig(filename='watermark.log', level=logging.INFO, format=LOG_FORMAT, filemode='a')

original_img = ""
logo_img = ""
watermark = Watermark()


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
            # watermark.add_logo(original_img, watermark_logo)
            watermark.add_logo_transparent(original_img, watermark_logo)
            messagebox.showinfo(title="Success", message="Watermark Logo added. "
                                                         "Check the new file with _watermark name in the same folder.")

        if watermark_text:
            watermark.add_text(original_img, watermark_text)
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

# canvas = Canvas(height=380, width=370)
# logo_img = PhotoImage(file="Success_watermark.png")
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
