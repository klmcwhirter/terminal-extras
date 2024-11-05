# kitty-extras
Stuff I have used to customize the kitty terminal


## color_scheme_watcher

This is an implementation of a kitty [watcher](https://sw.kovidgoyal.net/kitty/launch/#watchers) that is doing the job of monitoring the dark/light color scheme system changes for me. I am hesitant to share the code because it is an unorthodox approach; but it works for me.

### Assumptions:

- This is a big one - I side-stepped the suggestion for a mutex because I only ever have a single instance of kitty open at a time. I have been working this way for years. But if I were using a tiling window manager and opening new instances every time (instead of just a tab / window), this design would not work reliably.

- No new configuration needed; and cooperates with the themes kitten. It works by assuming a sub-dir named ~/.config/kitty/themes where there exists 1 and only 1 file for each of `themes/dark-\*.conf` and `themes/light-\*.conf`. As system changes occur the appropriate file is copied to `~/.config/kitty/current-theme.conf` and `load_config_file` is called.

That way the themes to use for dark/light schemes can be managed on the filesystem (perhaps via `themes --dump-theme ...` outputting to the appropriate named file) and I can use the themes kitten to occasionally select a higher contrast theme.

### Setup

- copy the `color_scheme_watcher.py` module to `~/.config/kitty`
- add `watcher color_scheme_watcher.py` to `~/.config/kitty/kitty.conf`
- create `~/.config/kitty/themes/` sub-dir
- place a `light-my theme name.conf` and a `dark-my theme name.conf` file in the `~/.config/kitty/themes/` sub-dir.

These can be acquired by using the `kitty +kitten themes` kitten one at a time and moved into place.
