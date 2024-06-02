import minimalmodbus
from .abl import Abl
import argparse

def main():

    parser = argparse.ArgumentParser(
                    prog='abl',
                    description='Controll app for ABL eEMH1. It reads status of the wallbox, ability to set limiting current or pause charging',
                    epilog='')
    parser.add_argument('-p', '--port', default="COM4", help="Serial port COM1 or /dev/ttyUSB0, etc.")
    parser.add_argument('-a', '--addr', default=1, help="Address of the wallbox from 1 to 16")
    parser.add_argument('-l', '--limit', type=float, help="Limit the charging current (via duty)")
    parser.add_argument('--pause', action='store_true', help="Pauses charging (via 100%% duty)")
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
