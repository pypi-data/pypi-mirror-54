from typing import Tuple
import glfw

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.glfw.keys import Keys


class Window(BaseWindow):
    """
    Window based on GLFW
    """
    #: GLFW specific key constants
    keys = Keys

    # GLFW do support other buttons, but we are limited by other libraries
    _mouse_button_map = {
        0: 1,
        1: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        # Configure the OpenGL context
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            self._width, self._height = mode.size.width, mode.size.height

            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        self._window = glfw.create_window(self.width, self.height, self.title, monitor, None)

        if not self._window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        if not self.cursor:
            glfw.set_input_mode(self._window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        glfw.make_context_current(self._window)

        if self.vsync:
            glfw.swap_interval(1)

        glfw.set_key_callback(self._window, self.glfw_key_event_callback)
        glfw.set_cursor_pos_callback(self._window, self.glfw_mouse_event_callback)
        glfw.set_mouse_button_callback(self._window, self.glfw_mouse_button_callback)
        glfw.set_scroll_callback(self._window, self.glfw_mouse_scroll_callback)
        glfw.set_window_size_callback(self._window, self.glfw_window_resize_callback)
        glfw.set_char_callback(self._window, self.glfw_char_callback)

        self.init_mgl_context()
        self.set_default_viewport()

    @property
    def position(self) -> Tuple[int, int]:
        """Tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        return glfw.get_window_pos(self._window)

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._position = glfw.set_window_pos(self._window, value[0], value[1])

    def close(self) -> None:
        """Suggest to glfw the window should be closed soon"""
        glfw.set_window_should_close(self._window, True)

    @property
    def is_closing(self):
        """bool: Checks if the window is scheduled for closing"""
        return glfw.window_should_close(self._window)

    def swap_buffers(self):
        """Swap buffers, increment frame counter and pull events"""
        glfw.swap_buffers(self._window)
        self._frames += 1
        glfw.poll_events()

    def _handle_modifiers(self, mods):
        """Checks key modifiers"""
        self._modifiers.shift = mods & 1 == 1
        self._modifiers.ctrl = mods & 2 == 2

    def glfw_key_event_callback(self, window, key, scancode, action, mods):
        """Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        Args:
            window: Window event origin
            key: The key that was pressed or released.
            scancode: The system-specific scancode of the key.
            action: ``GLFW_PRESS``, ``GLFW_RELEASE`` or ``GLFW_REPEAT``
            mods: Bit field describing which modifier keys were held down.
        """
        if key == self.keys.ESCAPE:
            self.close()

        self._handle_modifiers(mods)

        if action == self.keys.ACTION_PRESS:
            self._key_pressed_map[key] = True
        elif action == self.keys.ACTION_RELEASE:
            self._key_pressed_map[key] = False

        self._key_event_func(key, action, self._modifiers)

    def glfw_mouse_event_callback(self, window, xpos, ypos):
        """Mouse position event callback from glfw.
        Translates the events forwarding them to :py:func:`cursor_event`.

        Screen coordinates relative to the top-left corner

        Args:
            window: The window
            xpos: viewport x pos
            ypos: viewport y pos
        """
        if self.mouse_states.any:
            self._mouse_drag_event_func(xpos, ypos)
        else:
            self._mouse_position_event_func(xpos, ypos)

    def glfw_mouse_button_callback(self, window, button, action, mods):
        """Handle mouse button events and forward them to the example

        Args:
            window: The window
            button: The button creating the event
            action: Button action (press or release)
            mods: They modifiers such as ctrl or shift
        """
        button = self._mouse_button_map.get(button, None)
        if button is None:
            return

        xpos, ypos = glfw.get_cursor_pos(self._window)

        if action == glfw.PRESS:
            self._handle_mouse_button_state_change(button, True)
            self._mouse_press_event_func(xpos, ypos, button)
        else:
            self._handle_mouse_button_state_change(button, False)
            self._mouse_release_event_func(xpos, ypos, button)

    def glfw_mouse_scroll_callback(self, window, x_offset: float, y_offset: float):
        """Handle mouse scoll events and forward them to the example

        Args:
            window: The window
            x_offset (float): x wheel offset
            y_offest (float): y wheel offset
        """
        self._mouse_scroll_event_func(x_offset, y_offset)

    def glfw_char_callback(self, window, codepoint: int):
        """Handle text input (only unicode charaters)

        Args:
            window: The glfw window
            codepoint (int): The unicode codepoint
        """
        self._unicode_char_entered_func(chr(codepoint))

    def glfw_window_resize_callback(self, window, width, height):
        """
        Window resize callback for glfw

        Args:
            window: The window
            width: New width
            height: New height
        """
        self._width, self._height = width, height
        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def destroy(self):
        """Gracefully terminate GLFW"""
        glfw.terminate()
