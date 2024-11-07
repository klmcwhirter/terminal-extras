'''color_scheme_watcher.py - patch boss instance to use custom on_system_color_scheme_change

Install in the `~/.config/kitty` dir and configure in `kitty.conf` with:

`watcher color_scheme_watcher.py`

'''

from kitty.boss import Boss
from kitty.fast_data_types import get_boss
from kitty.utils import log_error

# **CUSTOMIZE** with your theme names
THEME_DARK = 'Solarized Dark'
THEME_LIGHT = 'Solarized Light'

# keys are possible input strings; values are theme name ]
_SCHEME_MAP_ = {
    'no_preference': THEME_LIGHT,
    'dark': THEME_DARK,
    'light': THEME_LIGHT,
}


def scheme2theme(scheme: str) -> str:
    return _SCHEME_MAP_[scheme] if scheme in _SCHEME_MAP_ else ''


def _watcher_print(*args, **kwargs) -> None:
    '''prepend message with the string `WATCHER: `

    This is useful for troubleshooting with `kitty --debug-gl`.
    '''
    print(*[__file__, '::', *args], **kwargs)


# from kitty.boss::Boss
# def on_system_color_scheme_change(boss: Boss, appearance: Literal['light', 'dark', 'no_preference']) -> None:
#     _watcher_print('system color theme changed:', appearance)


def on_scheme_change(scheme: str, *args, **kwargs) -> None:
    _watcher_print(f'on_scheme_change: {scheme=}, args={args}, kwargs={kwargs}')

    theme = scheme2theme(scheme)
    _watcher_print(f'on_scheme_change: {theme=}')

    if theme:
        boss.kitten('themes', theme)


boss: Boss = get_boss()
if boss:
    # --------------
    # HACK ALERT !!! "monkey patch" the existing method ...
    # --------------
    boss.on_system_color_scheme_change = on_scheme_change
else:
    log_error(f'{__file__}: could not get Boss instance')
