#!/usr/bin/env bash

THIS_SCRIPT_FILE_MAYBE_RELATIVE="$0"
THIS_SCRIPT_DIR_MAYBE_RELATIVE="${THIS_SCRIPT_FILE_MAYBE_RELATIVE%/*}"
THIS_SCRIPT_DIR_ABSOLUTE=`readlink -f "${THIS_SCRIPT_DIR_MAYBE_RELATIVE}"`

sudo apt-get --yes install autoconf automake libtool curl make g++ unzip
sudo apt-get --yes install zlib1g-dev
sudo apt-get --yes install pkg-config

#echo "Podaj znak: "
#read znak


# Protobuf
git clone https://github.com/google/protobuf.git
cd protobuf
git checkout v3.2.0
export CFLAGS="-Os"
export CXXFLAGS="-Os"
export LDFLAGS="-Wl,-s"
./autogen.sh
./configure
 ##--prefix=/usr
sudo make clean
make
sudo make install
sudo ldconfig
unset CFLAGS CXXFLAGS LDFLAGS
# force install python module
cd python
sudo python setup.py install
cd ../..

git clone https://github.com/grpc/grpc.git

cd grpc
git checkout v1.3.2
ubuntu_release=`lsb_release -s -r`
if [[ "${ubuntu_release}" > "18" ]]
then
    PATCH_DIR="${THIS_SCRIPT_DIR_ABSOLUTE}/grpc-v1.3.2-patches-for-ubuntu18.04"

    for PATCH_FILE in no-werror.diff unvendor-zlib.diff fix-libgrpc++-soname.diff make-pkg-config-files-nonexecutable.diff add-wrap-memcpy-flags.diff
    do
        patch -p1 < "${PATCH_DIR}/${PATCH_FILE}"
    done
fi
git submodule update --init --recursive
export LDFLAGS="-Wl,-s"
sudo make clean
make
sudo make install
sudo ldconfig
unset LDFLAGS
cd ..

# Deps needed to build PI:
sudo apt-get --yes install libjudy-dev libreadline-dev valgrind libtool-bin libboost-dev libboost-system-dev libboost-thread-dev

# PI/P4Runtime
git clone https://github.com/p4lang/PI.git
cd PI
git submodule update --init --recursive
cp ../proto/p4runtime.proto proto/p4runtime/proto/p4/v1
./autogen.sh
./configure --with-proto
make
sudo make install
sudo ldconfig
cd ..
