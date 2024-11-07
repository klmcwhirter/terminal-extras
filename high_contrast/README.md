# Accessibility D-Bus Instance on Fedora

## Background

- [AT-SPI](https://www.freedesktop.org/wiki/Accessibility/AT-SPI2/)
- [Linux Foundation - a11y d-bus ](https://wiki.linuxfoundation.org/accessibility/d-bus)
- [flatpak discussion](https://github.com/flatpak/flatpak/issues/79)

## Observations
- separate broker on Fedora 41

From ps listing:

```bash
/usr/bin/dbus-broker-launch --config-file=/usr/share/defaults/at-spi2/accessibility.conf --scope user
```

## Discovering D-Bus Address

There is a separate bus for a11y settings.

> Make sure the at-spi2-core is installed.

```bash
xprop -root | grep SPI
```

```
AT_SPI_BUS(STRING) = "unix:path=/run/user/1000/at-spi/bus"
```

But interacting with this bus is not required (and not really possible because it is only accessible to `root` by default).

## Monitoring High Contrast Signals

Pre-requisite on Fedora 41:

* requires the fedora pkg for selinux support, etc.
```bash
sudo dnf install python3-dbus-next
```

Run it and change High Contrast setting in Settings -> Accessibility -> Seeing ...

```bash
python high_contrast_monitor.py
```

> Note the lines with interface_name='org.freedesktop.appearance'

```
BUS='org.freedesktop.portal.Desktop'
PATH='/org/freedesktop/portal/desktop'
INTERFACE='org.freedesktop.portal.Settings'
SIGNAL=SettingChanged

Waiting for signals ...
          
setting_changed: interface_name='org.gnome.desktop.a11y.interface', changed_properties='high-contrast', invalidated_properties=<dbus_next.signature.Variant ('b', True)>
setting_changed: interface_name='org.gnome.desktop.a11y.interface', changed_properties='high-contrast', invalidated_properties=<dbus_next.signature.Variant ('b', True)>
setting_changed: interface_name='org.gnome.desktop.interface', changed_properties='gtk-theme', invalidated_properties=<dbus_next.signature.Variant ('s', HighContrast)>
setting_changed: interface_name='org.freedesktop.appearance', changed_properties='contrast', invalidated_properties=<dbus_next.signature.Variant ('u', 1)>
setting_changed: interface_name='org.gnome.desktop.a11y.interface', changed_properties='high-contrast', invalidated_properties=<dbus_next.signature.Variant ('b', False)>
setting_changed: interface_name='org.gnome.desktop.a11y.interface', changed_properties='high-contrast', invalidated_properties=<dbus_next.signature.Variant ('b', False)>
setting_changed: interface_name='org.gnome.desktop.interface', changed_properties='gtk-theme', invalidated_properties=<dbus_next.signature.Variant ('s', Adwaita)>
setting_changed: interface_name='org.freedesktop.appearance', changed_properties='contrast', invalidated_properties=<dbus_next.signature.Variant ('u', 0)>
^C
```

## Monitoring with `dbus-monitor`

```bash
dbus-monitor --session "type=signal,path=/org/freedesktop/portal/desktop,arg0namespace=org.gnome.desktop.a11y.interface,arg1=high-contrast,interface=org.freedesktop.portal.Settings,member=SettingChanged"
```

```
signal time=1730991180.191606 sender=:1.83 -> destination=(null destination) serial=944 path=/org/freedesktop/portal/desktop; interface=org.freedesktop.portal.Settings; member=SettingChanged
   string "org.gnome.desktop.a11y.interface"
   string "high-contrast"
   variant       boolean true
```

```bash
dbus-monitor --session "type=signal,path=/org/freedesktop/portal/desktop,arg0namespace=org.freedesktop.appearance,interface=org.freedesktop.portal.Settings,member=SettingChanged"
```

```
signal time=1731010222.356979 sender=:1.83 -> destination=(null destination) serial=1702 path=/org/freedesktop/portal/desktop; interface=org.freedesktop.portal.Settings; member=SettingChanged
   string "org.freedesktop.appearance"
   string "contrast"
   variant       uint32 1

signal time=1731010224.521052 sender=:1.83 -> destination=(null destination) serial=1706 path=/org/freedesktop/portal/desktop; interface=org.freedesktop.portal.Settings; member=SettingChanged
   string "org.freedesktop.appearance"
   string "contrast"
   variant       uint32 0
```

## Introspect with busctl

```bash
busctl --user introspect org.freedesktop.portal.Desktop /org/freedesktop/portal/desktop org.freedesktop.portal.Settings
```

```
NAME                            TYPE      SIGNATURE RESULT/VALUE FLAGS
.Read                           method    ss        v            deprecated
.ReadAll                        method    as        a{sa{sv}}    -
.ReadOne                        method    ss        v            -
.version                        property  u         2            emits-change
.SettingChanged                 signal    ssv       -            -
```
