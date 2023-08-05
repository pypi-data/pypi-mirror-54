# -*- coding: utf-8 -*-

from pybel.constants import GENE, RELATION, RNA, TRANSCRIBED_TO, TRANSLATED_TO
from pybel.struct.filters import filter_nodes
from ..filters.node_filters import data_missing_key_builder, node_is_upstream_leaf
from ..filters.node_selection import get_nodes_by_function

__all__ = [
    'get_upstream_leaves',
    'get_unweighted_upstream_leaves',
    'get_gene_leaves',
    'get_rna_leaves',
]


def get_upstream_leaves(graph):
    """Gets all leaves of the graph (with no incoming edges and only one outgoing edge)

    .. seealso:: :func:`upstream_leaf_predicate`

    :param pybel.BELGraph graph: A BEL graph
    :return: An iterator over nodes that are upstream leaves
    :rtype: iter[tuple]
    """
    return filter_nodes(graph, node_is_upstream_leaf)


def get_unweighted_upstream_leaves(graph, key):
    """Gets all leaves of the graph with no incoming edges, one outgoing edge, and without the given key in
    its data dictionary

    .. seealso :: :func:`data_does_not_contain_key_builder`

    :param pybel.BELGraph graph: A BEL graph
    :param str key: The key in the node data dictionary representing the experimental data
    :return: An iterable over leaves (nodes with an in-degree of 0) that don't have the given annotation
    :rtype: iter[tuple]
    """
    return filter_nodes(graph, [node_is_upstream_leaf, data_missing_key_builder(key)])


def get_gene_leaves(graph):
    """Iterate over all genes who have only one connection, that's a transcription to its RNA

    :param pybel.BELGraph graph: A BEL graph
    :rtype: iter[tuple]
    """
    for node in get_nodes_by_function(graph, GENE):
        if graph.in_degree(node) != 0:
            continue

        if graph.out_degree(node) != 1:
            continue

        _, _, d = graph.out_edges(node, data=True)[0]

        if d[RELATION] == TRANSCRIBED_TO:
            yield node


def get_rna_leaves(graph):
    """Iterate over all RNAs who have only one connection, that's a translation to its protein

    :param pybel.BELGraph graph: A BEL graph
    :rtype: iter[tuple]
    """
    for node in get_nodes_by_function(graph, RNA):
        if graph.in_degree(node) != 0:
            continue

        if graph.out_degree(node) != 1:
            continue

        _, _, d = graph.out_edges(node, data=True)[0]

        if d[RELATION] == TRANSLATED_TO:
            yield node
