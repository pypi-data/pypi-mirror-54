#!/usr/bin/python3
from sop import __version__, StatelessOpenPGP
# NOTE: this should give errors for everything :)

def main() -> None:
    sop = StatelessOpenPGP(version=__version__)
    sop.dispatch()

if __name__ == '__main__':
    main()
