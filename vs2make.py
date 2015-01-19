import xml.etree.ElementTree as ET
from collections import namedtuple

Project = namedtuple('Project', ['sources', 'headers'])

def parseTree(tree):
    root = tree.getroot()
    project = Project([], [])

    for itemgroup in root.findall('ItemGroup'):
        for f in itemgroup.findall('ClCompile'):
            project.sources.append(f.attrib['Include'])
        for f in itemgroup.findall('ClInclude'):
            project.headers.append(f.attrib['Include'])

    return project

project = parseTree(ET.parse('objects.vcxproj.xml'))

print project.sources
print project.headers