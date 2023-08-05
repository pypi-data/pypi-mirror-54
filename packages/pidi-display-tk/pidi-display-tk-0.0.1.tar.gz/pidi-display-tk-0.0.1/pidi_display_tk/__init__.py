"""pidi plugin for Tk display."""
import tkinter
from PIL import ImageTk
from pidi_display_pil import DisplayPIL


__version__ = '0.0.1'


class DisplayTK(DisplayPIL):
    """Tk display output for pidi."""

    # pylint: disable=too-few-public-methods

    option_name = 'tk'

    def __init__(self, args):
        DisplayPIL.__init__(self, args)

        self._root = tkinter.Tk()
        self._root.geometry(f'{self._size}x{self._size}')
        self._root.resizable(False, False)

    def redraw(self):
        DisplayPIL.redraw(self)

        self._root.title(f"{self._title} - {self._artist}, {self._album}")

        imagetk = ImageTk.PhotoImage(self._output_image)
        label_image = tkinter.Label(self._root, image=imagetk)
        label_image.place(x=0, y=0, width=self._size, height=self._size)

        self._root.update()
