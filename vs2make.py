import xml.etree.ElementTree as ET
from collections import namedtuple

Project = namedtuple('Project', ['sources', 'headers'])


class Parser:
    project = Project([], [])
    include_f = None

    def check_condition(self, e):
        if 'Condition' in e.attrib:
            result = e.attrib['Condition'] == "'$(Configuration)|$(Platform)'=='Debug|Win32'"
            print 'Checking', e.attrib['Condition'], 'for', e.tag, ":", result
            return result
        else:
            return True

    def mk(self, root, parsers):
        for child in root:
            if child.tag in parsers:
                if self.check_condition(child):
                    parsers[child.tag](child)

    def parse_file(self, e, include_f):
        # Ugly ugly ugly hack: don't know how to assign from inside of lambda
        exclude = []
        parsers = {
            'ExcludedFromBuild': lambda child: exclude.append('Fuck')
        }
        self.mk(e, parsers)
        if not exclude:
            include_f(e.attrib['Include'])

    def parse_item_group(self, e):
        parsers = {
            'ClCompile': lambda child: self.parse_file(child, lambda name: self.project.sources.append(name)),
            'ClInclude': lambda child: self.parse_file(child, lambda name: self.project.headers.append(name)),
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