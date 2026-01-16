import pygame
import threading
import os
import select
import time

# Für Pi evdev
try:
    from evdev import InputDevice, categorize, ecodes, list_devices
    EVDEV_AVAILABLE = True
except ImportError:
    EVDEV_AVAILABLE = False

# Standardisierte Aktionen
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
CONFIRM = "CONFIRM"
BACK = "BACK"
DROP = "DROP"
HOLD = "HOLD"
INPUTDELAY = 0.13  # Sekunden

class InputHandler:
    def __init__(self, started_on_pi=False):
        self.started_on_pi = started_on_pi
        self.pressed = set()          # Pygame + Joystick Tasten
        self.evdev_pressed = set()    # Pi evdev Tasten
        self.pressed_lock = threading.Lock()  # Thread-Safety für evdev
        self.input_delay = INPUTDELAY  # 100 ms für ALLE Inputs
        self.last_input_time = {}

        # Key Mapping für Pygame
        self.key_map = {
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_RETURN: CONFIRM,
            pygame.K_ESCAPE: BACK,
            pygame.K_SPACE: DROP,
            pygame.K_c: HOLD,
        }

        # Key Mapping für Pi evdev
        self.evdev_map = {}
        if started_on_pi and EVDEV_AVAILABLE:
            self.evdev_map = {
                ecodes.KEY_UP: UP,
                ecodes.KEY_DOWN: DOWN,
                ecodes.KEY_LEFT: LEFT,
                ecodes.KEY_RIGHT: RIGHT,
                ecodes.KEY_ENTER: CONFIRM,
                ecodes.KEY_KPENTER: CONFIRM,
                ecodes.KEY_ESC: BACK,
                ecodes.KEY_SPACE: DROP,
                ecodes.KEY_C: HOLD
            }
            self.start_evdev_keyboard()

        # Joysticks initialisieren
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()

    def is_pressed(self, action):
        now = time.time()

        with self.pressed_lock:
            # Taste überhaupt gedrückt?
            pressed = action in self.pressed or action in self.evdev_pressed
            if not pressed:
                self.last_input_time.pop(action, None)
                return False

            last = self.last_input_time.get(action, 0)
            if now - last >= self.input_delay:
                self.last_input_time[action] = now
                return True

        return False
    

    def is_pressed_custom(self, action, delay):
        now = time.time()

        with self.pressed_lock:
            # Taste überhaupt gedrückt?
            pressed = action in self.pressed or action in self.evdev_pressed
            if not pressed:
                self.last_input_time.pop(action, None)
                return False

            last = self.last_input_time.get(action, 0)
            if now - last >= delay:
                self.last_input_time[action] = now
                return True

        return False

    # ---------------------------
    # EVDEV Handling für Pi
    # ---------------------------
    def _find_first_active_keyboard(self):
        candidates = []
        for path in list_devices():
            dev = InputDevice(path)
            if "keyboard" in dev.name.lower():
                candidates.append(dev)
                print(f"Gefundene Keyboard-Candidate: {dev.name} ({dev.path})")

        if not candidates:
            print("Keine Tastaturen gefunden")
            return None

        print("Bitte Taste auf einer Tastatur drücken...")
        while True:
            r, _, _ = select.select([d.fd for d in candidates], [], [], 0.1)
            for fd in r:
                dev = next(d for d in candidates if d.fd == fd)
                for event in dev.read():
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        print(f"✅ Aktive Tastatur: {dev.name} ({dev.path})")
                        return dev

    def start_evdev_keyboard(self):
        keyboard = self._find_first_active_keyboard()
        if not keyboard:
            return

        # Optional: keyboard.grab() kann blockieren
        # try:
        #     keyboard.grab()
        # except OSError as e:
        #     print(f"Failed to grab keyboard: {e}")
        #     return

        def _reader():
            for event in keyboard.read_loop():
                if event.type == ecodes.EV_KEY:
                    mapped = self.evdev_map.get(event.code)
                    if mapped:
                        with self.pressed_lock:
                            if event.value == 1:
                                self.evdev_pressed.add(mapped)
                            elif event.value == 0:
                                self.evdev_pressed.discard(mapped)

        threading.Thread(target=_reader, daemon=True).start()

    # ---------------------------
    # Pygame Event Handling
    # ---------------------------
    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                mapped = self.key_map.get(event.key)
                if mapped:
                    self.pressed.add(mapped)
            elif event.type == pygame.KEYUP:
                mapped = self.key_map.get(event.key)
                if mapped:
                    self.pressed.discard(mapped)

            # Joystick Achsen & Buttons
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        self.pressed.add(LEFT)
                    elif event.value > 0.5:
                        self.pressed.add(RIGHT)
                    else:
                        self.pressed.discard(LEFT)
                        self.pressed.discard(RIGHT)
                elif event.axis == 1:
                    if event.value < -0.5:
                        self.pressed.add(UP)
                    elif event.value > 0.5:
                        self.pressed.add(DOWN)
                    else:
                        self.pressed.discard(UP)
                        self.pressed.discard(DOWN)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.pressed.add(CONFIRM)
                elif event.button == 1:
                    self.pressed.add(BACK)
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.pressed.discard(CONFIRM)
                elif event.button == 1:
                    self.pressed.discard(BACK)
