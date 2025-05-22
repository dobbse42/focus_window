import os
from pywayland.client import Display
from pywayland.protocol.wl_compositor import WlCompositor
from pywayland.protocol.wl_shm import WlShm
from pywayland.protocol.zwlr_layer_shell_v1 import ZwlrLayerShellV1, ZwlrLayerSurfaceV1
from pywayland.protocol.wl_surface import WlSurface
from PIL import Image
import mmap

LAYER_TOP = ZwlrLayerSurfaceV1.layer_top
ANCHOR_BOTTOM = ZwlrLayerSurfaceV1.anchor_bottom
ANCHOR_RIGHT = ZwlrLayerSurfaceV1.anchor_right

def create_shm_buffer(shm, width, height, image_path):
  stride = width*4
  size = stride*height

  shm_fd = os.open("/dev/shm/wayland-buffer", os.O_RDWR | os.O_CREAT | os.O_TRUNC)
  os.ftruncate(shm_fd, size)
  buffer_map = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE)

  image = Image.open(image_path).convert("RGBA")
  resized_image = image.resize((width, height))
  buffer_map.write(resized_image.tobytes())
  buffer_map.seek(0)

  shm_buffer = shm.create_pool(shm_fd, size).create_buffer(0, width, height, stride, WlShm.format_argb8888)
  os.close(shm_fd)

  return shm_buffer

def main():
  display = Display()
  display.connect()

  registry = display.get_registry()
  compositor = registry.bind(WlCompositor)
  shm = registry.bind(WlShm)
  layer_shell = registry.bind(ZwlrLayerShellV1)

  display.roundtrip()

  surface = compositor.create_surface()

  layer_surface = layer_shell.get_layer_surface(
    surface,
    None,
    LAYER_TOP,
    "example-image"
  )
  layer_surface.set_size(100, 100)
  layer_surface.set_anchor(ANCHOR_BOTTOM | ANCHOR_RIGHT)
  layer_surface.set_margin(10, 10, 10, 10)
  layer_surface.commit()

  image_path = "your-image.png"
  width, height = 100, 100
  buffer = create_shm_buffer(shm, width, height, image_path)

  surface.attach(buffer, 0, 0)
  surface.commit()

  while True:
    display.dispatch()


if __name__ == "__main__":
  main()
