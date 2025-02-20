# Power aggregator

Drag-n-drop power aggreagtor to model synthetic consumption data.

## Installation

Before starting download Git and Pyhton3.11+.

```
git clone https://github.com/VorobiovM/power-aggreagator.git
cd power-aggreagator
python -m venv .venv
pip install -e .[dev]
python src/power_aggregator/__main__.py
```

## Building executable

```
pip install -e .[dist]
pyinstaller aggregator.spec
```

### Contribution:
- [Fridge icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/fridge)
- [Air conditioning icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/air-conditioning)
- [Washing machine icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/washing-machine)
