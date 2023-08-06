from deprecated import deprecated

import pandas as pd

from .. import _common


class _AssetBase:

    def __init__(self, definition=None, parent=None):
        """
        Instantiates an Asset or Mixin.

        :param definition: A dictionary of property-value pairs that make up the definition of the Asset. Typically
        you will want to supply 'Name' at minimum.
        :type definition: dict
        :param parent: An instance of either an Asset or Mixin that represents the parent of this instance. Typically
        this is supplied when @Asset.Component is used to define child assets.
        :type parent: Asset, Mixin
        """
        self.definition = dict()

        if isinstance(definition, _AssetBase):
            self.definition = definition.definition
        elif isinstance(definition, pd.DataFrame):
            if len(definition) != 1:
                raise RuntimeError('DataFrame must be exactly one row')
            self.definition = definition.iloc[0].to_dict()
        elif isinstance(definition, pd.Series):
            self.definition = definition.to_dict()
        elif definition is not None:
            self.definition = definition

        self.definition['Type'] = 'Asset'
        if 'Name' in self.definition:
            self.definition['Asset'] = self.definition['Name']

        self.parent = parent  # type: _AssetBase

        if self.parent is not None:
            self.definition['Path'] = self.parent.definition['Path'] + ' >> ' + self.parent.definition['Name']

    @property
    @deprecated(reason="Use self.definition instead")
    def asset_definition(self):
        return self.definition

    @property
    @deprecated(reason="Use self.parent.definition instead")
    def parent_definition(self):
        return self.parent.definition if self.parent is not None else None

    def build(self, metadata):
        definitions = list()
        object_methods = [getattr(self, method_name) for method_name in dir(self)
                          if callable(getattr(self, method_name))]

        for func in object_methods:
            if not hasattr(func, 'spy_model'):
                continue

            attribute = func(metadata)

            if attribute is None:
                continue

            if isinstance(attribute, list):
                definitions.extend(attribute)
            else:
                definitions.append(attribute)

        return definitions


class Mixin(_AssetBase):

    def __init__(self, definition):
        super().__init__(definition)

    def build(self, metadata):
        definitions = super().build(metadata)
        return definitions


class Asset(_AssetBase):

    def __init__(self, definition=None, parent=None):
        super().__init__(definition, parent)
        self.definition['Template'] = self.__class__.__name__.replace('_', ' ')

    def build(self, metadata):
        definitions = super().build(metadata)
        definitions.append(self.definition)
        self.definition['Build Result'] = 'Success'
        return definitions

    @staticmethod
    def _add_asset_metadata(self, attribute_definition, error):
        if _common.present(self.asset_definition, 'Path') and not _common.present(attribute_definition, 'Path'):
            attribute_definition['Path'] = self.asset_definition['Path']

        if _common.present(self.asset_definition, 'Asset') and not _common.present(attribute_definition, 'Asset'):
            attribute_definition['Asset'] = self.asset_definition['Asset']

        if _common.present(self.asset_definition, 'Template') and not _common.present(attribute_definition, 'Template'):
            attribute_definition['Template'] = self.__class__.__name__.replace('_', ' ')

        attribute_definition['Build Result'] = 'Success' if error is None else error

    @classmethod
    def Attribute(cls):
        def attribute_decorator(func):
            def attribute_wrapper(self, metadata):
                func_results = func(self, metadata)

                attribute_definition = dict()

                error = None

                if func_results is None:
                    error = 'None returned by Attribute function'

                def _preserve_originals():
                    for key in ['Name', 'Path']:
                        if _common.present(attribute_definition, key):
                            attribute_definition['Referenced ' + key] = attribute_definition[key]
                            del attribute_definition[key]

                if isinstance(func_results, pd.DataFrame):
                    if len(func_results) == 1:
                        attribute_definition.update(func_results.iloc[0].to_dict())
                        _preserve_originals()
                        attribute_definition['Reference'] = True
                    elif len(func_results) > 1:
                        error = 'Multiple attributes returned by "%s":\n%s' % (func.__name__, func_results)
                    else:
                        error = 'No matching metadata row found for "%s"' % func.__name__

                elif isinstance(func_results, dict):
                    attribute_definition.update(func_results)
                    reference = _common.get(func_results, 'Reference')
                    if reference is not None:
                        if isinstance(reference, pd.DataFrame):
                            if len(reference) == 1:
                                attribute_definition = reference.iloc[0].to_dict()
                                _preserve_originals()
                                attribute_definition['Reference'] = True
                            elif len(reference) > 1:
                                error = 'Multiple attributes returned by "%s":\n%s' % (func.__name__, func_results)
                            else:
                                error = 'No matching metadata found for "%s"' % func.__name__

                if not _common.present(attribute_definition, 'Name'):
                    attribute_definition['Name'] = func.__name__.replace('_', ' ')

                attribute_definition['Asset'] = self.asset_definition['Name']

                Asset._add_asset_metadata(self, attribute_definition, error)

                return attribute_definition

            setattr(attribute_wrapper, 'spy_model', 'attribute')

            return attribute_wrapper

        return attribute_decorator

    @classmethod
    def Component(cls):
        def component_decorator(func):
            def component_wrapper(self, metadata):
                func_results = func(self, metadata)

                component_definitions = list()
                if func_results is None:
                    return component_definitions

                if not isinstance(func_results, list):
                    func_results = [func_results]

                for func_result in func_results:
                    if isinstance(func_result, _AssetBase):
                        _asset_obj = func_result  # type: _AssetBase
                        if not _common.present(_asset_obj.definition, 'Name'):
                            _asset_obj.definition['Name'] = func.__name__.replace('_', ' ')
                        build_results = _asset_obj.build(metadata)
                        component_definitions.extend(build_results)
                    elif isinstance(func_result, dict):
                        component_definition = func_result  # type: dict
                        Asset._add_asset_metadata(self, component_definition, None)
                        component_definitions.append(component_definition)

                return component_definitions

            setattr(component_wrapper, 'spy_model', 'component')

            return component_wrapper

        return component_decorator
