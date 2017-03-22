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

def stop_app():
    app.stop()

class WidgetManager(object):
    def __init__(self, *args, **kwargs):
        pass

    def create_widget(self, name):
        m_name = 'create_widget_' + name
        if hasattr(self, m_name):
            return getattr(self, m_name)()

        logging.error('unable to create widget with name:{}'.format(name))
        return None

    @staticmethod
    def _set_attrib(widget, name, value):
        '''
        set widget attribute,
        if there is a set function, call it
        otherwise set the attrib
        '''
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
            
        if hasattr(widget, 'set' + name.title()):
            getattr(widget, 'set' + name.title())(value)

        setattr(widget, name, value)

    @staticmethod
    def _get_attrib(widget, name, old_get_attrib):
        if hasattr(widget, 'get' + name.title()):
            return getattr(widget, 'get' + name.title())()

        return old_get_attrib(name)

    def _update_helper_funcs(self, w):
        w.set_id = lambda x: setattr(w, '__ui_id', x)
        w.get_id = lambda: getattr(w, '__ui_id') if hasattr(w, '__ui_id') else None

        def _add_child(child):
            pass

        w.add_child = _add_child
        w.apply_attrib = lambda n, v: self._set_attrib(w, n, v)

        old_get_attrib = w.__getattribute__
        w.__getattribute__ = lambda name: self._get_attrib(w, name, old_get_attrib)

    @staticmethod
    def _on_window_close(w, old_onClose, data):
        old_onClose(data)

        if hasattr(w, 'on_close'):
            getattr(w, 'on_close')(data)

    def create_widget_window(self):
        w = Window('title', 300, 400)

        self._update_helper_funcs(w)
        w.add_child = lambda x: w.setChild(x)

        old_onClose = w.onClose
        w.onClose = lambda data:self._on_window_close(w, old_onClose, data)

        def _window_apply_attrib(n, v):
            width, h = w.getContentSize()
            
            if n == 'width':
                width = int(v)
            elif n == 'height':
                h = int(v)
            elif n == 'content_size':
                parts = v.split(',')
                width = int(parts[0])
                h = int(parts[1])
            else:
                self._set_attrib(w, n, v)
                return

            w.setContentSize(width, h)

        w.apply_attrib = _window_apply_attrib
        w.show()

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

        return w
