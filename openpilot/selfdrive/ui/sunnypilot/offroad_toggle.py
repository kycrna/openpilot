"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.

One-tap Always Offroad shortcut for the tici/tizi UI: a pill on the driving view (above the driver monitoring icon) to enter
Always Offroad, and a pill on the home screen header to exit it.
"""
import pyray as rl
from openpilot.selfdrive.ui import UI_BORDER_SIZE
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.text_measure import measure_text_cached
from openpilot.system.ui.widgets.confirm_dialog import alert_dialog

ONROAD_BTN_WIDTH = 300
ONROAD_BTN_HEIGHT = 150
ONROAD_BTN_GAP = 30  # space between the button and the driver monitoring icon below it
FONT_SIZE = 56

BG_COLOR = rl.Color(0, 0, 0, 166)
BORDER_COLOR = rl.Color(255, 255, 255, 75)
EXIT_COLOR = rl.Color(54, 77, 239, 255)


def set_always_offroad(enable: bool) -> None:
  if enable and ui_state.engaged:
    gui_app.push_widget(alert_dialog(tr("Disengage to Enter Always Offroad Mode")))
    return
  ui_state.params.put_bool("OffroadMode", enable)
  ui_state.always_offroad = enable


def onroad_button_rect(content_rect: rl.Rectangle) -> rl.Rectangle:
  """Bottom-left, stacked directly above the driver monitoring icon."""
  from openpilot.selfdrive.ui.onroad.driver_state import BTN_SIZE as DM_BTN_SIZE
  from openpilot.selfdrive.ui.sunnypilot.onroad.developer_ui import get_bottom_dev_ui_offset
  dm_top = content_rect.y + content_rect.height - UI_BORDER_SIZE - DM_BTN_SIZE - get_bottom_dev_ui_offset()
  return rl.Rectangle(content_rect.x + UI_BORDER_SIZE, dm_top - ONROAD_BTN_GAP - ONROAD_BTN_HEIGHT,
                      ONROAD_BTN_WIDTH, ONROAD_BTN_HEIGHT)


def _draw_text_centered(rect: rl.Rectangle, text: str, font_size: int) -> None:
  font = gui_app.font(FontWeight.MEDIUM)
  size = measure_text_cached(font, text, font_size)
  pos = rl.Vector2(int(rect.x + (rect.width - size.x) / 2), int(rect.y + (rect.height - size.y) / 2))
  rl.draw_text_ex(font, text, pos, font_size, 0, rl.WHITE)


def draw_onroad_button(rect: rl.Rectangle) -> None:
  rl.draw_rectangle_rounded(rect, 0.35, 10, BG_COLOR)
  rl.draw_rectangle_rounded_lines_ex(rect, 0.35, 10, 4, BORDER_COLOR)
  _draw_text_centered(rect, tr("OFFROAD"), FONT_SIZE)


def draw_exit_button(rect: rl.Rectangle, font_size: int) -> None:
  rl.draw_rectangle_rounded(rect, 0.3, 10, EXIT_COLOR)
  _draw_text_centered(rect, tr("EXIT OFFROAD"), font_size)
