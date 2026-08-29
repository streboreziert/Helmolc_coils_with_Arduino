# Helmholtz coil driver

Arduino + L298N driver for a **rotating uniform field**. Eight PWM steps around the compass, pot-set frequency, LCD readout. This is the coil pair used in the MMML remagnetization experiments.

The file that ships the firmware was historically named `Run_sin_wave.py` — it is **Arduino C++**, not Python. A proper sketch lives at [`helmholtz_rotate.ino`](helmholtz_rotate.ino).

Field math (center + B(z)): [helmholtz-field](https://github.com/streboreziert/helmholtz-field) · [lab](https://robertstreize.com/lab.html#helmholtz)

---

## Bench

- Four coil directions: EAST 7, WEST 8, NORTH 10, SOUTH A0
- L298N enables: ENA 6, ENB 9
- Frequency pot: A2 (mapped ~1–20 Hz)
- 16×2 LCD on 12, 11, 5, 4, 3, 2

Sequence is an 8-step rotating vector, not a true sine — close enough for a viscous-sphere experiment, cheap enough for a student bench.

```bash
python3 field.py --r 7 --n 140 --i 1.2 --z 0
python3 field.py --r 7 --n 140 --i 1.2 --scan
```

`--scan` prints B from z = −R … +R so you can see the Helmholtz flat.

Site: [robertstreize.com](https://robertstreize.com/project.html?repo=Helmolc_coils_with_Arduino)

MIT · Roberts Treize · MMML Lab
