'''
builder.py for ui builder
'''
import logging
from .backend import create_widget, run_app

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class _UIModel(dict):
    def __getattribute__(self, name):
        if hasattr(super(_UIModel, self), name):
            return super(_UIModel, self).__getattribute__(name)

        if name in self:
            return self[name]

        return super(_UIModel, self).__getattribute__(name)

    def __setattr__(self, name, v):
        if hasattr(super(_UIModel, self), name):
            super(_UIModel, self).__setattr__(name, v)

        self[name] = v

    def run(self):
        run_app()

class Builder(object):
    '''
    ui builder to create ui from xml description
    '''
    def __init__(self):
        super(Builder, self).__init__()
        self.__nodes = {}
        self.__styles = None
        self.__id_count = 0

    def load(self, path):
        '''
        load xml ui description from file specified by path
        '''
        root = ET.parse(path).getroot()
        self._process_root_node(root)

    def _process_root_node(self, root):
        for child in root:
            logging.info('child:{}, attrib:{}, tag:{}'.format(child, child.attrib, child.tag))

            if hasattr(self, '_process_' + child.tag):
                getattr(self, '_process_' + child.tag)(child)
            else:
                self._process_general_node(child)

    def loadstring(self, xmlcontent):
        '''
        load xml ui description from xml string
        '''
        root = ET.fromstring(xmlcontent)
        self._process_root_node(root)

    def _process_general_node(self, node):
        _id = node.attrib['id'] if 'id' in node.attrib else self._gen_id(node)

        logging.info('get node:{}, attrib:{} with id:{}'.format(node.tag, node.attrib, _id))
        self.__nodes[_id] = node

    def _process_styles(self, node):
        logging.info('get styles node:{}'.format(node.attrib))
        styles = self._load_styles(node)

        self.__styles = self._merge_styles(self.__styles, styles)

    def _merge_styles(self, dst, src):
        if not dst:
            return src

        if src:
            dst.update(src)

        return dst

    def _load_styles(self, node):
        return None

    def _gen_id(self, node):
        self.__id_count += 1
        return 'id_{}_{}'.format(node.tag, self.__id_count)

    def build(self):
        '''
        create ui widget using loaded xml description
        '''
        _ui_model = _UIModel()

        for _id in self.__nodes:
            _node = self.__nodes[_id]

            _widget = self._create_widget_from_node(_ui_model, _node)
            _widget.set_id(_id)

            _ui_model[_id] = _widget

        return _ui_model

    def _create_widget(self, node):
        return create_widget(node)

    def _apply_attribs(self, w, node):
        for attr in node.attrib:
            w.apply_attrib(attr, node.attrib[attr])

    def _create_widget_from_node(self, ui_model, node):
        _widget = self._create_widget(node)
        _layout = self._create_layout(node, self.__styles)
        self._apply_attribs(_widget, node)

        if _layout:
            _layout.apply(_widget)

        for child in node:
            _child_id = child.attrib['id'] if 'id' in child.attrib else self._gen_id(child)
            _child_widget = self._create_widget_from_node(ui_model, child)
            _child_widget.set_id(_child_id)
            ui_model[_child_id] = _child_widget

            _widget.add_child(_child_widget)

        return _widget

    def _create_layout(self, node, styles):
        pass
