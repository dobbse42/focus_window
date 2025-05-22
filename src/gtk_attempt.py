import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

class ImageWindow(Gtk.Window):
  def __init__(self):
    super().__init__()
    self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
    self.set_decorated(False)
    self.set_keep_above(True)
    self.set_app_paintable(True)

    imgpath = "/home/evan/.config/background/white_test.png"

    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(imgpath, 100, 100, True)
    image = Gtk.Image.new_from_pixbuf(pixbuf)
    self.add(image)

    self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    self.set_resizable(False)

    self.set_default_size(100, 100)
    self.move_to_corner()

    self.show_all()

  def move_to_corner(self):
    screen = self.get_screen()
    #monitor = screen.get_monitor_geometry(screen.get_primary_monitor())
    #x = monitor.x + monitor.width - 50
    #y = monitor.y + monitor.height - 110
    x = 100
    y = 100
    self.move(x, y)

win = ImageWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
