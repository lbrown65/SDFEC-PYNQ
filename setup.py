#   Copyright (c) 2019, Xilinx, Inc.
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import subprocess
import shutil
from distutils.dir_util import copy_tree

from setuptools import find_packages, setup

# global variables
board = os.environ['BOARD']
repo_board_folder = f'boards/{board}/'
hw_data_files = []


def check_env():
    """Check if we're running on PYNQ and if the board is supported."""
    if not os.path.isdir(repo_board_folder):
        raise ValueError("Board {} is not supported.".format(board))


def copy_board_files(subdir):
    """Copy files from board directory to package""" 
    src_dir = os.path.join(repo_board_folder, subdir) 
    dst_dir = os.path.join('rfsoc_sdfec', subdir)
    copy_tree(src_dir, dst_dir)
    for new_file_dir, _, new_files in os.walk(dst_dir):
        hw_data_files.extend(
            [os.path.join("..", new_file_dir, f) for f in new_files]
        )


check_env()
make_command = ["make", "-C", repo_board_folder]
if subprocess.call(make_command) != 0:
    sys.exit(-1)
copy_board_files('notebooks')
copy_board_files('bitstreams')


setup(
    name="rfsoc_sdfec",
    version='2.0',
    install_requires=[
        'pynq>=2.4',
        'plotly>=3.8.1',
        'tqdm>=4.31.1'
    ],
    url='https://github.com/Xilinx/SDFEC-PYNQ',
    license='BSD 3-Clause License',
    author="Craig Ramsay",
    author_email="cramsay@xilinx.com",
    packages=find_packages(),
    package_data={'': hw_data_files},
    description="PYNQ example of using the RFSoC's Soft Decision Forward Error Correction (SD-FEC) IP")
