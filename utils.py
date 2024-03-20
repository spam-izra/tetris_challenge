from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui

import time
import sys


def impl_glfw_init(*, size=None, window_name="minimal ImGui/GLFW3 example"):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    mon = glfw.get_primary_monitor()
    screen_size =  glfw.get_monitor_workarea(mon)
    print("Detected screen size:", screen_size)

    if size is None:
        x, y, w, h = screen_size
        size = w - 100, h - 100

    size = list(size)

    if size[0] > screen_size[2] - 100:
        size[0] = screen_size[2] - 100
    if size[1] > screen_size[3] - 100:
        size[1] = screen_size[3] - 100

    x = max(50, screen_size[0] + screen_size[2] / 2 - size[0] / 2)
    y = max(50, screen_size[1] + screen_size[3] / 2 - size[1] / 2)
    width, height = size

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.set_window_pos(window, int(x), int(y))
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


def fb_to_window_factor(window):
    win_w, win_h = glfw.get_window_size(window)
    fb_w, fb_h = glfw.get_framebuffer_size(window)

    return max(float(fb_w) / win_w, float(fb_h) / win_h)



class Application:
    def __init__(self, *, screen_size=(1280, 720), title="Application"):
        self.screen_size = screen_size
        self.title = title
        self.fonts = {}
        self.clock = time.monotonic()

    def add_font(self, name: str, font):
        self.fonts[name] = font

    def get_font(self, name):
        return self.fonts[name]

    def init_fonts(self, impl: GlfwRenderer):
        return
        """
        io = imgui.get_io()
        io.fonts.clear()
        # io.fonts.add_font_default()
        cfg = imgui.FontConfig(merge_mode=True)

        io.fonts.add_font_from_file_ttf("DroidSans.ttf", 20, None,
            io.fonts.get_glyph_ranges_latin())
        self.add_font(
            "DroidSansJapanese,20",
            io.fonts.add_font_from_file_ttf("DroidSansJapanese.ttf", 20, cfg,
            io.fonts.get_glyph_ranges_japanese()))

        self.add_font(
            "DroidSansJapanese,15",
            io.fonts.add_font_from_file_ttf("DroidSansJapanese.ttf", 15, None,
            io.fonts.get_glyph_ranges_japanese()))

        self.add_font(
            "DroidSansJapanese,10",
            io.fonts.add_font_from_file_ttf("DroidSansJapanese.ttf", 10, None,
            io.fonts.get_glyph_ranges_japanese()))
        """

    def draw(dt: float, self, width: int, height: int, keys: list):
        with imgui.begin("Text example"):
            imgui.text("Hello!")


    def loop(self, framerate=1.0/30.0):
        imgui.create_context()

        window = impl_glfw_init(size=self.screen_size, window_name=self.title)
        impl = GlfwRenderer(window)
        font_scaling_factor = fb_to_window_factor(window)
        print("Font Scaling Factor: ", font_scaling_factor)

        io = imgui.get_io()
        io.fonts.add_font_default()
        self.init_fonts(impl)
        impl.refresh_font_texture()

        try:
            history = []
            while not glfw.window_should_close(window):
                t = time.monotonic()
                dt = t - self.clock

                self.clock = t

                history.append(dt)
                while len(history) > 10:
                    history.pop(0)

                glfw.poll_events()
                impl.process_inputs()

                imgui.new_frame()

                keys = []

                if glfw.get_key(window, glfw.KEY_A):
                    keys.append("A")
                if glfw.get_key(window, glfw.KEY_S):
                    keys.append("S")
                if glfw.get_key(window, glfw.KEY_D):
                    keys.append("D")
                if glfw.get_key(window, glfw.KEY_W):
                    keys.append("W")
                if glfw.get_key(window, glfw.KEY_Q):
                    keys.append("Q")
                if glfw.get_key(window, glfw.KEY_E):
                    keys.append("E")

                size = glfw.get_window_size(window)
                self.draw(dt, *size, keys=keys)

                imgui.set_next_window_position(size[0] - 150, 10)
                imgui.set_next_window_size(80, 70)
                with imgui.begin("FPS", False, imgui.WINDOW_NO_RESIZE | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_NAV):
                    imgui.text(f"{len(history)/sum(history):5.2f}")

                gl.glClearColor(0, 0, 0, 1)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                imgui.render()
                impl.render(imgui.get_draw_data())
                glfw.swap_buffers(window)

                if self.sleep:
                    time.sleep(self.sleep)
                else:
                    t = time.monotonic()
                    leftover = max(0, framerate - (t - self.clock))
                    if leftover:
                        time.sleep(leftover)
        finally:
            impl.shutdown()
            glfw.terminate()