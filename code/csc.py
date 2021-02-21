import argparse
import utils
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument(
        '-f',
        '--function',
        type=str,
        choices=['classify', 'time'],
        help='choose function'
        )
    parser.add_argument(
        '-s',
        '--stage',
        type=str,
        choices=['train', 'test'],
        help='choose stage'
        )
    parser.add_argument(
        '--train',
        type=str,
        default=""
        help='choose stage'
        )

    args = parser.parse_args()

    # print(args.stage)
    # print(args.function)
    if args.function == "classify":
        utils.MakeClassifyDir()

    elif args.function == "time":
        utils.MakeTimeDir()
