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

        # Key Mapping für Pygame (Pfeiltasten + WASD)
        self.key_map = {
            # Pfeiltasten
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,

            # WASD
            pygame.K_w: UP,
            pygame.K_s: DOWN,
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT,

            # Aktionen
            pygame.K_RETURN: CONFIRM,
            pygame.K_ESCAPE: BACK,
            pygame.K_SPACE: DROP,
            pygame.K_c: HOLD,
        }

        # Key Mapping für Pi evdev (Pfeiltasten + WASD)
        self.evdev_map = {}
        if started_on_pi and EVDEV_AVAILABLE:
            self.evdev_map = {
                # Pfeiltasten
                ecodes.KEY_UP: UP,
                ecodes.KEY_DOWN: DOWN,
                ecodes.KEY_LEFT: LEFT,
                ecodes.KEY_RIGHT: RIGHT,

                # WASD
                ecodes.KEY_W: UP,
                ecodes.KEY_S: DOWN,
                ecodes.KEY_A: LEFT,
                ecodes.KEY_D: RIGHT,

                # Aktionen
                ecodes.KEY_ENTER: CONFIRM,
                ecodes.KEY_KPENTER: CONFIRM,
                ecodes.KEY_ESC: BACK,
                ecodes.KEY_SPACE: DROP,
                ecodes.KEY_C: HOLD
            }
            self.start_evdev_keyboard()

        self.joy_map = {
            0: DROP,
            1: CONFIRM,
            2: BACK,
            3: HOLD
        }

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
    
    # Custom Input delay pro Aktion (z.B. schnelleres Movement, langsameres Jumping)
    def is_pressed_custom(self, action, delay):
        now = time.time()

        with self.pressed_lock:
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
        # falls ein Joystick bereits angeschlossen ist, müssen wir gar nicht
        # nach einer Tastatur suchen – dann überspringen wir die Wartephase
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            print("Controller(s) vorhanden – überspringe Tastatur-Suche")
            return None

        candidates = []
        for path in list_devices():
            dev = InputDevice(path)
            if "keyboard" in dev.name.lower():
                candidates.append(dev)
                print(f"Gefundene Keyboard-Candidate: {dev.name} ({dev.path})")

        if not candidates:
            print("Keine Tastaturen gefunden")
            return None

        print("Bitte Taste auf Tastatur ODER Controller drücken...")

        while True:
            # Prüfe eventuell während der Wartephase angeschlossene Joysticks
            # (z.b. Joy‑Cons, Controller usw.). Pygame meldet keine Neuanschlüsse
            # per Event, deshalb prüfen wir die Anzahl periodisch.
            pygame.joystick.quit()
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                print("Controller angeschlossen – breche Tastatur-Wartephase ab")
                return None

            # --- Prüfe evdev Keyboard ---
            r, _, _ = select.select([d.fd for d in candidates], [], [], 0.05)
            for fd in r:
                dev = next(d for d in candidates if d.fd == fd)
                for event in dev.read():
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        print(f"Aktive Tastatur: {dev.name} ({dev.path})")
                        return dev
                    
            # --- Prüfe Controller (Pygame) ---
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION):
                    print("Controller erkannt – Wartephase beendet")
                    return None


    def start_evdev_keyboard(self):
        keyboard = self._find_first_active_keyboard()
        if not keyboard:
            return

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
                mapped = self.joy_map.get(event.button)
                if mapped:
                    self.pressed.add(mapped)

            elif event.type == pygame.JOYBUTTONUP:
                mapped = self.joy_map.get(event.button)
                if mapped:
                    self.pressed.discard(mapped)