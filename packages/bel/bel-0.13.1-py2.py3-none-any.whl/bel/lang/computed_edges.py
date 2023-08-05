# Compute Edges related code

from typing import List, Any, Mapping, MutableSequence

from bel.lang.ast import BELAst, Function, NSArg

import logging
log = logging.getLogger(__name__)

# Typings
Edges = MutableSequence[Mapping[str, Any]]
BELSpec = Mapping[str, Any]
ComputeRules = List[str]


def compute_edges(ast: BELAst, spec: BELSpec, compute_rules: ComputeRules = None) -> Edges:
    """Compute BEL Edges from BEL AST

    Args:
        ast (BELAst): BEL ASTf
        spec (Mapping[str, Any]): BEL specification dictionary
        compute_rules (List[str]): only process listed compute rules or all rules if None

    Returns:
        List[Tuple[Union[Function, str], str, Function]]: edge list of (subject_ast, relation, object_ast)
    """
    edges = []

    # Expose nested assertion as edge
    if compute_rules and 'nested' in compute_rules and ast.bel_object.__class__.__name__ == 'BELAst':
        edges.append(ast.bel_object)

    for rule in spec['computed_signatures']:
        if compute_rules and rule not in compute_rules:
            continue
        elif spec['computed_signatures'][rule] is True:
            continue

        log.debug(f'Starting rule {rule}')

        process_rule(edges, ast, spec['computed_signatures'][rule], spec)

    return edges


def process_rule(edges: Edges, ast: Function, rule: Mapping[str, Any], spec: BELSpec):
    """Process computed edge rule

    Recursively processes BELAst versus a single computed edge rule

    Args:
        edges (List[Tuple[Union[Function, str], str, Function]]): BEL Edge ASTs
        ast (Function): BEL Function AST
        rule (Mapping[str, Any]: computed edge rule
    """
    ast_type = ast.__class__.__name__
    trigger_functions = rule.get('trigger_function', [])
    trigger_types = rule.get('trigger_type', [])
    rule_subject = rule.get('subject')
    rule_relation = rule.get('relation')
    rule_object = rule.get('object')

    log.debug(f'Running {rule_relation}  Type: {ast_type}')

    if isinstance(ast, Function):
        function_name = ast.name
        args = ast.args
        parent_function = ast.parent_function

        if function_name in trigger_functions:
            if rule_subject == 'trigger_value':
                subject = ast

            if rule_object == 'args':
                for arg in args:
                    log.debug(f'1: {subject} {arg}')
                    edge_ast = BELAst(subject, rule_relation, arg, spec)
                    edges.append(edge_ast)
            elif rule_object == 'parent_function' and parent_function:
                log.debug(f'2: {subject} {parent_function}')
                edge_ast = BELAst(subject, rule_relation, parent_function, spec)
                edges.append(edge_ast)

        elif ast_type in trigger_types:
            if rule_subject == 'trigger_value':
                subject = ast

            if rule_object == 'args':
                for arg in args:
                    log.debug(f'3: {subject} {arg}')
                    edge_ast = BELAst(subject, rule_relation, arg, spec)
                    edges.append(edge_ast)
            elif rule_object == 'parent_function' and parent_function:
                log.debug(f'4: {subject} {parent_function}')
                edge_ast = BELAst(subject, rule_relation, parent_function, spec)
                edges.append(edge_ast)

    if isinstance(ast, NSArg):
        term = "{}:{}".format(ast.namespace, ast.value)
        parent_function = ast.parent_function

        if ast_type in trigger_types:
            if rule_subject == 'trigger_value':
                subject = term

            if rule_object == 'args':
                for arg in args:
                    log.debug(f'5: {subject} {arg}')
                    edge_ast = BELAst(subject, rule_relation, arg, spec)
                    edges.append(edge_ast)
            elif rule_object == 'parent_function' and parent_function:
                log.debug(f'6: {subject} {parent_function}')
                edge_ast = BELAst(subject, rule_relation, parent_function, spec)
                edges.append(edge_ast)

    # Recursively process every element by processing BELAst and Functions
    if hasattr(ast, 'args'):
        for arg in ast.args:
            process_rule(edges, arg, rule, spec)

