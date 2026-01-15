#!/usr/bin/env python3
import sys
from evdev import InputDevice, list_devices, categorize, ecodes

def find_keyboard():
    for path in list_devices():
        dev = InputDevice(path)
        if "keyboard" in dev.name.lower():
            return dev
    return None

def main():
    keyboard = find_keyboard()
    if not keyboard:
        print("Keine Tastatur gefunden")
        sys.exit(1)

    print(f"Gefundene Tastatur: {keyboard.name} ({keyboard.path})")
    print("Drücke Tasten (Strg+C zum Beenden)...\n")

    try:
        for event in keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                print("---")
                print(f"event: {event}")
                print(f"event.type: {event.type}")
                print(f"event.code: {event.code} -> {ecodes.KEY[event.code]}")
                print(f"event.value: {event.value}  (0=up,1=down,2=hold)")
                try:
                    print(f"key.scancode: {key.scancode}")
                except AttributeError:
                    print("key.scancode: n/a")
                try:
                    print(f"key.keycode: {key.keycode}")
                except AttributeError:
                    print("key.keycode: n/a")
                print("---\n")
    except KeyboardInterrupt:
        print("\nBeendet.")

if __name__ == "__main__":
    main()
