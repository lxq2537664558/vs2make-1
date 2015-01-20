import xml.etree.ElementTree as ET
from collections import namedtuple

Project = namedtuple('Project', ['sources', 'headers'])


class Parser:
    project = Project([], [])

    def check_condition(self, e):
        if 'Condition' in e.attrib:
            print 'Checking', e.attrib['Condition'], 'for', e.tag
        return True

    def mk(self, root, parsers):
        for child in root:
            if child.tag in parsers:
                if self.check_condition(root):
                    parsers[child.tag](child)

    def parse_cpp(self, e):
        self.project.sources.append(e.attrib['Include'])

    def parse_h(self, e):
        self.project.headers.append(e.attrib['Include'])

    def parse_item_group(self, e):
        parsers = {
            'ClCompile': self.parse_cpp,
            'ClInclude': self.parse_h,
        }
        self.mk(e, parsers)

    def parse_project(self, e):
        parsers = {
            'ItemGroup': self.parse_item_group
        }
        self.mk(e, parsers)

    def parse(self, tree):
        root = tree.getroot()
        self.project = Project([], [])
        self.parse_project(root)
        return self.project


def parse_tree(tree):
    parser = Parser()
    return parser.parse(tree)


tree = ET.parse('test_proj.vcxproj.xml')
project = parse_tree(tree)

print project.sources
print project.headers