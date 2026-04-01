# 👾 Alien Attack — Space Shooter Game

A classic space shooter game built entirely with Python and **Tkinter** — no external game engines needed. Shoot down alien intruders, survive as long as possible, and climb the leaderboard.

---

## 🎮 Gameplay

- Move your ship left and right to dodge enemies
- Shoot bullets to destroy incoming alien intruders
- The game gets harder as your score increases
- If an intruder reaches the bottom — it's game over

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚀 Dynamic Difficulty | Speed and spawn rate increase every 50 points |
| 🏆 Leaderboard | Top 5 scores saved locally in `leaderboard.json` |
| ⚙️ Key Remapping | Fully customisable controls via the Settings menu |
| 👔 Boss Key | Press `Tab` to instantly hide the game with a fake work screen |
| ⚡ Cheat Code | Press `↑ ↓` during gameplay to activate 6-second invincibility (Power Mode) |
| 🖼️ Fallback Images | Runs even if custom image assets are missing |

---

## 🕹️ Controls

| Action | Default Key |
|---|---|
| Move Left | `←` Arrow |
| Move Right | `→` Arrow |
| Shoot | `Space` |
| Pause / Resume | Pause button (top right) |
| Boss Key | `Tab` |
| Cheat Code | `↑` then `↓` |

> All keys can be remapped in the **Settings** menu.

---

## 🚀 Getting Started

### Requirements
- Python 3.x
- Tkinter (included with Python by default)

### Run the game

```bash
python game.py
```

### Adding custom images (optional)

Place the following image files in the same directory as `game.py` for custom visuals:

| File | Used for |
|---|---|
| `shooter.png` | Player ship |
| `intruder.png` | Enemy alien |
| `bullet.png` | Bullet |
| `pause.png` | Pause button |
| `resume.png` | Resume button |
| `background.png` | Game background |
| `work_page.png` | Boss key fake screen |

> The game will run with built-in fallback shapes if any images are missing.

---

## 📁 Project Structure

```
├── game.py                # Main game file
├── leaderboard.json       # Auto-created when you first play
├── key_mappings.json      # Auto-created when you remap keys
└── README.md
```

---

## 🔭 Future Improvements

- [ ] Sound effects and background music
- [ ] Multiple enemy types
- [ ] Power-up drops
- [ ] High score display during gameplay
- [ ] Animated explosions
