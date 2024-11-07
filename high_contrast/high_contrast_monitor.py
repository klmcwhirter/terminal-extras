import asyncio

from dbus_next.aio import MessageBus

BUS='org.freedesktop.portal.Desktop'
PATH='/org/freedesktop/portal/desktop'
INTERFACE='org.freedesktop.portal.Settings'

async def main():
    bus = await MessageBus().connect()
    # the introspection xml would normally be included in your project
    introspection = ''
    # Note: had to comment out power-saver-enabled element because of validation error.
    with open('settings-orig.xml', 'r', encoding='utf-8') as f:
        introspection = f.read()
    # print(f'{introspection=}')

    def setting_changed(interface_name, changed_properties, invalidated_properties):
        '''Watch for changes to the High Contrast setting'''
        print(f'setting_changed: {interface_name=}, {changed_properties=}, {invalidated_properties=}')

    desktop = bus.get_proxy_object(BUS, PATH, introspection)
    settings = desktop.get_interface(INTERFACE)
    # print(f'{dir(settings)}')

    settings.on_setting_changed(setting_changed)

    print(f'''
{BUS=}
{PATH=}
{INTERFACE=}
SIGNAL=SettingChanged

Waiting for signals ...
          ''')

    await asyncio.Event().wait()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print()
