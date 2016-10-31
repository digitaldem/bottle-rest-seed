# Standard Library imports
from __future__ import absolute_import, print_function
from StringIO import StringIO
from xml.etree.cElementTree import ElementTree, Element, SubElement

# Package imports

# Local imports


def serialize(datadict, roottag='root', defaulttag='item', encoding='utf-8', xml_declaration=True, pretty=False, sort=False):
    if len(datadict.keys()) == 1:
        roottag, datadict = datadict.items()[0]

    root = Element(roottag)
    _convert_dict_to_xml_recurse(root, datadict, {}, defaulttag, sort)

    if pretty:
        _indent(root)

    tree = ElementTree(root)
    fileobj = StringIO()
    tree.write(fileobj, encoding=encoding, xml_declaration=xml_declaration)
    return fileobj.getvalue()


def _convert_dict_to_xml_recurse(parent, dictitem, listnames, defaulttag, sort):
    if isinstance(dictitem, list):
        raise TypeError('Unable to convert bare lists')

    if isinstance(dictitem, dict):
        items = dictitem.iteritems()
        if sort:
            items = sorted(items)
        for (tag, child) in items:
            if isinstance(child, list):
                itemname = listnames.get(tag, defaulttag)
                if itemname is not None:
                    listelem = SubElement(parent, tag)
                else:
                    listelem = parent

                for listchild in child:
                    if itemname is not None:
                        elem = SubElement(listelem, itemname)
                    else:
                        elem = SubElement(listelem, tag)

                    _convert_dict_to_xml_recurse(elem, listchild, listnames, defaulttag, sort)
            else:
                if tag.startswith('@'):
                    parent.attrib[tag[1:]] = child
                else:
                    elem = Element(tag)
                    parent.append(elem)
                    _convert_dict_to_xml_recurse(elem, child, listnames, defaulttag, sort)
    elif dictitem is not None:
        parent.text = unicode(dictitem)


def _indent(elem, level=0):
    i = "\n" + level * " "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

        child = None
        for child in elem:
            _indent(child, level + 1)

        if child:
            if not child.tail or not child.tail.strip():
                child.tail = i
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
