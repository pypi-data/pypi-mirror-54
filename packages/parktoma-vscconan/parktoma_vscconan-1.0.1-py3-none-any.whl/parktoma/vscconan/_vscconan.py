__all___ = ['update_cpp_tools', 'CppToolsUpdateFailure']

import inspect
import json
import os.path
import platform

_SUPPORTED_PLATFORM_PAIRS = { 'Windows': 'Win32', 'Darwin': 'Mac', 'Linux': 'Linux' }

class CppToolsUpdateFailure(Exception):
    '''Error which occurred trying to update c_cpp_properties.json'''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def update_cpp_tools(conanfile, conanfile_path=None, c_cpp_properties_path=None, config_name=None, throw_errors=False):
    '''Updates c_cpp_properties.json so Intellisense can find Conan dependencies
    
    :param conanfile: The ConanFile object for looking up dependencies
    :param conanfile_path: Optional path to the user's conanfile.py, or None. If provided, looks for './.vscode/c_cpp_properties.json'.
        Either conanfile_path or c_cpp_properties_path must be defined.
    :param c_cpp_properties_path: Optional path to c_cpp_properties.json, or None.
        Either conanfile_path or c_cpp_properties_path must be defined.
    :param config_name: The name of the configuration to update, or None. 
        If None or not provided, updates the default configuration for the OS.
    :throw_errors: If True, raises an exception if failure occurs. If false, logs a warning in the ConanFile object.
    :raises CppToolsUpdateFailure: If a failure occurs and throw_errors is True
    '''
    try:
        if c_cpp_properties_path is not None:
            resolved_c_cpp_properties_path = c_cpp_properties_path
        elif conanfile_path is not None:
            conanfile_dir_path = os.path.dirname(os.path.abspath(os.path.realpath(conanfile_path)))
            resolved_c_cpp_properties_path = os.path.join(conanfile_dir_path, '.vscode', 'c_cpp_properties.json')
        else:
            raise CppToolsUpdateFailure('Must provide path to conanfile.py or c_cpp_properties.json')

        if config_name is not None:
            resolved_config_name = config_name
        else:
            resolved_config_name = _SUPPORTED_PLATFORM_PAIRS.get(platform.system(), None)
            if resolved_config_name is None:
                raise CppToolsUpdateFailure('Unable to determine default configuration name from OS')

        try:
            include_paths = [os.path.abspath(os.path.realpath(include_path))
                for dep in conanfile.deps_cpp_info.deps 
                for include_path in conanfile.deps_cpp_info[dep].include_paths]
        except Exception as e:
            raise CppToolsUpdateFailure('Failed to get include path information found in conanfile object')

        if not (os.path.isfile(resolved_c_cpp_properties_path)):
            raise CppToolsUpdateFailure('c_cpp_properties.json not found')
        
        try:
            with open(resolved_c_cpp_properties_path, 'r') as f:
                c_cpp_props = json.load(f)
        except IOError as e:
            raise CppToolsUpdateFailure('Failed to read c_cpp_properties.json') from e
        except json.JSONDecodeError as e:
            raise CppToolsUpdateFailure('Failed to parse c_cpp_properties.json') from e
        
        try:
            config = next((config 
                for config in c_cpp_props['configurations'] 
                if config['name'] == resolved_config_name), None)
            if config is None:
                raise CppToolsUpdateFailure("Configuration with name '{}' not found".format(resolved_config_name))

            config_include_paths = config.setdefault('includePath', [])
            config_include_paths_lookup = set(config_include_paths)
            config_include_paths.extend(include_path 
                for include_path in include_paths 
                if include_path not in config_include_paths_lookup)
        except CppToolsUpdateFailure:
            raise
        except Exception as e:
            raise CppToolsUpdateFailure('Failed to update include paths of c_cpp_properties.json') from e

        try:
            with open(resolved_c_cpp_properties_path, 'w') as f:
                json.dump(c_cpp_props, f, indent=4)
        except IOError as e:
            raise CppToolsUpdateFailure('Failed to udpate c_cpp_properties.json') from e
    except CppToolsUpdateFailure as e:
        if throw_errors:
            raise
        conanfile.output.warn(str(e))