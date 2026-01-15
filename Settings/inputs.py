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

class InputHandler:
    REPEAT_DELAY = 0.2  # 200ms Delay für gedrückthalten

    def __init__(self, started_on_pi=False):
        self.started_on_pi = started_on_pi
        self.pressed = set()          # Pygame + Joystick Tasten
        self.evdev_pressed = set()    # Pi evdev Tasten
        self.evdev_last_time = {}     # für Repeat-Delay
        self.pressed_lock = threading.Lock()  # Thread-Safety für evdev
        self.keyboard_device = None

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
            self.start_evdev_keyboard(non_blocking=True)

        # Joysticks initialisieren
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()

    def is_pressed(self, action):
        """Checkt, ob eine standardisierte Aktion gerade gedrückt wurde"""
        with self.pressed_lock:
            if action in self.pressed:
                return True
            # evdev mit Repeat-Delay
            if action in self.evdev_pressed:
                now = time.time()
                last = self.evdev_last_time.get(action, 0)
                if now - last >= self.REPEAT_DELAY:
                    self.evdev_last_time[action] = now
                    return True
        return False

    # ---------------------------
    # EVDEV Handling für Pi
    # ---------------------------
    def _find_active_keyboard_non_blocking(self):
        """Sucht Tastatur non-blocking, returns InputDevice oder None"""
        candidates = []
        for path in list_devices():
            dev = InputDevice(path)
            if "keyboard" in dev.name.lower():
                candidates.append(dev)

        if not candidates:
            return None

        r, _, _ = select.select([d.fd for d in candidates], [], [], 0)
        for fd in r:
            dev = next(d for d in candidates if d.fd == fd)
            for event in dev.read():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    return dev
        return None

    def start_evdev_keyboard(self, non_blocking=False):
        """Startet evdev-Keyboard Thread"""
        def _reader():
            while True:
                # Falls noch keine Tastatur gesetzt: non-blocking Suche
                if self.keyboard_device is None:
                    dev = self._find_active_keyboard_non_blocking()
                    if dev:
                        print(f"✅ Aktive Tastatur gesetzt: {dev.name} ({dev.path})")
                        self.keyboard_device = dev
                    else:
                        time.sleep(0.01)
                        continue

                for event in self.keyboard_device.read():
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
        if not self.started_on_pi:
            # Nur auf Nicht-Pi Pygame Events clearen
            self.pressed.clear()

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
