# Copyright (c) 2013, Mike Gibson
# Copyright (c) 2012, Claudio "nex" Guarnieri
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import hashlib
import binascii

try:
    import magic
except ImportError:
    pass

try:
    import pydeep
    HAVE_SSDEEP = True
except ImportError:
    HAVE_SSDEEP = False

class File:
    def __init__(self, file_path=None, file_data=None):
        self.file_path = file_path

        if file_path:
            self.file_data = open(self.file_path, "rb").read()
        else:
            self.file_data = file_data

    def get_name(self):
        file_name = os.path.basename(self.file_path)
        return file_name

    def get_data(self):
        return self.file_data

    def get_size(self):
        return os.path.getsize(self.file_path)

    def get_crc32(self):
        res = ''
        crc = binascii.crc32(self.file_data)
        for i in range(4):
            t = crc & 0xFF
            crc >>= 8
            res = '%02X%s' % (t, res)
        return res

    def get_md5(self):
        return hashlib.md5(self.file_data).hexdigest()

    def get_sha1(self):
        return hashlib.sha1(self.file_data).hexdigest()

    def get_sha256(self):
        return hashlib.sha256(self.file_data).hexdigest()

    def get_sha512(self):
        return hashlib.sha512(self.file_data).hexdigest()

    def get_ssdeep(self):
        if not HAVE_SSDEEP:
            return None

        try:
            return pydeep.hash_file(self.file_path)
        except Exception:
            return None

    def get_type(self):
        try:
            ms = magic.open(magic.MAGIC_NONE)
            ms.load()
            file_type = ms.buffer(self.file_data)
        except:
            try:
                file_type = magic.from_buffer(self.file_data)
            except:
                try:
                    import subprocess
                    file_process = subprocess.Popen(['file', '-b', self.file_path], stdout = subprocess.PIPE)
                    file_type = file_process.stdout.read().strip()
                except:
                    return None

        return file_type
