"""
A simple python3 implementation of Unix's strings utility, with some reverse-engineering utility

"""
import re
import sys
from mmap import ALLOCATIONGRANULARITY
from mmap import mmap, ACCESS_READ

from elftools.elf.elffile import ELFFile


def strings(file_name, sections=None, min_length=4):
    """
    Finds all strings in a file; if it's an ELF file, you can specify where (in which section) to
    look for the strings.

    :param file_name: name of the file to be examined
    :param sections: a list of strings which identify the ELF sections; should be used only with ELF files
    :param min_length:
    :return:
    """
    pattern = '([\x20-\x7E]{' + str(min_length) + '}[\x20-\x7E]*)'  # ASCII table from character space to tilde
    pattern = pattern.encode()
    regexp = re.compile(pattern)
    if not sections:
        with open(file_name, 'rb') as f, mmap(f.fileno(), 0, access=ACCESS_READ) as m:
            for match in regexp.finditer(m):
                yield str(match.group(0), 'utf-8')
    else:
        with open(file_name, 'rb') as f:
            elffile = ELFFile(f)
            for section in sections:
                try:
                    sec = elffile.get_section_by_name(section)
                except AttributeError:
                    # section not found
                    continue
                # skip section if missing in elf file
                if not sec:
                    continue
                offset = sec['sh_offset']
                size = sec['sh_size']
                if offset is None or size is None:
                    continue
                # round to allocation granularity for mmap
                offset = max(offset - offset % ALLOCATIONGRANULARITY, 0)
                with mmap(f.fileno(), size, access=ACCESS_READ, offset=offset) as m:
                    for match in regexp.finditer(m):
                        yield str(match.group(0), 'utf-8')


def main(argv):
    if len(argv) == 2:
        for word in strings(sys.argv[1]):
            print(word)
    elif len(argv) == 3:
        for word in strings(sys.argv[1], None, sys.argv[2]):
            print(word)
    else:
        print("Usage: python {0} path/to/file [min_string_length]".format(argv[0]))


if __name__ == '__main__':
    main(sys.argv)
