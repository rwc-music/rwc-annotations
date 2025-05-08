# AIST_RWC-MDB_BEAT_specification

## Example Annotations
```
4	4	384
49	49	48
93	93	96
137	137	144
182	182	384
226	226	48
271	271	96
315	315	144
360	360	384
404	404	48
449	449	96
493	493	144
537	537	384
582	582	48
626	626	96
671	671	144
715	715	384
760	760	48
```

## Format Specification

- Frame-rate: 100 Hz
- Column 1: Start position of the beat in frames (e.g., 4 = 40 ms)
- Column 2: End position of the beat in frames
- Column 3: Beat position in musical time
    - 384: beginning of the measure
    - 48: first quarter note
    - 96: second quarter note
    - 144: fourth quarter note
