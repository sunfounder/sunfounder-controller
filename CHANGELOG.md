# Changelog

All notable changes to this project will be documented in this file.

## [0.0.4] - 2026-08-11

- Fix voice control (J key) repeating the last recognition result in `picarx_control.py`
- Add J-key ack protocol: device returns `1` on receipt (ack), then `0` when the action completes, so the App clears the pending command and repeated identical commands (e.g. consecutive "forward") trigger again
- Edge-triggered voice command execution (empty/None -> command)

## [0.0.2] - 2020-06-12

- New Release
