"""Globally defined stream names.

These stream declarations document the major system streams that are used
internally in an IOTile device to log important system events.  Each
declaration includes a description of how to interpret the contents of data
logged to that stream.

Most of these streams are system inputs, which means they are presented to the
running sensor-graph for actions but ignored by default if no actions react to
them.
"""

from iotile.sg import DataStream

def declare_stream(string_name):
    """Create a StreamDeclaration from a string name.

    This will encode the string name into a 16-bit stream
    identifier.

    Args:
        string_name (str): The human-readable name of the stream.

    Returns:
        int: The stream declaration.
"""

    return DataStream.FromString(string_name).encode()


SYSTEM_RESET = declare_stream('system input 1024')
"""Logs a reading every time the IOTile device is reset with SensorGraph running.

This stream records system reboots.  It is only used when there is a
programmed sensor_graph script running in the device.  It can be used for
debugging if a system reboot is unexpected or for keeping track of when the
device's internal uptime is expected to reset back to zero.

The contents of each reading logged in this stream are an oquare integer value
that is architecture specific and describes the technical cause of the reset
(such as power on, brownout, etc).
"""

NORMAL_TICK = declare_stream('system input 2')
"""Sent every 10 seconds to trigger periodic sensor graph rules.

This is the base tick that forms that periodic input for most long running
timers inside the sensor_graph subsystem.  It cannot be turned off or
configured.
"""

FAST_TICK = declare_stream('system input 3')
"""A fast 1 second tick that is disabled by default.

Technically this tick can be user controlled and set to a value other than one
second but it is controlled internally by the sensor-graph compiler so if you
want to use it for another purpose, you need to make sure it is not referenced
by any rules generated by your .sgf file.
"""

USER_TICK_1 = declare_stream('system input 5')
"""A user controlled tick.

This tick can take any integer second value.  It defaults to being disabled.
These ticks are most valuable for implementing field-programmable timers that
are easy to change with a simple RPC.
"""

USER_TICK_2 = declare_stream('system input 6')
"""A user controlled tick.

This tick can take any integer second value.  It defaults to being disabled.
These ticks are most valuable for implementing field-programmable timers that
are easy to change with a simple RPC.
"""

COMM_TILE_OPEN = declare_stream('system input 1025')
"""Sent when a communications tile opens its streaming interface.

The value in the stream is the address of the tile that opened its streaming
interface.  This input to sensor_graph can be used for entering high-power or
high-speed modes to send more data when there is a user actively connected to
the device.
"""

COMM_TILE_CLOSED = declare_stream('system input 1026')
"""Sent when a communications tile closes its streaming interface.

The value in the stream is the address of the tile the closed its streaming
interface.  This input can be used for leaving high-power or high-speed data
collection modes since there is not longer a user actively connected to the
device.
"""

DATA_CLEARED = declare_stream('system output 1027')
"""Logs a reading every time the sensor log subsystem receives a clear() command.

Each entry in this data stream marks the point in time where the sensor log
was cleared.  It can be used for debugging or forensic purposes if such a
clear was unexpected.  Internally it is used to ensure that there is always a
valid reading inside the sensor log to store the current highest allocated
reading id.
"""
