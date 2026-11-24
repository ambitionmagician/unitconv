# unitconv

Converts values between common units from the command line — length,
mass, temperature, volume, speed, data, and time — with friendly unit
names and clean errors when a conversion makes no sense.

## Quickstart

```
python3 unitconv.py 5 km mi
python3 unitconv.py --list
```

## Usage

```
unitconv.py VALUE FROM TO [--precision N]
unitconv.py --list [CATEGORY]
```

Units are case-insensitive and common aliases work (`meters`,
`celsius`, `pounds`). Temperature handles offsets correctly — it is
not a simple factor. Data units use 1024 steps (1 GB = 1024 MB).

## Examples

```
$ python3 unitconv.py 5 km mi
5.0 km = 3.10686 mi
$ python3 unitconv.py 100 c f
100.0 c = 212 f
$ python3 unitconv.py 32 f c
32.0 f = 0 c
$ python3 unitconv.py 5 km lb
Cannot convert between categories: length and mass   (exit code 2)
```

## Configuration

None — all options are command-line flags.

## Limitations

- No currency, compound units (like kg/m^3), or cooking approximations
  beyond the standard volume set.
- Results are floating-point; not intended for metrology.

## License

MIT — see `LICENSE`.

By Dr. Brent Allen Jensen, Radical Blueprinting Research.

## Support this work

If this tool saved you time, you can support more open work like it:

- **BTC:** `15McijPo79Zx58NGyEf2PvaPtGqGmpztWn`
- **ETH:** `0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B`

Thank you.
