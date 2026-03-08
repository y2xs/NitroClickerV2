# ⚡ NitroClickerV2
> A high-performance, multi-threaded Python auto-clicker built for speed and precision.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![Tech: Pynput](https://img.shields.io/badge/Library-Pynput-brightgreen)

**NitroClickerV2** is the evolution of simple automation. Unlike standard scripts that can hang or lag your system, V2 utilizes background threading to separate the clicking logic from the listener, ensuring that your stop-commands are registered instantly even at extremely high CPS (Clicks Per Second).

---

## ✨ Features
* **🏎️ Ultra-High Frequency:** Capable of sub-millisecond delays for maximum clicking speed.
* **🧵 Threaded Execution:** Runs the clicking loop on a separate thread to prevent UI or system freezing.
* **⌨️ Global Hotkeys:** Control the clicker (Start/Stop/Exit) from anywhere on your OS without needing to focus the terminal.
* **🛡️ Human-Like Variance:** Optional randomization logic to prevent bot-detection in specific environments.
* **🪶 Lightweight:** Minimal dependencies and extremely low CPU/RAM footprint.

---

## 🏗 Technical Architecture
NitroClickerV2 is built using the `pynput` library for low-level input control. 

1. **The Listener:** A keyboard listener runs in a non-blocking loop, waiting for the defined trigger keys.
2. **The Worker:** A custom thread class manages the mouse controller, cycling through clicks as long as the `active` flag is set to true.
3. **The Logic:** When a hotkey is pressed, the listener toggles a thread-safe boolean, allowing the worker to start or stop clicking without terminating the entire script.

---

## 📜 License & Warranty
This project is licensed under the **MIT License**. 

**What this means:** You are free to use, copy, modify, and distribute this software for any purpose (even commercially) as long as you include the original copyright notice.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.** The author is not liable for any account bans, hardware wear-and-tear (mouse switches), or accidental clicks resulting from the use of this software.

See the [LICENSE](./LICENSE) file for the full legal text.
