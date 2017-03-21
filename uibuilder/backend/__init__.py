#__init__.py backend
import os
import sys
import logging

L = logging.getLogger('backend')

def create_widget(node):
    '''
    create widget based on xml node
    '''
    if 'impl' in node.attrib:
        try:
            return create_widget_from_impl(node.attrib['impl'])
        except:
            L.exception('unable to create using impl class:{}'.format(node.attrib['impl']))

    return create_widget_from_tag(node.tag)

def create_widget_from_impl(impl_cls):
    '''
    create widget from the impl class
    '''
    _module = __load_module_by_name(impl_cls)
    return _module.create_widget()

def create_widget_from_tag(tag):
    '''
    create widget from tag using backend
    '''
    _wm = __load_backend_widget_manager()
    return _wm.create_widget(tag)

def __load_module_by_name(m_name):
    '''
    load module using given moudle name m_name
    '''
    if not m_name in sys.modules:
        __import__(m_name)

    return sys.modules[m_name]

def __load_backend_widget_manager():
    '''
    load widget manager from predefined backend
    '''
    return __load_module_by_name('libui.widget_manager')
