# -*- coding: utf-8 -*-

import os
import json
import time
import numpy as np
from typing import List, Dict, Optional
from collections import ChainMap
import importlib.resources as pkg_resources

from openfisca_core.parameters import ParameterNodeAtInstant, VectorialParameterNodeAtInstant, ALLOWED_PARAM_TYPES
from openfisca_core.indexed_enums import EnumArray


class TracingParameterNodeAtInstant:

    def __init__(self, parameter_node_at_instant, tracer):
        self.parameter_node_at_instant = parameter_node_at_instant
        self.tracer = tracer

    def __getattr__(self, key):
        child = getattr(self.parameter_node_at_instant, key)
        return self.get_traced_child(child, key)

    def __getitem__(self, key):
        child = self.parameter_node_at_instant[key]
        return self.get_traced_child(child, key)

    def get_traced_child(self, child, key):
        period = self.parameter_node_at_instant._instant_str
        if isinstance(child, (ParameterNodeAtInstant, VectorialParameterNodeAtInstant)):
            return TracingParameterNodeAtInstant(child, self.tracer)
        if not isinstance(key, str) or isinstance(self.parameter_node_at_instant, VectorialParameterNodeAtInstant):
            # In case of vectorization, we keep the parent node name as, for instance, rate[status].zone1 is best described as the value of "rate"
            name = self.parameter_node_at_instant._name
        else:
            name = '.'.join([self.parameter_node_at_instant._name, key])
        if isinstance(child, (np.ndarray,) + ALLOWED_PARAM_TYPES):
            self.tracer.record_parameter_access(name, period, child)
        return child


class SimpleTracer:

    def __init__(self):
        self._stack = []

    def record_calculation_start(self, variable: str, period):
        self.stack.append({'name': variable, 'period': period})

    def record_calculation_result(self, value: np.ndarray):
        pass  # ignore calculation result

    def record_parameter_access(self, parameter: str, period, value):
        pass

    def record_calculation_end(self):
        self.stack.pop()

    @property
    def stack(self):
        return self._stack


class FullTracer:

    def __init__(self):
        self._simple_tracer = SimpleTracer()
        self._trees = []
        self._current_node = None

    def record_calculation_start(self, variable: str, period):
        self._simple_tracer.record_calculation_start(variable, period)
        self._enter_calculation(variable, period)
        self._record_start_time()

    def _enter_calculation(self, variable: str, period):
        new_node = {'name': variable, 'period': period, 'children': [], 'parent': self._current_node, 'parameters': [], 'value': None}
        if self._current_node is None:
            self._trees.append(new_node)
        else:
            self._current_node['children'].append(new_node)
        self._current_node = new_node

    def record_parameter_access(self, parameter: str, period, value):
        self._current_node['parameters'].append({'name': parameter, 'period': period, 'value': value})

    def _record_start_time(self, time_in_s: Optional[float] = None):
        if time_in_s is None:
            time_in_s = self._get_time_in_sec()

        self._current_node['start'] = time_in_s

    def record_calculation_result(self, value: np.ndarray):
        self._current_node['value'] = value

    def record_calculation_end(self):
        self._simple_tracer.record_calculation_end()
        self._record_end_time()
        self._exit_calculation()

    def _record_end_time(self, time_in_s: Optional[float] = None):
        if time_in_s is None:
            time_in_s = self._get_time_in_sec()

        self._current_node['end'] = time_in_s

    def _exit_calculation(self):
        self._current_node = self._current_node['parent']

    @property
    def stack(self):
        return self._simple_tracer.stack

    @property
    def trees(self):
        return self._trees

    @property
    def computation_log(self):
        return ComputationLog(self)

    @property
    def performance_log(self):
        return PerformanceLog(self)

    def _get_time_in_sec(self) -> float:
        return time.time_ns() / (10**9)

    def print_computation_log(self, aggregate = False):
        self.computation_log.print_log(aggregate)

    def generate_performance_graph(self, dir_path):
        self.performance_log.generate_graph(dir_path)

    def _get_nb_requests(self, tree, variable: str):
        tree_call = tree['name'] == variable
        children_calls = sum(self._get_nb_requests(child, variable) for child in tree['children'])

        return tree_call + children_calls

    def get_nb_requests(self, variable: str):
        return sum(self._get_nb_requests(tree, variable) for tree in self.trees)

    def key(self, node):
        name = node['name']
        period = node['period']
        return f"{name}<{period}>"

    def get_flat_trace(self):
        trace = {}
        for tree in self._trees:
            trace = {**self._get_flat_trace(tree), **trace}
        return trace

    def serialize(self, value):
        if isinstance(value, EnumArray):
            value = [item.name for item in value.decode()]
        elif isinstance(value, np.ndarray):
            value = value.tolist()
            if len(value) > 0 and isinstance(value[0], bytes):
                value = [str(item) for item in value]
        return value

    def _get_flat_trace(self, node: Dict) -> Dict[str, Dict]:
        key = self.key(node)
        node_trace = {
            key: {
                'dependencies': [
                    self.key(child) for child in node['children']
                    ],
                'parameters': {
                    self.key(parameter): self.serialize(parameter['value']) for parameter in node['parameters']
                    },
                'value': self.serialize(node['value'])
                }
            }
        child_traces = [self._get_flat_trace(child) for child in node['children']]
        return dict(ChainMap(node_trace, *child_traces))


