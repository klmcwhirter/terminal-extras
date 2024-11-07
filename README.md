# kitty-extras
Stuff I have used to customize the kitty terminal


## color_scheme_watcher

This is an implementation of a kitty [watcher](https://sw.kovidgoyal.net/kitty/launch/#watchers) that is doing the job of monitoring the dark/light color scheme system changes for me. I am hesitant to share the code because it is an unorthodox approach; but it works for me.

### Assumptions:

- This is a big one - I side-stepped the suggestion for a mutex because I only ever have a single instance of kitty open at a time. I have been working this way for years. But if I were using a tiling window manager and opening new instances every time (instead of just a tab / window), this design would not work reliably.

- Customize the constants at the top of [color_scheme_watcher.py](./color_scheme_watcher/color_scheme_watcher.py) with your prefered theme names.

### Setup

- copy the `color_scheme_watcher.py` module to `~/.config/kitty`
- add `watcher color_scheme_watcher.py` to `~/.config/kitty/kitty.conf`
- customize theme names in `color_scheme_watcher.py`
