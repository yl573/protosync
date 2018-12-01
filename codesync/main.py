import argparse
from codesync.dest import start_dest_sync
from codesync.source import start_source_sync

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mode', type=str, choices=['source', 'dest'],
                        help='dest is synced to source')
    parser.add_argument('pin',  type=str, default='', nargs='?', help='pin for identifying which diretory to sync to')
    parser.add_argument('--dir', type=str, default='.', help='directory to sync')

    args = parser.parse_args()

    if args.mode == 'source':
        start_source_sync(args.dir, args.pin)
    else:
        start_dest_sync(args.dir, args.pin)

