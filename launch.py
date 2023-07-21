import sys
import argparse
import subprocess
import socket
from contextlib import closing


import main


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser("")
    parser.add_argument("--server", default="hexserver", help="")
    parser.add_argument("--adb", default="adb", help="ADB binary path")
    parser.add_argument("--rpc-port", default=9000,
                        type=int, help="RPC server port")
    parser.add_argument("--tracker-port", default=9190,
                        type=int, help="RPC tracker port")
    parser.add_argument("--adb-port", default=5037, type=int, help="ADB port")
    parser.add_argument("--serial", default="98281FFAZ009SV",
                        help="The serial number of the Android phone")
    parser.add_argument("--num-threads", default=1, type=int,
                        help="The number of threads RPC server uses")
    parser.add_argument("--taskset", default="80",
                        help="The thread affinity for RPC server to restrict the RPC server to use the largest core")
    parser.add_argument("--key", default="pixel4",
                        help="The key string to display in the RPC tracker for this Android phone")
    parser.add_argument("--start-rpc-tracker", action="store_true",
                        help="Whether to start RPC tracker or not")
    args = parser.parse_args()

    ps = []

    if args.server != "localhost":
        if not check_socket("localhost", args.adb_port):
            p = subprocess.Popen([
                "ssh", "-fN", "-L", f"{args.adb_port}:localhost:{args.adb_port}", args.server
            ])
            p.wait()

        ps.append(subprocess.Popen([
            "ssh", "-N", "-L", f"{args.rpc_port}:localhost:{args.rpc_port}", args.server
        ]))
        ps.append(subprocess.Popen([
            "ssh", "-N", "-R", f"{args.tracker_port}:localhost:{args.tracker_port}", args.server
        ]))

    if args.start_rpc_tracker:
        ps.append(subprocess.Popen([
            sys.executable, "-m", "tvm.exec.rpc_tracker", "--host=0.0.0.0", f"--port={args.tracker_port}"
        ]))

    ps.append(subprocess.Popen([
        args.adb, "-s", args.serial, "forward", f"tcp:{args.rpc_port}", f"tcp:{args.rpc_port}"
    ]))

    ps.append(subprocess.Popen([
        args.adb, "-s", args.serial, "reverse", f"tcp:{args.tracker_port}", f"tcp:{args.tracker_port}"
    ]))

    ps.append(subprocess.Popen([
        sys.executable, main.__file__, f"--serial={args.serial}", f"--taskset={args.taskset}", f"--num-threads={args.num_threads}",
        "--cmd-args", "server", "--host=0.0.0.0",
        f"--port={args.rpc_port}", f"--port-end={args.rpc_port + 1}",
        f"--tracker=127.0.0.1:{args.tracker_port}", f"--key={args.key}"
    ]))

    for p in ps:
        p.wait()
