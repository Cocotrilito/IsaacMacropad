#   MK1 BY COCOTRILO
import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation

# --- Keyboard base ---
keyboard = KMKKeyboard()

# Matrix pins (3x3)
keyboard.col_pins = (board.GP29, board.GP0, board.GP1)
keyboard.row_pins = (board.GP26, board.GP27, board.GP28)

# Diodes: are facing the rows
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Encoder (rotation only) ---
from kmk.modules.encoder import EncoderHandler

encoder = EncoderHandler()
encoder.pins = ((board.GP2, board.GP3, False),)  # (A, B, is_reversed)
encoder.map = (
    (KC.VOLD, KC.VOLU),  # CCW, CW
)
keyboard.modules.append(encoder)

#  --- Oled Screen ---
try:
    from kmk.extensions.oled import OLED

    i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
    oled = OLED(
        i2c=i2c,
        addr=0x3C,
        width=128,
        height=32,
        flip=False,
    )

    # Simple screen
    
    oled.entries = [
        ("MK1 by cocotrilo", 0, 0),
        ("Layer:", 0, 16),
        (lambda: str(keyboard.active_layers[0]), 50, 16),
    ]
    keyboard.extensions.append(oled)

except Exception:
    # OLED not available yet — firmware still works without display
    pass

# --- Keymaps (2 layers) ---
#   The idea is to make a swiss-army tool macropad with diferent layers for diferent workflows in my computer
# Layer 0: productivity / macros placeholder
# Layer 1: media controls (no brightness keys)
keyboard.keymap = [
    # LAYER 0
    [
        KC.ESC,   KC.TAB,   KC.BSPC,
        KC.LCTL,  KC.LALT,  KC.LGUI,
        KC.TG(1), KC.ENT,   KC.SPC,
    ],

    # LAYER 1 (Media)
    [
        KC.MPLY,  KC.MPRV,  KC.MNXT,
        KC.MUTE,  KC.VOLD,  KC.VOLU,
        KC.TG(1), KC.NO,    KC.NO,
    ],
]

if __name__ == "__main__":
    keyboard.go()
