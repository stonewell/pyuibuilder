import logging

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

class Builder(object):
    def __init__(self):
        super(Builder, self).__init__()
        self.__nodes = {}
        self.__styles = None
        self.__id_count = 0

    def load(self, path):
        root = ET.parse(path).getroot()
        self._process_root_node(root)

    def _process_root_node(self, root):
        for child in root:
            print(child, child.attrib, child.tag)

            if hasattr(self, '_process_' + child.tag):
                getattr(self, '_process_' + child.tag)(child)
            else:
                self._process_general_node(child)

    def loadstring(self, xmlcontent):
        root = ET.fromstring(xmlcontent)
        self._process_root_node(root)

    def _process_general_node(self, node):
        id = node.attrib['id'] if 'id' in node.attrib else self._gen_id(node)

        logging.info('get node:{}, attrib:{} with id:{}'.format(node.tag, node.attrib, id))
        self.__nodes[id] = node

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
        ui_model = _UIModel()

        for id in self.__nodes:
            node = self.__nodes[id]

            widget = self._create_widget(node)
            layout = self._create_layout(node, self.__styles)

            layout.apply(widget)
            
            ui_model[id] = widget

        return ui_model

    def _create_widget(self, node):
        pass

    def _create_layout(self, node, styles):
        pass