class ComputationLog:

    def __init__(self, full_tracer):
        self._full_tracer = full_tracer

    def display(self, value):
        if isinstance(value, EnumArray):
            value = value.decode_to_str()

        return np.array2string(value, max_line_width = float("inf"))

    def _get_node_log(self, node, depth, aggregate) -> List[str]:

        def print_line(depth, node) -> str:
            value = node['value']
            if aggregate:
                try:
                    formatted_value = str({'avg': np.mean(value), 'max': np.max(value), 'min': np.min(value)})
                except TypeError:
                    formatted_value = "{'avg': '?', 'max': '?', 'min': '?'}"
            else:
                formatted_value = self.display(value)

            return "{}{}<{}> >> {}".format('  ' * depth, node['name'], node['period'], formatted_value)

        # if not self.trace.get(node):
        #     return print_line(depth, node, "Calculation aborted due to a circular dependency")

        node_log = [print_line(depth, node)]
        children_logs = self._flatten(
            self._get_node_log(child, depth + 1, aggregate)
            for child in node['children']
            )

        return node_log + children_logs

    def _flatten(self, list_of_lists):
        return [item for _list in list_of_lists for item in _list]

    def lines(self, aggregate = False) -> List[str]:
        depth = 1
        lines_by_tree = [self._get_node_log(node, depth, aggregate) for node in self._full_tracer.trees]
        return self._flatten(lines_by_tree)

    def print_log(self, aggregate = False):
        """
            Print the computation log of a simulation.

            If ``aggregate`` is ``False`` (default), print the value of each computed vector.

            If ``aggregate`` is ``True``, only print the minimum, maximum, and average value of each computed vector.
            This mode is more suited for simulations on a large population.
        """
        for line in self.lines(aggregate):
            print(line)  # noqa T001


class PerformanceLog:

    def __init__(self, full_tracer):
        self._full_tracer = full_tracer

    def generate_graph(self, dir_path):
        with open(os.path.join(dir_path, 'index.html'), 'w') as f:
            template = pkg_resources.read_text('openfisca_core.scripts.assets', 'index.html')
            perf_graph_html = template.replace('{{data}}', json.dumps(self._json()))
            f.write(perf_graph_html)

    def _json(self):
        children = [self._json_tree(tree) for tree in self._full_tracer.trees]
        calculations_total_time = sum(child['value'] for child in children)
        return {'name': 'All calculations', 'value': calculations_total_time, 'children': children}

    def _json_tree(self, tree):
        calculation_total_time = tree['end'] - tree['start']
        children = [self._json_tree(child) for child in tree['children']]
        return {'name': f"{tree['name']}<{tree['period']}>", 'value': calculation_total_time, 'children': children}
