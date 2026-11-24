#!/usr/bin/env python3
"""
Unit conversion command-line tool.

Examples:
    $ python unitconv.py 100 m km
    100 m = 0.1 km

    $ python unitconv.py 32 f c
    32 f = 0 c

    $ python unitconv.py 1 tb b
    1 tb = 8589934592 b
"""

import argparse
import sys

UNITS = {
    'length': {
        'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
        'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.344,
        'meters': 1.0, 'metres': 1.0, 'kilometers': 1000.0, 'kilometres': 1000.0,
        'inches': 0.0254, 'feet': 0.3048, 'yards': 0.9144, 'miles': 1609.344,
    },
    'mass': {
        'g': 1.0, 'kg': 1000.0, 't': 1000000.0, 'oz': 28.349523125, 'lb': 453.59237,
        'grams': 1.0, 'kilograms': 1000.0, 'tons': 1000000.0, 'tonnes': 1000000.0,
        'ounces': 28.349523125, 'pounds': 453.59237,
    },
    'temperature': {
        'c': {'offset': 0, 'factor': 1, 'to_base': lambda x: x + 273.15, 'from_base': lambda x: x - 273.15},
        'f': {'offset': -459.67, 'factor': 5.0/9.0, 'to_base': lambda x: (x + 459.67) * 5.0/9.0, 'from_base': lambda x: x * 9.0/5.0 - 459.67},
        'k': {'offset': 0, 'factor': 1, 'to_base': lambda x: x, 'from_base': lambda x: x},
        'celsius': {'offset': 0, 'factor': 1, 'to_base': lambda x: x + 273.15, 'from_base': lambda x: x - 273.15},
        'fahrenheit': {'offset': -459.67, 'factor': 5.0/9.0, 'to_base': lambda x: (x + 459.67) * 5.0/9.0, 'from_base': lambda x: x * 9.0/5.0 - 459.67},
    },
    'volume': {
        'ml': 0.001, 'l': 1.0, 'tsp': 0.00492892, 'tbsp': 0.0147868, 'cup': 0.236588, 'floz': 0.0295735, 'pt': 0.473176, 'qt': 0.946353, 'gal': 3.78541,
        'milliliters': 0.001, 'liters': 1.0, 'teaspoons': 0.00492892, 'tablespoons': 0.0147868, 'cups': 0.236588, 'fluidounces': 0.0295735, 'pints': 0.473176, 'quarts': 0.946353, 'gallons': 3.78541,
    },
    'speed': {
        'mps': 1.0, 'kmh': 1.0/3.6, 'mph': 0.44704, 'kn': 0.514444,
        'meterspersecond': 1.0, 'meterspersecond': 1.0, 'kilometersperhour': 1.0/3.6, 'kph': 1.0/3.6, 'milesperhour': 0.44704, 'knots': 0.514444,
    },
    'data': {
        'b': 1.0, 'bit': 1.0/8.0, 'kb': 1024.0, 'mb': 1024.0**2, 'gb': 1024.0**3, 'tb': 1024.0**4,
        'bytes': 1.0, 'bits': 1.0/8.0, 'kilobytes': 1024.0, 'kilobyte': 1024.0, 'megabytes': 1024.0**2, 'megabyte': 1024.0**2,
        'gigabytes': 1024.0**3, 'gigabyte': 1024.0**3, 'terabytes': 1024.0**4, 'terabyte': 1024.0**4,
    },
    'time': {
        's': 1.0, 'min': 60.0, 'h': 3600.0, 'd': 86400.0, 'wk': 604800.0,
        'seconds': 1.0, 'minutes': 60.0, 'hours': 3600.0, 'days': 86400.0, 'weeks': 604800.0,
    },
}

def normalize_unit(unit):
    unit_lower = unit.lower()
    for category, units in UNITS.items():
        if unit_lower in units:
            return category, unit_lower
    return None, None

def list_units(category=None):
    categories = UNITS.keys() if category is None else [category]
    for cat in categories:
        if cat not in UNITS:
            print(f"Unknown category: {cat}", file=sys.stderr)
            sys.exit(2)
        print(f"{cat}: {', '.join(sorted(UNITS[cat].keys()))}")

def convert(value, from_unit, to_unit):
    from_cat, from_norm = normalize_unit(from_unit)
    to_cat, to_norm = normalize_unit(to_unit)
    
    if from_cat is None or to_cat is None:
        print("Unknown unit", file=sys.stderr)
        sys.exit(2)
    
    if from_cat != to_cat:
        print(f"Cannot convert between categories: {from_cat} and {to_cat}", file=sys.stderr)
        sys.exit(2)
    
    if from_cat == 'temperature':
        to_kelvin = UNITS[from_cat][from_norm]['to_base'](value)
        result = UNITS[from_cat][to_norm]['from_base'](to_kelvin)
    else:
        result = value * UNITS[from_cat][from_norm] / UNITS[from_cat][to_norm]
    
    return result

def format_result(value, precision):
    if value == 0:
        return "0"
    s = f"{value:.{precision}g}"
    return s.rstrip('0').rstrip('.') if '.' in s else s

def main():
    parser = argparse.ArgumentParser(description='Convert values between common units.')
    parser.add_argument('value', nargs='?', type=float, help='Value to convert')
    parser.add_argument('from_unit', nargs='?', help='Source unit')
    parser.add_argument('to_unit', nargs='?', help='Target unit')
    parser.add_argument('--list', nargs='?', const='', metavar='CATEGORY', help='List supported units')
    parser.add_argument('--precision', type=int, default=6, help='Significant digits (default: 6)')
    
    args = parser.parse_args()
    
    if args.list is not None:
        list_units(args.list if args.list else None)
        return
    
    if args.value is None or args.from_unit is None or args.to_unit is None:
        parser.print_help()
        sys.exit(1)
    
    result = convert(args.value, args.from_unit, args.to_unit)
    formatted = format_result(result, args.precision)
    print(f"{args.value} {args.from_unit} = {formatted} {args.to_unit}")

if __name__ == '__main__':
    main()
