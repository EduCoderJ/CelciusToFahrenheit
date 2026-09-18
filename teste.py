#!/usr/bin/env python3
"""Simple Celsius/Fahrenheit converter with Brazil/US number format support.

Usage examples:
  python teste.py "37,5 C"           # interprets comma as decimal (Brazil) and converts to Fahrenheit
  python teste.py "100 F" --to C --out-format brazil
  python teste.py                      # interactive prompt
"""

from __future__ import annotations

import argparse
import re
from typing import Tuple


def c_to_f(c: float) -> float:
	return c * 9.0 / 5.0 + 32.0


def f_to_c(f: float) -> float:
	return (f - 32.0) * 5.0 / 9.0


def parse_input(s: str) -> Tuple[float, str]:
	"""Parse a temperature string and return (value, unit).

	Accepts both comma and dot as decimal separators and optional unit C or F.
	If unit missing, assume Celsius.
	Examples: '37,5 C', '100F', '12.3', '0'
	"""
	s = s.strip()
	# Extract unit if present
	m = re.match(r"^([+-]?[0-9.,]+)\s*([cCfF])?$", s)
	if not m:
		raise ValueError(f"Can't parse temperature: {s!r}")
	num_str, unit = m.group(1), m.group(2)
	# Normalize comma to dot for parsing
	num_str = num_str.replace(',', '.')
	value = float(num_str)
	unit = (unit or 'C').upper()
	return value, unit


def format_number(value: float, out_format: str, precision: int = 1) -> str:
	fmt = f"{value:.{precision}f}"
	if out_format == 'brazil':
		# replace dot with comma
		fmt = fmt.replace('.', ',')
	return fmt


def main() -> None:
	p = argparse.ArgumentParser(description='Celsius/Fahrenheit converter with locale number formatting')
	p.add_argument('temp', nargs='?', help='Temperature to convert, e.g. "37,5 C" or "100F". Interactive if omitted')
	p.add_argument('--to', choices=['C', 'F'], default='F', help='Convert to C or F (default: F)')
	p.add_argument('--out-format', choices=['us', 'brazil'], default='us', help='Number format for output (us uses dot, brazil uses comma)')
	p.add_argument('--precision', type=int, default=1, help='Decimal places in output')
	args = p.parse_args()

	if not args.temp:
		try:
			args.temp = input('Enter temperature (e.g. 37,5 C or 100F): ').strip()
		except EOFError:
			p.print_help()
			return

	try:
		value, unit = parse_input(args.temp)
	except ValueError as e:
		print('Error:', e)
		return

	if unit == args.to:
		out_val = value
	elif unit == 'C' and args.to == 'F':
		out_val = c_to_f(value)
	elif unit == 'F' and args.to == 'C':
		out_val = f_to_c(value)
	else:
		print('Unsupported conversion')
		return

	in_fmt = format_number(value, 'brazil' if ',' in args.temp else 'us', precision=args.precision)
	out_fmt = format_number(out_val, 'brazil' if args.out_format == 'brazil' else 'us', precision=args.precision)

	unit_sym = lambda u: '°C' if u == 'C' else '°F'
	print(f"{in_fmt}{unit_sym(unit)} = {out_fmt}{unit_sym(args.to)}")


if __name__ == '__main__':
	main()
