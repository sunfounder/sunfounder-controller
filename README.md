# SunFounder Controller

SunFounder Controller provides a WebSocket-based controller for Raspberry Pi robots. It enables real-time bidirectional communication between a web/mobile client and your robot over the local network.

## Quick Start

Install from source:

```shell
git clone https://github.com/sunfounder/sunfounder-controller.git
cd sunfounder-controller
sudo python3 setup.py install
```

## Usage

```python
from sunfounder_controller import SunFounderController

sc = SunFounderController()

# Start the WebSocket server
sc.start()

# Send a value to connected clients
sc.set('A_region', value)

# Read a value from clients
value = sc.get('A')
```

## Debug Mode

Enable debug logging to troubleshoot WebSocket connections and message flow:

```shell
SF_CONTROLLER_DEBUG=1 python3 your_script.py
```

Or set it in your script before importing:

```python
import os
os.environ['SF_CONTROLLER_DEBUG'] = '1'
```

Debug output is prefixed with `[SF_CONTROLLER_DEBUG]` and includes timestamps, connection/disconnection events, raw message dumps, and parse errors.

## Examples

See the `examples/` directory. Run with:

```bash
cd examples
sudo python3 xxx.py
```

Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop.

## API Reference

| Method | Description |
|--------|-------------|
| `start()` | Start the WebSocket server on port 8765 |
| `get(key='A', default=None)` | Get a value from `recv_dict` by key |
| `getall()` | Return the full `recv_dict` |
| `set(key='A_region', value=None)` | Send a value to clients via `send_dict` |
| `set_name(name)` | Set the controller name sent to clients |
| `set_type(type)` | Set the controller type sent to clients |
| `close()` | Shut down the WebSocket server |

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

## About SunFounder

SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strive to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project.

## Contact

- Website: [sunfounder.com](https://www.sunfounder.com)
- Email: service@sunfounder.com
