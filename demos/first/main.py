import os
import logging

from uibuilder.builder import Builder

logging.getLogger('').setLevel(logging.DEBUG)

def main():
    builder = Builder()
    builder.load(os.path.join(os.path.dirname(__file__), 'main.xml'))

    ui = builder.build()

    print(ui.mainWnd, ui['mainWnd'])

if __name__ == '__main__':
    main()
