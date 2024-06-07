# LICENSE HEADER MANAGED BY add-license-header
#
# MIT License
#
# Copyright (c) 2024 Libor Ukropec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import minimalmodbus
from .abl import Abl
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="abl",
        description="Controll app for ABL eEMH1. It reads status of the wallbox, ability to set limiting current or pause charging",
        epilog="",
    )
    parser.add_argument(
        "-p",
        "--port",
        default="/dev/ttyUSB0",
        help="Serial port COM1 or /dev/ttyUSB0, etc.",
    )
    parser.add_argument(
        "-a", "--addr", default=1, help="Address of the wallbox from 1 to 16"
    )
    parser.add_argument(
        "-l", "--limit", type=float, help="Limit the charging current (via duty)"
    )
    parser.add_argument(
        "--pause", action="store_true", help="Pauses charging (via 100%% duty)"
    )
    args = parser.parse_args()

    ABL = minimalmodbus.Instrument(args.port, args.addr, minimalmodbus.MODE_ASCII)
    a = Abl(ABL)
    a.Wake_Up()
    status = a.Read_Status()
    print(status)
    if args.pause:
        a.Set_Duty(100)
    elif args.limit is not None:
        a.Set_Current(args.limit)


if __name__ == "__main__":
    main()
