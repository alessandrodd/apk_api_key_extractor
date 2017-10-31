"""
Utility tool used for supervised learnset creation, blacklist population and database cleaning
"""
import os
import sys

from words_finder_singleton import finder

from db_interface import get_apikey_unverified, remove_apikey, set_apikey_verified
from my_tools.getch import getch


def main(argv):
    if len(argv) != 4:
        print("Usage: python {0} text_learnset_output_path api_learnset_output_path blacklist_output_path".format(
            argv[0]))
        return
    if os.path.exists(argv[1]):
        newline_text = '\n'
    else:
        newline_text = ''
    if os.path.exists(argv[2]):
        newline_api = '\n'
    else:
        newline_api = ''
    if os.path.exists(argv[3]):
        newline_blk = '\n'
    else:
        newline_blk = ''

    text_dest = open(argv[1], "a", 1)
    api_dest = open(argv[2], "a", 1)
    blk_dest = open(argv[3], "a", 1)
    print("Press 0 if the string is NOT an API Key, 1 otherwhise\n"
          "Press b to blacklist the entry\n"
          "Press r to remove the record from database\n"
          "Press q to quit")
    try:
        while True:
            api_doc = get_apikey_unverified()
            if not api_doc:
                print("No more keys!")
                break
            print("{0}   {1}   {2}   {3}".format(api_doc.get("package"), api_doc.get("source"), api_doc.get("name"),
                                                 api_doc.get("value")))
            x = '-1'
            if finder.get_words_percentage(api_doc.get("value")) >= 0.4:
                remove_apikey(api_doc.get("_id"))
            else:
                while x != '0' and x != '1' and x != 'r' and x != 'b' and x != 'q':
                    x = getch()
                    if x == '0':
                        remove_apikey(api_doc.get("_id"))
                        text_dest.write(newline_text + api_doc.get("value"))
                        newline_text = '\n'
                    elif x == '1':
                        set_apikey_verified(api_doc.get("_id"))
                        api_dest.write(newline_api + api_doc.get("value"))
                        newline_api = '\n'
                    elif x == 'r':
                        remove_apikey(api_doc.get("_id"))
                    elif x == 'b':
                        remove_apikey(api_doc.get("_id"))
                        blk_dest.write(newline_blk + api_doc.get("value"))
                        newline_blk = '\n'
                    elif x == 'q':
                        text_dest.close()
                        api_dest.close()
                        exit()

    except KeyboardInterrupt:
        print('\nInterrupted!')


if __name__ == '__main__':
    main(sys.argv)
