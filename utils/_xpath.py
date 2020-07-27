# coding: utf-8

from lxml import etree

from setting import CLICKABLE_XPATH_EXPR


class XPathUtils:

    @staticmethod
    def get_node_list_by_xpath(page_source: str, xpath_expr: str):
        node_list = etree.fromstring(bytes(page_source, encoding='utf-8')).xpath(xpath_expr)
        return node_list

    @staticmethod
    def get_android_app_name_from_dom(page_source):
        pass

    @staticmethod
    def __element_to_path_list(page_source: str, xpath_expr: str):
        all_element_path = []
        root = etree.fromstring(bytes(page_source, encoding='utf-8'))
        node_list = root.xpath(xpath_expr)
        for node in node_list:
            element_xpath = root.getroottree().getpath(node)
            if element_xpath not in all_element_path:
                all_element_path.append(element_xpath)
            for child_node in node.iterchildren():
                element_xpath = root.getroottree().getpath(child_node)
                if element_xpath not in all_element_path:
                    all_element_path.append(element_xpath)
        return all_element_path

    @staticmethod
    def page_clickable_item_update(xml_str, clicked_list=None):
        clickable_xpath_expr = CLICKABLE_XPATH_EXPR
        root = etree.fromstring(bytes(xml_str, encoding='utf-8'))
        node_list = root.xpath(clickable_xpath_expr)

        click_dict = {}
        known_value_list = []

        if clicked_list is None:
            for node in node_list:
                xpath = root.getroottree().getpath(node)
                bounds = XPathUtils.element_center_position(node.attrib["bounds"])
                if bounds not in known_value_list:
                    click_dict[xpath] = {
                        "bounds": bounds,
                        "covered": False
                    }
                    known_value_list.append(bounds)
                    for child_node in node.iterchildren():
                        xpath = root.getroottree().getpath(child_node)
                        bounds = XPathUtils.element_center_position(node.attrib["bounds"])
                        if xpath not in click_dict.keys() and bounds not in known_value_list:
                            click_dict[xpath] = {
                                "bounds": bounds,
                                "covered": False
                            }
                            known_value_list.append(bounds)

        else:
            for node in node_list:
                xpath = root.getroottree().getpath(node)
                bounds = XPathUtils.element_center_position(node.attrib["bounds"])
                if xpath not in clicked_list and bounds not in known_value_list:
                    click_dict[xpath] = {
                        "bounds": bounds,
                        "covered": False
                    }
                    known_value_list.append(bounds)
                for child_node in node.iterchildren():
                    xpath = root.getroottree().getpath(child_node)
                    bounds = XPathUtils.element_center_position(node.attrib["bounds"])
                    if xpath not in click_dict.keys() and xpath not in clicked_list and bounds not in known_value_list:
                        click_dict[xpath] = {
                            # "bounds": XPathUtils.element_center_position(node.attrib["bounds"]),
                            "bounds": bounds,
                            "covered": False
                        }
                        known_value_list.append(bounds)
        return click_dict

    @staticmethod
    def page_text_list(dom: str):
        root = etree.fromstring(bytes(dom, encoding='utf-8'))
        text_list = []
        for elem in root.iter():
            for attr_key, attr_value in elem.attrib.items():
                if attr_key == 'text' and attr_value != "" and attr_value not in text_list:
                    text_list.append(attr_value)
        return text_list

    @staticmethod
    def element_center_position(bounds_str):
        # covert dom element bounds attribute to element center coordinate
        # bounds_str = "[1030,1266][1047,1307]"
        x1, tmp, y2 = bounds_str.lstrip("[").rstrip("]").split(",")
        y1, x2 = tmp.split("][")
        x = (int(x1) + int(x2)) / 2
        y = (int(y1) + int(y2)) / 2
        return (int(x), int(y))