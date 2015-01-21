import xml.etree.ElementTree as ET
from collections import namedtuple


class Project:
    sources = []
    headers = []
    customs = []



class Parser:
    project = Project()

    def check_condition(self, e):
        if 'Condition' in e.attrib:
            result = e.attrib['Condition'] == "'$(Configuration)|$(Platform)'=='Debug|Win32'"
            print 'Checking', e.attrib['Condition'], 'for', e.tag, ":", result
            return result
        else:
            return True

    def mk(self, root, parsers, skip_unknown=True):
        for child in root:
            if child.tag in parsers:
                if self.check_condition(child):
                    parsers[child.tag](child)
            else:
                if not skip_unknown:
                    message = 'Unknown tag: ' + child.tag
                    raise Exception(message)

    def parse_project_configuration(self, e):
        pass

    def parse_custom_build(self, e):
        self.project.customs.append(e.attrib['Include'])

    def parse_source(self, e):
        self.project.sources.append(e.attrib['Include'])

    def parse_header(self, e):
        self.project.headers.append(e.attrib['Include'])

    def parse_item_group(self, e):
        parsers = {
            'ClCompile': self.parse_source,
            'ClInclude': self.parse_header,
            'CustomBuild': self.parse_custom_build,
            'ProjectConfiguration': self.parse_project_configuration,
        }
        self.mk(e, parsers, skip_unknown=False)

    # ItemDefinitionGroup
    def parse_item_definition_group(self, e):
        pass


    def parse_project(self, e):
        parsers = {
            'ItemGroup': self.parse_item_group,
            'ItemDefinitionGroup': self.parse_item_definition_group,
        }
        self.mk(e, parsers)

    def parse(self, tree):
        root = tree.getroot()
        self.project = Project()
        self.parse_project(root)
        return self.project


def parse_tree(tree):
    parser = Parser()
    return parser.parse(tree)


tree = ET.parse('objects.vcxproj.xml')
project = parse_tree(tree)

print project.sources
print project.headers
print project.customs