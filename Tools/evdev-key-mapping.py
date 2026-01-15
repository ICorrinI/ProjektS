#!/usr/bin/env python3
import sys
from evdev import InputDevice, list_devices, ecodes, categorize, util
import select

def find_first_active_keyboard():
    candidates = []

    # manuel python3 -m evdev-evtest
    # alle Devices mit "keyboard" im Namen sammeln
    for path in list_devices():
        dev = InputDevice(path)
        if "keyboard" in dev.name.lower():
            candidates.append(dev)
            print(f"Gefundenes Keyboard-Candidate: {dev.name} ({dev.path})")

    if not candidates:
        print("Keine Tastaturen gefunden")
        return None

    print("\nBitte eine Taste auf einer Tastatur drücken, um die aktive zu wählen...")

    while True:
        r, _, _ = select.select([dev.fd for dev in candidates], [], [], 0.1)
        for fd in r:
            # das Device zu dem FD finden
            dev = next(d for d in candidates if d.fd == fd)
            for event in dev.read():
                if event.type == ecodes.EV_KEY and event.value == 1:  # key down
                    print(f"✅ Aktive Tastatur: {dev.name} ({dev.path})")
                    return dev

def main():
    keyboard = find_first_active_keyboard()
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
