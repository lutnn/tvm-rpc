# TVM RPC

Setting TVM RPC server on Android phones requires a series of commands.
The commands are the follows:
- Forward RPC server port and tracker port for ssh if the Android phones are connected to a remote server.
- Forward RPC server port and tracker port for ADB.
- Start RPC server on the Android phones.
- Start RPC tracker on the local machine.

This repository provides a one-click script for executing these commands.

## Installation

```bash
mkdir build
cd build
cmake \
	-DANDROID_ABI=arm64-v8a \
	-DCMAKE_TOOLCHAIN_FILE=${NDK_CMAKE_TOOLCHAIN_FILE} \
	-DCMAKE_BUILD_TYPE=Release \
	-DTVM_PATH=${TVM_PATH} \
	-DUSE_LIBBACKTRACE=OFF \
	..
make -j4
```

## Run

```
$ python launch.py --help
usage:  [-h] [--server SERVER] [--adb ADB] [--rpc-port RPC_PORT] [--tracker-port TRACKER_PORT] [--adb-port ADB_PORT] [--serial SERIAL] [--num-threads NUM_THREADS] [--taskset TASKSET] [--key KEY] [--start-rpc-tracker]

options:
  -h, --help            show this help message and exit
  --server SERVER
  --adb ADB             ADB binary path
  --rpc-port RPC_PORT   RPC server port
  --tracker-port TRACKER_PORT
                        RPC tracker port
  --adb-port ADB_PORT   ADB port
  --serial SERIAL       The serial number of the Android phone
  --num-threads NUM_THREADS
                        The number of threads RPC server uses
  --taskset TASKSET     The thread affinity for RPC server to restrict the RPC server to use the largest core
  --key KEY             The key string to display in the RPC tracker for this Android phone
  --start-rpc-tracker   Whether to start RPC tracker or not
```