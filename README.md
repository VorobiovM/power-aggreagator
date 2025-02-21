# Power aggregator

Drag-n-drop power aggreagtor to model synthetic consumption data.

## Installation

Before starting download Git and Pyhton3.11+.

### Windows (Powershell)

```
git clone https://github.com/VorobiovM/power-aggreagator.git
cd power-aggreagator
python -m venv .venv
& .venv/Scripts/Activate.ps1
pip install -e .[dev]
python src/power_aggregator/__main__.py
```

### Linux

```
git clone https://github.com/VorobiovM/power-aggreagator.git
cd power-aggreagator
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python src/power_aggregator/__main__.py
```

## Building executable

Before building application, frist follow installation steps.

```
pip install -e .[dist]
pyinstaller aggregator.spec
```

### Contribution:
- [Fridge icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/fridge)
- [Air conditioning icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/air-conditioning)
- [Washing machine icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/washing-machine)
- [Charger icons created by Iconic Panda - Flaticon](https://www.flaticon.com/free-icons/charger)
