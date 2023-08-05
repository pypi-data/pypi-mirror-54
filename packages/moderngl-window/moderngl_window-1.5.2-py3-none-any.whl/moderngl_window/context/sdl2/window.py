from typing import Tuple
from ctypes import c_int
import sdl2
import sdl2.ext
import sdl2.video

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.sdl2.keys import Keys


class Window(BaseWindow):
    """
    Basic window implementation using SDL2.
    """
    #: SDL2 specific key constants
    keys = Keys

    _mouse_button_map = {
        1: 1,
        3: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise ValueError("Failed to initialize sdl2")

        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, self.gl_version[0])
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, self.gl_version[1])
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)

        sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if self.cursor else sdl2.SDL_DISABLE)

        if self.samples > 1:
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, self.samples)

        flags = sdl2.SDL_WINDOW_OPENGL
        if self.fullscreen:
            flags |= sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
        else:
            if self.resizable:
                flags |= sdl2.SDL_WINDOW_RESIZABLE

        self._window = sdl2.SDL_CreateWindow(
            self.title.encode(),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.width,
            self.height,
            flags,
        )

        if not self._window:
            raise ValueError("Failed to create window:", sdl2.SDL_GetError())

        self._context = sdl2.SDL_GL_CreateContext(self._window)

        sdl2.video.SDL_GL_SetSwapInterval(1 if self.vsync else 0)

        self.init_mgl_context()

        self.set_default_viewport()

    @property
    def position(self) -> Tuple[int, int]:
        """Tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        x = c_int(0)
        y = c_int(0)
        sdl2.SDL_GetWindowPosition(self._window, x, y)
        return x.value, y.value

    @position.setter
    def position(self, value: Tuple[int, int]):
        sdl2.SDL_SetWindowPosition(self._window, value[0], value[1])

    def swap_buffers(self) -> None:
        """Swap buffers, set viewport, trigger events and increment frame counter"""
        sdl2.SDL_GL_SwapWindow(self._window)
        self.set_default_viewport()
        self.process_events()
        self._frames += 1

    def resize(self, width, height) -> None:
        """Resize callback

        Args:
            width: New window width
            height: New window height
        """
        self._width = width
        self._height = height
        self._buffer_width, self._buffer_height = self._width, self._height
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def _handle_mods(self) -> None:
        """Update key mods"""
        mods = sdl2.SDL_GetModState()
        self._modifiers.shift = mods & sdl2.KMOD_SHIFT
        self._modifiers.ctrl = mods & sdl2.KMOD_CTRL

    def process_events(self) -> None:
        """Handle all queued events in sdl2 dispatching events to standard methods"""
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_MOUSEMOTION:
                if self.mouse_states.any:
                    self._mouse_drag_event_func(event.motion.x, event.motion.y)
                else:
                    self._mouse_position_event_func(event.motion.x, event.motion.y)

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, True)
                    self._mouse_release_event_func(
                        event.motion.x, event.motion.y,
                        button,
                    )

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, False)
                    self._mouse_press_event_func(
                        event.motion.x, event.motion.y,
                        button,
                    )

            elif event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP]:
                self._handle_mods()

                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.close()

                if event.type == sdl2.SDL_KEYDOWN:
                    self._key_pressed_map[event.key.keysym.sym] = True
                elif event.type == sdl2.SDL_KEYUP:
                    self._key_pressed_map[event.key.keysym.sym] = False

                self._key_event_func(event.key.keysym.sym, event.type, self._modifiers)

            elif event.type == sdl2.SDL_TEXTINPUT:
                self._unicode_char_entered_func(event.text.text.decode())

            elif event.type == sdl2.SDL_MOUSEWHEEL:
                self._mouse_scroll_event_func(float(event.wheel.x), float(event.wheel.y))

            elif event.type == sdl2.SDL_QUIT:
                self.close()

            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self.resize(event.window.data1, event.window.data2)

    def destroy(self) -> None:
        """Gracefully close the window"""
        sdl2.SDL_GL_DeleteContext(self._context)
        sdl2.SDL_DestroyWindow(self._window)
        sdl2.SDL_Quit()
