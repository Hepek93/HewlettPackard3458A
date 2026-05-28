# HP3458A Python Library (Unofficial)

A Pythonic interface for controlling the **Keysight / HP 3458A 8½-Digit Digital Multimeter** using `pyvisa`.

## 📜 Licensing & Attribution
This project is licensed under the **MIT License**.  
**Important:** If you use this library, you must keep the original copyright notice. If you modify it, please attribute the original work to [Đorđe Novaković](https://github.com/Hepek93). 

*Note: For commercial support or custom features, please contact the author.*

## ⚠️ Safety Warning
The HP 3458A is a high-precision instrument capable of measuring high voltages (up to 1000V). This software is unofficial and interacts directly with the instrument hardware. Incorrect configurations or automation loops could potentially lead to unexpected behavior in a test environment. Use at your own risk. Always ensure your test setup is safe and your inputs do not exceed the instrument's maximum ratings before enabling automation.

## 🚀 Overview
The HP 3458A is the industry standard for high-precision metrology, but its native command set can be complex to automate. This library wraps those commands into a clean, Pythonic API, making it easy to configure NPLC, sub-ppm ranges, and data streaming without having to parse the 500-page manual for every script.

## Installation
```bash
pip install hp3458a
```

## Quick start

```python
from hp3458a import HP3458A

dmm = HP3458A("GPIB0::22::INSTR")

hp3458a.set_trigger_arm('HOLD')
hp3458a.set_voltage_dc_rang_res(10, 1E-6)
hp3458a.set_number_of_digits(8)
hp3458a.set_nplc(NPLC)
hp3458a.set_number_of_reading_per_trigger(1, 'AUTO')
hp3458a.set_trigger_event('AUTO')
hp3458a.set_memory_storage_mode('FIFO')
hp3458a.set_fixedz('OFF')
hp3458a.set_realtime_math('OFF')


hp3458a.set_trigger_arm('SGL',1)
hp3458a_data = hp3458a.read_memory(1,1,1).strip().split(',')
hp3458a_data.reverse()
hp3458a_data = [float(x) for x in hp3458a_data]
```

### Requirements

1. Python 3.8+
2. pyvisa-py
3. A valid VISA backend (pyvisa-py, NI-VISA, or Keysight IO Libraries)