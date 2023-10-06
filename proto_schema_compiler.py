import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-r', '--root', help='root of protobuf schema.')

args = parser.parse_args()
proto_root = args.root

for r, d, fs in os.walk(proto_root):
    for f in fs:
        if os.path.splitext(f)[-1] == '.proto':
            protoc_cmd = 'protoc -I={} --python_out={} {}'.format(proto_root, proto_root, os.path.join(r, f))
            print(protoc_cmd)
            os.system(protoc_cmd)
