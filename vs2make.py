import xml.etree.ElementTree as ET
from collections import namedtuple

Project = namedtuple('Project', ['sources', 'headers'])


class Parser:
    project = Project([], [])

    def __parse_item_group(self, itemgroup):
        for f in itemgroup.findall('ClCompile'):
            self.project.sources.append(f.attrib['Include'])
        for f in itemgroup.findall('ClInclude'):
            self.project.headers.append(f.attrib['Include'])

    def __parse_project(self, root):
        for item in root:
            if item.tag == 'ItemGroup':
                self.__parse_item_group(item)

    def parse(self, tree):
        self.project = Project([], [])
        root = tree.getroot()

        self.__parse_project(root)
        return self.project


parser = Parser()
project = parser.parse(ET.parse('objects.vcxproj.xml'))

print project.sources
print project.headers