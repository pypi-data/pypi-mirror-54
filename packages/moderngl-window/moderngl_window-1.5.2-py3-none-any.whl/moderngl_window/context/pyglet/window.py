from typing import Tuple
import platform
import pyglet

# On OS X we need to disable the shadow context
# because the 2.1 shadow contect cannot be upgrade to a 3.3+ core
if platform.system() == 'Darwin':
    pyglet.options['shadow_window'] = False

pyglet.options['debug_gl'] = False

from moderngl_window.context.pyglet.keys import Keys  # noqa: E402
from moderngl_window.context.base import BaseWindow  # noqa: E402


class Window(BaseWindow):
    """
    Window based on Pyglet 1.4.x
    """
    #: Pyglet specific key constants
    keys = Keys

    # pyglet button id -> universal button id
    _mouse_button_map = {
        1: 1,
        4: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config = pyglet.gl.Config(
            major_version=self.gl_version[0],
            minor_version=self.gl_version[1],
            forward_compatible=True,
            depth_size=24,
            double_buffer=True,
            sample_buffers=1 if self.samples > 1 else 0,
            samples=self.samples,
        )

        if self.fullscreen:
            display = pyglet.canvas.get_display()
            screen = display.get_default_screen()
            self._width, self._height = screen.width, screen.height

        self._window = PygletWrapper(
            width=self.width, height=self.height,
            caption=self.title,
            resizable=self.resizable,
            vsync=self.vsync,
            fullscreen=self.fullscreen,
            config=config,
        )

        self._window.set_mouse_visible(self.cursor)

        self._window.event(self.on_key_press)
        self._window.event(self.on_key_release)
        self._window.event(self.on_mouse_motion)
        self._window.event(self.on_mouse_drag)
        self._window.event(self.on_resize)
        self._window.event(self.on_mouse_press)
        self._window.event(self.on_mouse_release)
        self._window.event(self.on_mouse_scroll)
        self._window.event(self.on_text)

        self.init_mgl_context()
        self._buffer_width, self._buffer_height = self._window.get_framebuffer_size()
        self.set_default_viewport()

    @property
    def position(self) -> Tuple[int, int]:
        """Tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        return self._window.get_location()

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._window.set_location(value[0], value[1])

    @property
    def is_closing(self) -> bool:
        """Check pyglet's internal exit state"""
        return self._window.has_exit or super().is_closing

    def close(self) -> None:
        """Close the pyglet window directly"""
        self._window.close()
        super().close()

    def swap_buffers(self) -> None:
        """Swap buffers, increment frame counter and pull events"""
        self._window.flip()
        self._frames += 1
        self._window.dispatch_events()

    def _handle_modifiers(self, mods):
        """Update key modifier states"""
        self._modifiers.shift = mods & 1 == 1
        self._modifiers.ctrl = mods & 2 == 2

    def on_key_press(self, symbol, modifiers):
        """Pyglet specific key press callback.

        Forwards and translates the events to the standard methods.

        Args:
            symbol: The symbol of the pressed key
            modifiers: Modifier state (shift, ctrl etc.)
        """
        self._key_pressed_map[symbol] = True
        self._handle_modifiers(modifiers)
        self._key_event_func(symbol, self.keys.ACTION_PRESS, self._modifiers)

    def on_text(self, text):
        """Pyglet specific text input callback

        Forwards and translates the events to the standard methods.

        Args:
            text (str): The unicode character entered
        """
        self._unicode_char_entered_func(text)

    def on_key_release(self, symbol, modifiers):
        """Pyglet specific key release callback.

        Forwards and translates the events to standard methods.

        Args:
            symbol: The symbol of the pressed key
            modifiers: Modifier state (shift, ctrl etc.)
        """
        self._key_pressed_map[symbol] = False
        self._handle_modifiers(modifiers)
        self._key_event_func(symbol, self.keys.ACTION_RELEASE, self._modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Pyglet specific mouse motion callback.

        Forwards and traslates the event to the standard methods.

        Args:
            x: x position of the mouse
            y: y position of the mouse
            dx: delta x position
            dy: delta y position of the mouse
        """
        # NOTE: Screen coordinates relative to the lower-left corner
        # so we have to flip the y axis to make this consistent with
        # other window libraries
        self._mouse_position_event_func(x, self._buffer_height - y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Pyglet specific mouse drag event.

        When a mouse button is pressed this is the only way
        to capture mouse posision events
        """
        self._mouse_drag_event_func(x, self._buffer_height - y)

    def on_mouse_press(self, x: int, y: int, button, mods):
        """Handle mouse press events and forward to standard methods

        Args:
            x: x position of the mouse when pressed
            y: y position of the mouse when pressed
            button: The pressed button
            mods: Modifiers
        """
        button = self._mouse_button_map.get(button, None)
        if button is not None:
            self._handle_mouse_button_state_change(button, True)
            self._mouse_press_event_func(
                x, self._buffer_height - y,
                button,
            )

    def on_mouse_release(self, x: int, y: int, button, mods):
        """Handle mouse release events and forward to standard methods

        Args:
            x: x position when moutse button was released
            y: y position when moutse button was released
            button: The button pressed
            mods: Modifiers
        """
        button = self._mouse_button_map.get(button, None)
        if button is not None:
            self._handle_mouse_button_state_change(button, False)
            self._mouse_release_event_func(
                x, self._buffer_height - y,
                button,
            )

    def on_mouse_scroll(self, x, y, x_offset: float, y_offset: float):
        """Handle mouse wheel.

        Args:
            x_offset (float): X scroll offset
            y_offset (float): Y scroll offset
        """
        self.mouse_scroll_event_func(x_offset, y_offset)

    def on_resize(self, width: int, height: int):
        """Pyglet specific callback for window resize events forwarding to standard methods

        Args:
            width: New window width
            height: New window height
        """
        self._width, self._height = width, height
        self._buffer_width, self._buffer_height = self._window.get_framebuffer_size()
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def destroy(self):
        """Destroy the pyglet window"""
        pass


class PygletWrapper(pyglet.window.Window):
    """Block out some window methods so pyglet don't trigger GL errors"""

    def on_resize(self, width, height):
        """Block out the resize method.
        For some reason pyglet calls this triggering errors.
        """
        pass

    def on_draw(self):
        """Block out the default draw method to avoid GL errors"""
        pass
