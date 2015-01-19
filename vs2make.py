import xml.etree.ElementTree as ET
from collections import namedtuple

Project = namedtuple('Project', ['sources', 'headers'])


def check_condition(root, project):
    if 'Condition' in root.attrib:
        print 'checking condition:', root.attrib['Condition'], 'in', root.tag
    return True


def mk(parsers):
    def f(root, p):
        for child in root:
            if child.tag in parsers:
                if check_condition(child, p):
                    parsers[child.tag](child, p)
    return f


item_group_parser = mk({
    'ClCompile': (lambda e, proj: proj.sources.append(e.attrib['Include'])),
    'ClInclude': (lambda e, proj: proj.headers.append(e.attrib['Include'])),
})


def prop_group(root, project):
    pass

project_parser = mk({
    'ItemGroup': item_group_parser,
    'PropertyGroup': prop_group,
})


tree = ET.parse('test_proj.vcxproj.xml')
root = tree.getroot()

project = Project([], [])

project_parser(root, project)

print project.sources
print project.headers