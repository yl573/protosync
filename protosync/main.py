import argparse
import os
from protosync.dest import start_dest_sync
from protosync.source import start_source_sync
from protosync.common import set_debug

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mode', type=str, choices=['source', 'dest'],
                        help='dest is synced to source')
    parser.add_argument('pin',  type=str, default='', nargs='?', help='pin for identifying which diretory to protosync to')
    parser.add_argument('--dir', type=str, default='.', help='directory to protosync')
    parser.add_argument('--debug', action='store_true', help='run in debug mode, tries to connect to local server')

    args = parser.parse_args()

    if args.debug:
        print('running in debug mode')
        set_debug()

    args.dir = os.path.expanduser(args.dir)
    if not os.path.isdir(args.dir):
        print('Error: directory {} does not exist'.format(args.dir))

    if args.mode == 'source':
        start_source_sync(args.dir, args.pin, debug=args.debug)
    else:
        start_dest_sync(args.dir, debug=args.debug)


if __name__ == '__main__':
    main()
