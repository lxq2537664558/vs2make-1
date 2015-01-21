import xml.etree.ElementTree as ET


class CppConfig:
    defines = []


class LinkerConfig:
    libs = []


class Project:
    sources = []
    headers = []
    customs = []
    compiler_config = CppConfig()
    linker_config = LinkerConfig()
    imports = []


class Parser:
    project = Project()
    check_condition = None

    def check_elem_condition(self, e):
        if 'Condition' in e.attrib:
            return self.check_condition(e.attrib['Condition'])
        else:
            return True

    def mk(self, root, parsers, skip_unknown=True):
        for child in root:
            if child.tag in parsers:
                if self.check_elem_condition(child):
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

    def parse_preprocessor_definitions(self, e):
        self.project.compiler_config.defines = (s.strip() for s in e.text.split(';'))

    def parse_compiler_config(self, e):
        parsers = {
            'PreprocessorDefinitions': self.parse_preprocessor_definitions,
        }
        self.mk(e, parsers)

    def parse_additional_dependencies(self, e):
        self.project.linker_config.libs = (s.strip() for s in e.text.split(';'))

    def parse_linker_config(self, e):
        parsers = {
            'AdditionalDependencies': self.parse_additional_dependencies,
        }
        self.mk(e, parsers)

    def parse_item_definition_group(self, e):
        parsers = {
            'ClCompile': self.parse_compiler_config,
            'Link': self.parse_linker_config,
        }
        self.mk(e, parsers)

    def parse_import(self, e):
        self.project.imports.append(e.attrib['Project'])

    def parse_import_group(self, e):
        parsers = {
            'Import': self.parse_import,
        }
        self.mk(e, parsers)

    def parse_project(self, e):
        parsers = {
            'ItemGroup': self.parse_item_group,
            'ItemDefinitionGroup': self.parse_item_definition_group,
            'Import': self.parse_import,
        }
        self.mk(e, parsers)

    def parse(self, tree, check_condition):
        root = tree.getroot()
        self.project = Project()
        self.check_condition = check_condition
        self.parse_project(root)
        return self.project


def parse_tree(tree, check_condition):
    parser = Parser()
    return parser.parse(tree, check_condition)


def check_condition(cond):
    print 'Checking:', cond
    return True


tree = ET.parse('objects.vcxproj.xml')
project = parse_tree(tree, check_condition)

print(list(project.imports))