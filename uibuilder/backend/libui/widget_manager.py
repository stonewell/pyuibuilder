import logging

from pylibui.core import App
from pylibui.controls import *

app = App()

widget_manager = None

def get_widget_manager():
    global widget_manager

    if not widget_manager:
        widget_manager = WidgetManager()

    return widget_manager

def create_widget(name):
    return get_widget_manager().create_widget(name)

def run_app():
    app.start()
    app.close()

class WidgetManager(object):
    def __init__(self, *args, **kwargs):
        pass

    def create_widget(self, name):
        m_name = 'create_widget_' + name
        if (hasattr(self, m_name)):
            return getattr(self, m_name)()

        logging.error('unable to create widget with name:{}'.format(name))
        return None

    def _update_helper_funcs(self, w):
        w.set_id = lambda x: setattr(w, '__ui_id', x)
        w.get_id = lambda: getattr(w, '__ui_id') if hasattr(w, '__ui_id') else None

        def _add_child(child):
            pass

        w.add_child = _add_child
        w.apply_attrib = lambda name, value: setattr(w, name, value)

    def create_widget_window(self):
        w = Window('title', 300, 400)
        w.show()

        self._update_helper_funcs(w)
        w.add_child = lambda x: w.setChild(x)

        return w

    def create_widget_tab(self):
        w = Tab()

        self._update_helper_funcs(w)

        w.add_child = lambda x:w.append(getattr(x, 'title') if hasattr(x, 'title') else x.get_id(), x)

        return w

    def create_widget_tabpage(self):
        w = HorizontalBox()

        self._update_helper_funcs(w)
        w.add_child = lambda x: w.append(x)

        return w

    def create_widget_label(self):
        w = Label('')

        self._update_helper_funcs(w)

        def _apply_attrib(name, value):
            if name == 'text':
                w.setText(value)
            else:
                setattr(w, name, value)

        w.apply_attrib = _apply_attrib
        return w
