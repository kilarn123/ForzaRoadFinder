# Forza Road Finder

A tiny real-time screen tool that helps you find the **last un-driven roads** in Forza Horizon's map completion.

On the in-game map, drivable roads render as grey (`#808080`). This tool captures your game monitor, recolors those grey road pixels to **bright pink (`#FF00FF`)**, mutes everything else, and shows the result in a separate window — ideal on a second monitor while you play on the main screen.

## How it works

1. Grab a frame from the game monitor (fast, via `mss`).
2. Build a mask of pixels matching grey `#808080` (with adjustable tolerance) using `numpy`.
3. Thicken the matched road lines and set them to bright pink.
4. Desaturate + darken the background so the pink pops, then display via OpenCV.

The loop runs continuously, so panning/zooming the in-game map updates live.

## Requirements

- Python 3.8+
- A dual-monitor setup is ideal (game on one screen, this tool on the other), but not required.

## Setup

```sh
pip install -r requirements.txt
```

Installs `mss`, `numpy`, and `opencv-python`.

## Usage

```sh
python road_finder.py
```

1. On startup the console **prints your detected monitors** — note the index of the screen running the game.
2. If that index isn't `1`, edit `CAPTURE_MONITOR` at the top of [`road_finder.py`](road_finder.py).
3. Drag the **Road Finder** window onto your second monitor and maximize it.
4. Open Forza's map on your primary screen — grey roads light up pink.
5. Press **`q`** (or close the window) to quit.

## Controls

Four live sliders at the top of the window:

| Slider  | Default | What it does |
|---------|---------|--------------|
| `tol`   | `0`     | How far a pixel can be from grey `128` and still count. `0` = exact `#808080` match. |
| `grey`  | `0`     | Max spread between R/G/B channels (keeps matches to true neutral greys). `0` = strict. |
| `dim`   | `70`    | How much to darken/desaturate the non-road background (%). Higher = pink pops more. |
| `thick` | `6`     | Thicken thin road lines by this many pixels so they're easy to spot. |

**Recommended defaults:** `tol=0`, `grey=0`, `thick=6` — Forza's roads are exactly `#808080`, so no tolerance is needed and the thickening does the visibility work.

## Tuning tips

- **Roads missed?** Raise `tol` (and maybe `grey`) a little.
- **Too much flips pink** (grey UI/text)? Lower `tol`/`grey`.
- **Pink hard to see?** Raise `dim` and/or `thick`.
- **Wrong screen shown?** Change `CAPTURE_MONITOR` to the other monitor index from the startup printout.

## Configuration

Constants at the top of [`road_finder.py`](road_finder.py):

| Name              | Purpose |
|-------------------|---------|
| `TARGET`          | Grey channel value to match (`128` = `#808080`). |
| `PINK`            | Highlight color in BGR (default bright pink `#FF00FF`). |
| `CAPTURE_MONITOR` | `mss` monitor index of the game screen (`1`, `2`, …; `0` is the all-monitors box). |

## Files

- [`road_finder.py`](road_finder.py) — the entire tool.
- [`requirements.txt`](requirements.txt) — dependencies.
