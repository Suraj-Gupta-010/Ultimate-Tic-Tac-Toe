from time import sleep
from pynput.mouse import Controller as MouseController
from pynput import keyboard
from pyperclip import copy
import tkinter as tk
import threading

mouse = MouseController()

start = None
small_gap = None
big_gap = None

overlay_running = False
overlay_root = None
canvas = None


# ── Overlay (runs on main thread via after()) ─────────────────────────

def start_overlay():
    global overlay_root, canvas

    if overlay_root is not None:
        return  # already exists

    overlay_root = tk.Tk()
    overlay_root.attributes('-topmost', True)
    overlay_root.attributes('-alpha', 0.4)
    overlay_root.overrideredirect(True)

    w = overlay_root.winfo_screenwidth()
    h = overlay_root.winfo_screenheight()
    overlay_root.geometry(f"{w}x{h}+0+0")

    canvas = tk.Canvas(overlay_root, width=w, height=h,
                       bg='black', highlightthickness=0)
    canvas.pack()

    overlay_root.after(100, tick)
    overlay_root.mainloop()          # blocks – call from main thread only


def tick():
    """Redraws the overlay every 100 ms; also handles show/hide."""
    global overlay_root, canvas

    if overlay_root is None:
        return

    canvas.delete("all")

    if overlay_running and start and small_gap and big_gap:
        for letter in "ABCDEFGHI":
            for num in range(1, 10):
                x, y = move_to_position(letter, num)
                r = 5
                canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")
                canvas.create_text(x, y - 12, text=f"{letter}{num}",
                                   fill="white", font=("Arial", 8))

    overlay_root.after(100, tick)


def show_overlay():
    global overlay_running, overlay_root
    overlay_running = True
    # If the window doesn't exist yet, create it on the main thread via a flag.
    # We schedule it with after(0) so it runs inside mainloop.
    if overlay_root is not None:
        overlay_root.deiconify()


def hide_overlay():
    global overlay_running
    overlay_running = False
    if overlay_root is not None:
        overlay_root.withdraw()


# ── Grid maths ────────────────────────────────────────────────────────

def move_to_position(board: str, pos: int) -> tuple[int, int]:
    board_index = ord(board) - ord('A')

    board_x = board_index % 3
    board_y = board_index // 3

    cell_x = (pos - 1) % 3
    cell_y = (pos - 1) // 3

    board_size = 3 * small_gap

    x = start[0] + board_x * (board_size + big_gap) + cell_x * small_gap
    y = start[1] + board_y * (board_size + big_gap) + cell_y * small_gap

    return int(x), int(y)


# ── Sweep ─────────────────────────────────────────────────────────────

def run_sweep():
    print("\n--- SWEEP START ---\n")
    for letter in "ABCDEFGHI":
        print(f"Board {letter}")
        for number in range(1, 10):
            x, y = move_to_position(letter, number)
            mouse.position = (x, y)
            print(f"  Cell {number} → ({x}, {y})")
            sleep(0.12)


# ── Keyboard listener (background thread) ────────────────────────────

_listener_done = threading.Event()

def on_press(key):
    global start, small_gap, big_gap

    try:
        ch = key.char.lower()
    except AttributeError:
        return

    if ch == 's':
        start = mouse.position
        print(f"[S] Start (A1): {start}")

    elif ch == 'g':
        if start is None:
            print("Set start first (press S).")
            return
        pos = mouse.position
        small_gap = pos[0] - start[0]
        print(f"[G] Small gap: {small_gap}")

    elif ch == 'o':
        if overlay_running:
            hide_overlay()
            print("Overlay OFF")
        else:
            show_overlay()
            print("Overlay ON")

    elif ch == 'b':
        if start is None or small_gap is None:
            print("Complete S and G steps first.")
            return

        pos = mouse.position
        dx = pos[0] - start[0]
        board_size = 3 * small_gap
        big_gap_val = dx - board_size

        # write into the global so move_to_position() can use it
        globals()['big_gap'] = big_gap_val
        print(f"[B] Big gap: {big_gap_val}")

        print("\nStarting sweep in 2 seconds...")
        sleep(2)
        run_sweep()

        code = f"{start[0]}:{start[1]}.{small_gap}.{big_gap_val}"
        print(f"\nCalibration code: {code}")
        copy(code)
        print("Copied to clipboard!")

        show_overlay()
        _listener_done.set()   # signal main thread to stop listener


def keyboard_thread():
    with keyboard.Listener(on_press=on_press) as listener:
        _listener_done.wait()   # block until 'b' finishes
        listener.stop()


# ── Entry point ───────────────────────────────────────────────────────

print("Calibration steps:")
print("  1. Hover over cell A1 and press  S")
print("  2. Hover over cell A2 and press  G")
print("  3. Hover over cell B1 and press  B  (sweep will run)\n")
print("Press  'O' at any time to toggle the overlay.\n")

# Keyboard listener runs in background; tkinter runs on main thread.
t = threading.Thread(target=keyboard_thread, daemon=True)
t.start()

start_overlay()   # blocks on main thread until window is closed
