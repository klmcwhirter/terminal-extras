'''color_scheme_watcher.py - patch boss instance to use custom on_system_color_scheme_change

Install in the `~/.config/kitty` dir and configure in `kitty.conf` with:

`watcher color_scheme_watcher.py`

'''

import glob
import os
import shutil

from kitty.boss import Boss
from kitty.constants import config_dir
from kitty.fast_data_types import get_boss
from kitty.utils import log_error


_CURR_THEME_ = os.path.join(config_dir, 'current-theme.conf')
_SCHEME_MAP_ = {
    'no_preference': 'light',
    'dark': 'dark',
    'light': 'light',
}


def _watcher_print(*args, **kwargs) -> None:
    '''prepend message with the string `WATCHER: `
    
    This is useful for troubleshooting with `kitty --debug-gl`.
    '''
    print(*['WATCH: ', *args], **kwargs)


def change_color_scheme(scheme: str):
    '''Copy the file for the requested scheme

    Assumes a sub-dir `~/.config/kitt/themes` which contains 1 and only 1 file for each of:
    - dark-*.conf
    - light-*.conf

    If there are multiples - selects the first file name returned by `glob.glob`.

    Based on the requested scheme the appropriate file is copied to `__CURR_THEME__`
    which is purposefully set to the same default file name used by the `themes` kitten as output.
    '''
    def theme_file_from_scheme(scheme: str) -> str:
        pattern = os.path.join(config_dir, f'themes/{scheme}-*.conf')
        return glob.glob(pattern)[0]

    # _watcher_print(f'{scheme=}')

    theme_file = theme_file_from_scheme(scheme)
    # _watcher_print(f'{theme_file=}')

    shutil.copyfile(theme_file, _CURR_THEME_)


def color_scheme_to_use(mode: str) -> str:
    '''return the requested color scheme light or dark'''
    rc = None
    _watcher_print(f'{mode=}')

    for k, v in _SCHEME_MAP_.items():
        if k in mode:
            rc = v
            break

    return rc

# from kitty.boss::Boss
# def on_system_color_scheme_change(boss: Boss, appearance: Literal['light', 'dark', 'no_preference']) -> None:
#     _watcher_print('system color theme changed:', appearance)

def on_system_color_scheme_change(mode: str, *args, **kwargs) -> None:
    # _watcher_print(f'system color theme changed: {mode=}, args={args}, kwargs={kwargs}')

    scheme = color_scheme_to_use(mode)
    if scheme:
        # _watcher_print(f'{scheme=}')
        change_color_scheme(scheme)
        boss.load_config_file()


boss: Boss = get_boss()
if boss:
    boss.on_system_color_scheme_change = on_system_color_scheme_change
else:
    log_error('WATCHER: could not get Boss instance')
