from hyperopt import hp
import math
from pprint import pprint
import re

class Hyperparameter:
    """ This class represents a hyperparameter."""

    def __init__(self, config, parent=None, root='root'):
        self.config = config
        self.root = root
        self.name = root[5:]
        self.parent = parent
        self.resultVariableName = re.sub("\\.\\d+\\.", ".", self.name)

        self.hyperoptVariableName = self.root
        if 'name' in config:
            self.hyperoptVariableName = config['name']

    def createHyperoptSpace(self, lockedValues=None):
        name = self.root

        if lockedValues is None:
            lockedValues = {}

        if 'anyOf' in self.config or 'oneOf' in self.config:
            data = []
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            subSpaces = [Hyperparameter(param, self, name + "." + str(index)).createHyperoptSpace(lockedValues) for index, param in enumerate(data)]
            for index, space in enumerate(subSpaces):
                space["$index"] = index

            choices = hp.choice(self.hyperoptVariableName, subSpaces)

            return choices
        elif 'enum' in self.config:
            if self.name in lockedValues:
                return lockedValues[self.name]

            choices = hp.choice(self.hyperoptVariableName, self.config['enum'])
            return choices
        elif 'constant' in self.config:
            if self.name in lockedValues:
                return lockedValues[self.name]

            return self.config['constant']
        elif self.config['type'] == 'object':
            space = {}
            for key in self.config['properties'].keys():
                config = self.config['properties'][key]
                space[key] = Hyperparameter(config, self, name + "." + key).createHyperoptSpace(lockedValues)
            return space
        elif self.config['type'] == 'number':
            if self.name in lockedValues:
                return lockedValues[self.name]

            mode = self.config.get('mode', 'uniform')
            scaling = self.config.get('scaling', 'linear')

            if mode == 'uniform':
                min = self.config.get('min', 0)
                max = self.config.get('max', 1)
                rounding = self.config.get('rounding', None)

                if scaling == 'linear':
                    if rounding is not None:
                        return hp.quniform(self.hyperoptVariableName, min, max, rounding)
                    else:
                        return hp.uniform(self.hyperoptVariableName, min, max)
                elif scaling == 'logarithmic':
                    if rounding is not None:
                        return hp.qloguniform(self.hyperoptVariableName, math.log(min), math.log(max), rounding)
                    else:
                        return hp.loguniform(self.hyperoptVariableName, math.log(min), math.log(max))
            if mode == 'randint':
                max = self.config.get('max', 1)
                return hp.randint(self.hyperoptVariableName, max)

            if mode == 'normal':
                mean = self.config.get('mean', 0)
                stddev = self.config.get('stddev', 1)
                rounding = self.config.get('rounding', None)

                if scaling == 'linear':
                    if rounding is not None:
                        return hp.qnormal(self.hyperoptVariableName, mean, stddev, rounding)
                    else:
                        return hp.normal(self.hyperoptVariableName, mean, stddev)
                elif scaling == 'logarithmic':
                    if rounding is not None:
                        return hp.qlognormal(self.hyperoptVariableName, math.log(mean), math.log(stddev), rounding)
                    else:
                        return hp.lognormal(self.hyperoptVariableName, math.log(mean), math.log(stddev))

    def getFlatParameterNames(self):
        name = self.root

        if 'anyOf' in self.config or 'oneOf' in self.config:
            keys = set()
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            for index, param in enumerate(data):
                subKeys = Hyperparameter(param, self, name + "." + str(index)).getFlatParameterNames()
                for key in subKeys:
                    keys.add(key)

            return keys
        elif 'enum' in self.config or 'constant' in self.config:
            return [name]
        elif self.config['type'] == 'object':
            keys = set()
            for key in self.config['properties'].keys():
                config = self.config['properties'][key]
                subKeys = Hyperparameter(config, self, name + "." + key).getFlatParameterNames()
                for key in subKeys:
                    keys.add(key)

            return keys
        elif self.config['type'] == 'number':
            return [name]

    def getFlatParameters(self):
        name = self.root
        if 'anyOf' in self.config or 'oneOf' in self.config:
            parameters = []
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            for index, param in enumerate(data):
                subParameters = Hyperparameter(param, self, name + "." + str(index)).getFlatParameters()
                parameters = parameters + subParameters
            return parameters
        elif 'enum' in self.config or 'constant' in self.config:
            return [self]
        elif self.config['type'] == 'object':
            parameters = []
            for key in self.config['properties'].keys():
                config = self.config['properties'][key]
                subParameters = Hyperparameter(config, self, name + "." + key).getFlatParameters()
                parameters = parameters + subParameters
            return parameters
        elif self.config['type'] == 'number':
            return [self]

    def getLog10Cardinality(self):
        if 'anyOf' in self.config or 'oneOf' in self.config:
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            log10_cardinality = Hyperparameter(data[0], self, self.root + ".0").getLog10Cardinality()
            for index, subParam in enumerate(data[1:]):
                # We used logarithm identities to create this reduction formula
                other_log10_cardinality = Hyperparameter(subParam, self, self.root + "." + str(index)).getLog10Cardinality()

                # Revert to linear at high and low values, for numerical stability. Check here: https://www.desmos.com/calculator/efkbbftd18 to observe
                if (log10_cardinality - other_log10_cardinality) > 3:
                    log10_cardinality = log10_cardinality + 1
                elif (other_log10_cardinality - log10_cardinality) > 3:
                    log10_cardinality = other_log10_cardinality + 1
                else:
                    log10_cardinality = other_log10_cardinality + math.log10(1 + math.pow(10, log10_cardinality - other_log10_cardinality))
            return log10_cardinality + math.log10(len(data))
        elif 'enum' in self.config:
            return math.log10(len(self.config['enum']))
        elif 'constant' in self.config:
            return math.log10(1)
        elif self.config['type'] == 'object':
            log10_cardinality = 0
            for index, subParam in enumerate(self.config['properties'].values()):
                subParameter = Hyperparameter(subParam, self, self.root + "." + str(index))
                log10_cardinality += subParameter.getLog10Cardinality()
            return log10_cardinality
        elif self.config['type'] == 'number':
            if 'rounding' in self.config:
                return math.log10(min(20, (self.config['max'] - self.config['min']) / self.config['rounding'] + 1))
            else:
                return math.log10(20)  # Default of 20 for fully uniform numbers.

    def convertToFlatValues(self, params):
        flatParams = {}

        def recurse(key, value, root):
            result_key = root + "." + key
            if isinstance(value, str):
                flatParams[result_key[1:]] = value
            elif isinstance(value, float) or isinstance(value, bool) or isinstance(value, int):
                flatParams[result_key[1:]] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    recurse(subkey, subvalue, result_key)

        for key in params.keys():
            value = params[key]
            recurse(key, value, '')

        flatValues = {}

        if 'anyOf' in self.config or 'oneOf' in self.config:
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            subParameterIndex = flatParams[self.resultVariableName + '.$index']
            flatValues[self.name] = subParameterIndex

            for index, param in enumerate(data):
                subParameter = Hyperparameter(param, self, self.root + "." + str(index))

                if index == subParameterIndex:
                    subFlatValues = subParameter.convertToFlatValues(flatParams)
                    for key in subFlatValues:
                        flatValues[key] = subFlatValues[key]
                else:
                    for flatParam in subParameter.getFlatParameters():
                        flatValues[flatParam.name] = ""

            return flatValues
        elif 'constant' in self.config:
            flatValues[self.name] = flatParams[self.resultVariableName]
            return flatValues
        elif 'enum' in self.config:
            flatValues[self.name] = flatParams[self.resultVariableName]
            return flatValues
        elif self.config['type'] == 'object':
            for key in self.config['properties'].keys():
                config = self.config['properties'][key]

                subFlatValues = Hyperparameter(config, self, self.root + "." + key).convertToFlatValues(flatParams)

                for key in subFlatValues:
                    flatValues[key] = subFlatValues[key]

                if self.name == "":
                    for key in params.keys():
                        if key.startswith("$"):
                            flatValues[key] = params[key]

            return flatValues
        elif self.config['type'] == 'number':
            flatValues[self.name] = flatParams[self.resultVariableName]
            return flatValues

    def convertToStructuredValues(self, flatValues):
        if 'anyOf' in self.config or 'oneOf' in self.config:
            if 'anyOf' in self.config:
                data = self.config['anyOf']
            else:
                data = self.config['oneOf']

            subParameterIndex = flatValues[self.name]
            subParam = Hyperparameter(data[subParameterIndex], self, self.root + "." + str(subParameterIndex))

            structured = subParam.convertToStructuredValues(flatValues)
            structured['$index'] = subParameterIndex

            return structured
        elif 'constant' in self.config:
            return flatValues[self.name]
        elif 'enum' in self.config:
            return flatValues[self.name]
        elif self.config['type'] == 'object':
            result = {}
            for key in self.config['properties'].keys():
                config = self.config['properties'][key]

                subStructuredValue = Hyperparameter(config, self, self.root + "." + key).convertToStructuredValues(flatValues)

                result[key] = subStructuredValue

                if self.name == "":
                    for key in flatValues.keys():
                        if key.startswith("$"):
                            result[key] = flatValues[key]
            return result
        elif self.config['type'] == 'number':
            return flatValues[self.name]


    @staticmethod
    def createHyperparameterConfigForHyperoptDomain(domain):
        if domain.name is None:
            data = {
                "type": "object",
                "properties": {}
            }

            for key in domain.params:
                data['properties'][key] = Hyperparameter.createHyperparameterConfigForHyperoptDomain(domain.params[key])

                if 'name' not in data['properties'][key]:
                    data['properties'][key]['name'] = key

            return data
        elif domain.name == 'dict':
            data = {
                "type": "object",
                "properties": {}
            }

            for item in domain.named_args:
                data['properties'][item[0]] = Hyperparameter.createHyperparameterConfigForHyperoptDomain(item[1])

            return data
        elif domain.name == 'switch':
            data = {
                "oneOf": [

                ]
            }

            data['name'] = domain.pos_args[0].pos_args

            for item in domain.pos_args[1:]:
                data['oneOf'].append(Hyperparameter.createHyperparameterConfigForHyperoptDomain(item))
            return data
        elif domain.name == 'hyperopt_param':
            data = Hyperparameter.createHyperparameterConfigForHyperoptDomain(domain.pos_args[1])
            data['name'] = domain.pos_args[0]._obj
            return data
        elif domain.name == 'uniform':
            data = {"type": "number"}
            data['scaling'] = 'linear'
            data['mode'] = 'uniform'
            data['min'] = domain.pos_args[0]._obj
            data['max'] = domain.pos_args[1]._obj
            return data
        elif domain.name == 'quniform':
            data = {"type": "number"}
            data['scaling'] = 'linear'
            data['mode'] = 'uniform'
            data['min'] = domain.pos_args[0]._obj
            data['max'] = domain.pos_args[1]._obj
            data['rounding'] = domain.pos_args[2]._obj
            return data
        elif domain.name == 'loguniform':
            data = {"type": "number"}
            data['scaling'] = 'logarithmic'
            data['mode'] = 'uniform'
            data['min'] = math.exp(domain.pos_args[0]._obj)
            data['max'] = math.exp(domain.pos_args[1]._obj)
            return data
        elif domain.name == 'qloguniform':
            data = {"type": "number"}
            data['scaling'] = 'logarithmic'
            data['mode'] = 'uniform'
            data['min'] = math.exp(domain.pos_args[0]._obj)
            data['max'] = math.exp(domain.pos_args[1]._obj)
            data['rounding'] = domain.pos_args[2]._obj
            return data
        elif domain.name == 'normal':
            data = {"type": "number"}
            data['scaling'] = 'linear'
            data['mode'] = 'normal'
            data['mean'] = domain.pos_args[0]._obj
            data['stddev'] = domain.pos_args[1]._obj
            return data
        elif domain.name == 'qnormal':
            data = {"type": "number"}
            data['scaling'] = 'linear'
            data['mode'] = 'normal'
            data['mean'] = domain.pos_args[0]._obj
            data['stddev'] = domain.pos_args[1]._obj
            data['rounding'] = domain.pos_args[2]._obj
            return data
        elif domain.name == 'lognormal':
            data = {"type": "number"}
            data['scaling'] = 'logarithmic'
            data['mode'] = 'normal'
            data['mean'] = domain.pos_args[0]._obj
            data['stddev'] = domain.pos_args[1]._obj
            return data
        elif domain.name == 'qlognormal':
            data = {"type": "number"}
            data['scaling'] = 'logarithmic'
            data['mode'] = 'normal'
            data['mean'] = domain.pos_args[0]._obj
            data['stddev'] = domain.pos_args[1]._obj
            data['rounding'] = domain.pos_args[2]._obj
            return data
        elif domain.name == 'literal':
            data = {
                'type': 'string',
                'constant': domain._obj
            }
            return data
        elif domain.name == 'randint':
            data = {"type": "number"}
            max = domain.pos_args[0]._obj
            data['max'] = max
            data['mode'] = 'randint'
            return data
        else:
            raise ValueError(f"Unsupported hyperopt domain type {domain.name}")
