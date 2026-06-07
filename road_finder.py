"""Forza Road Finder.

Captures one monitor in real time, recolors grey road pixels (#808080) to
bright pink (#FF00FF), and shows the result in a resizable window so you can
spot the last un-driven roads on the in-game map.

Usage:
    python road_finder.py

Controls (with the "Road Finder" window focused):
    tol  trackbar  - how far a pixel can be from grey 128 and still count
    grey trackbar  - max spread between R/G/B (keeps it to true neutrals)
    q              - quit
"""

import mss
import numpy as np
import cv2

# --- Config ---------------------------------------------------------------
TARGET = 128                       # grey #808080 channel value
PINK = np.array([255, 0, 255])     # BGR bright pink (#FF00FF)
CAPTURE_MONITOR = 1                # mss monitor index of the GAME screen
WINDOW = "Road Finder"
# --------------------------------------------------------------------------


def main():
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("tol", WINDOW, 0, 60, lambda v: None)    # color tolerance
    cv2.createTrackbar("grey", WINDOW, 0, 60, lambda v: None)   # max channel spread
    cv2.createTrackbar("dim", WINDOW, 70, 100, lambda v: None)   # darken non-road %
    cv2.createTrackbar("thick", WINDOW, 6, 6, lambda v: None)    # thicken roads (px)

    with mss.mss() as sct:
        # mss.monitors[0] is the virtual all-monitors box; 1..N are real screens.
        print("Detected monitors:")
        for i, m in enumerate(sct.monitors):
            print(f"  [{i}] {m}")
        if CAPTURE_MONITOR >= len(sct.monitors):
            raise SystemExit(
                f"CAPTURE_MONITOR={CAPTURE_MONITOR} but only "
                f"{len(sct.monitors) - 1} real monitor(s) found. "
                "Edit CAPTURE_MONITOR at the top of road_finder.py."
            )
        mon = sct.monitors[CAPTURE_MONITOR]
        print(f"Capturing monitor [{CAPTURE_MONITOR}] {mon}. Press 'q' to quit.")

        while True:
            frame = np.array(sct.grab(mon))[:, :, :3]  # BGRA -> BGR
            tol = cv2.getTrackbarPos("tol", WINDOW)
            gtol = cv2.getTrackbarPos("grey", WINDOW)
            dim = cv2.getTrackbarPos("dim", WINDOW)
            thick = cv2.getTrackbarPos("thick", WINDOW)

            b = frame[..., 0].astype(np.int16)
            g = frame[..., 1].astype(np.int16)
            r = frame[..., 2].astype(np.int16)

            near_grey = (
                (np.abs(b - TARGET) <= tol)
                & (np.abs(g - TARGET) <= tol)
                & (np.abs(r - TARGET) <= tol)
            )
            is_neutral = (
                (np.abs(b - g) <= gtol)
                & (np.abs(g - r) <= gtol)
                & (np.abs(b - r) <= gtol)
            )
            mask = (near_grey & is_neutral).astype(np.uint8)

            # Thicken thin road lines so they're easier to spot.
            if thick > 0:
                k = 2 * thick + 1
                mask = cv2.dilate(mask, np.ones((k, k), np.uint8))

            # Mute the background (desaturate + darken) so full-bright pink pops.
            grey_bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out = cv2.cvtColor(grey_bg, cv2.COLOR_GRAY2BGR)
            out = (out.astype(np.int16) * (100 - dim) // 100).astype(np.uint8)
            out[mask.astype(bool)] = PINK

            cv2.imshow(WINDOW, out)
            # waitKey also lets the window process trackbar/close events.
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            # Stop if the window was closed with the X button.
            if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
