# Copyright (c) 2018 Sine Nomine Associates
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""git log with gerrit numbers"""

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import re
import sys
from git_gerrit._help import command_desc
from git_gerrit._unicode import cook, asciitize
from sh.contrib import git

def log(number=None, reverse=False, shorthash=True, revision=None, repodir=None, **kwargs):
    args = []
    if revision:
        args.append(revision)
    options = {
        'pretty':'hash:%{0}%nsubject:%s%n%n%b%%%%'.format('h' if shorthash else 'H'),
        'reverse':reverse,
        '_tty_out':False, # disable the pager
        '_iter':True,     # get lines
        '_cwd':repodir,
    }
    if number:
        options['max-count'] = number
    fields = {'hash':'', 'subject':'', 'number':'-' }
    for line in git.log(*args, **options):
        line = cook(line)
        line = line.strip()
        m = re.match(r'^hash:(.*)', line)
        if m:
            fields['hash'] = m.group(1)
            continue
        m = re.match(r'^subject:(.*)', line)
        if m:
            fields['subject'] = m.group(1)
            continue
        m = re.match(r'^Reviewed-on: .*/([0-9]+)$', line)
        if m:
            fields['number'] = int(m.group(1)) # get last one
            continue
        m = re.match(r'^%%$', line)
        if m:
            yield fields
            fields = {'hash':'', 'subject':'', 'number':'-'}

def main():
    DEFAULT_FORMAT = '{number} {hash} {subject}'
    parser = argparse.ArgumentParser(
                 description=command_desc('log'),
                 epilog='format fields: number, hash, subject')
    parser.add_argument('--repodir', help='path to the git project directory', default=None)
    parser.add_argument('--format',
                        help='output format (default: "{0}")'.format(DEFAULT_FORMAT),
                        default=DEFAULT_FORMAT)
    parser.add_argument('-n', '--number', type=int, help='number of commits')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse order')
    parser.add_argument('-l', '--long-hash', action='store_true', default=False, help='show full sha1 hash')
    parser.add_argument('revision', nargs='?', help='revision range')
    kwargs = vars(parser.parse_args())
    format = cook(kwargs.pop('format'))
    kwargs['shorthash'] = not kwargs['long_hash']

    for fields in log(**kwargs):
        try:
            print(format.format(**fields))
        except UnicodeEncodeError:
            # Fall back to ascii only.
            for k in fields:
                fields[k] = asciitize(fields[k])
            print(format.format(**fields))
    return 0

if __name__ == '__main__':
    sys.exit(main())
