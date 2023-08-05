# -*- coding: utf-8 -*-

"""The Unbiased Candidate Mechanism Pertubation Amplitude (UCMPA) workflow has four parts:

1) Assembling a network, pre-processing, and overlaying data
2) Generating unbiased candidate mechanisms from the network
3) Generating random subgraphs from each unbiased candidate mechanism
4) Applying standard heat diffusion to each subgraph and calculating scores for each unbiased candidate mechanism based
   on the distribution of scores for its subgraph

In this algorithm, heat is applied to the nodes based on the data set. For the differential gene expression experiment,
the log-fold-change values are used instead of the corrected p-values to allow for the effects of up- and
down-regulation to be admitted in the analysis. Finally, heat diffusion inspired by previous algorithms publsihed in
systems and networks biology [1]_ [2]_ is run with the constraint that decreases
edges cause the sign of the heat to be flipped. Because of the construction of unbiased candidate mechanisms, all
heat will flow towards their seed biological process nodes. The amount of heat on the biological process node after
heat diffusion stops becomes the score for the whole unbiased candidate mechanism.

The issue of inconsistent causal networks addressed by SST [3]_ does not affect heat diffusion algorithms
since it can quantify multiple conflicting pathways. However, it does not address the possibility of contradictory
edges, for example, when ``A increases B`` and ``A decreases B`` are both true. A random sampling approach is used on
networks with contradictory edges and aggregate statistics over multiple trials are used to assess the robustness of the
scores as a function of the topology of the underlying unbiases candidate mechanisms.

Invariants
~~~~~~~~~~
- Because heat always flows towards the biological process node, it is possible to remove leaf nodes (nodes with no
  incoming edges) after each step, since their heat will never change.

Examples
~~~~~~~~
This workflow has been applied in several Jupyter notebooks:

- `Unbiased Candidate Mechanism Pertubation Amplitude Workflow <http://nbviewer.jupyter.org/github/pybel/pybel-notebooks/blob/master/algorithms/Candidate%20Mechanism%20Perturbation%20Amplitude%20Algorithm.ipynb>`_
- `Time Series UCMPA <http://nbviewer.jupyter.org/github/pybel/pybel-notebooks/blob/master/algorithms/Time%20Series%20CMPA.ipynb>`_

Future Work
~~~~~~~~~~~
This algorithm can be tuned to allow the use of correlative relationships. Because many multi-scale and multi-modal
data are often measured with correlations to molecular features, this enables experiments to be run using SNP or
brain imaging features, whose experiments often measure their correlation with the activity of gene products.

.. [1] Bernabò N., *et al.* (2014). `The biological networks in studying cell signal transduction complexity: The
       examples of sperm capacitation and of endocannabinoid system
       <https://www.sciencedirect.com/science/article/pii/S2001037014000282?via%3Dihub>`_. Computational and Structural
       Biotechnology Journal, 11 (18), 11–21.
.. [2] Leiserson, M. D. M., *et al.* (2015). `Pan-cancer network analysis identifies combinations of rare somatic
       mutations across pathways and protein complexes <https://www.nature.com/articles/ng.3168>`_. Nature Genetics,
       47 (2), 106–14.
.. [3] Vasilyev, D. M., *et al.* (2014). `An algorithm for score aggregation over causal biological networks based on
       random walk sampling <https://doi.org/10.1186/1756-0500-7-516>`_. BMC Research Notes, 7, 516.
"""

from __future__ import print_function

import logging
import random
from collections import defaultdict
from operator import itemgetter

import numpy as np
from scipy import stats
from tqdm import tqdm

from pybel.constants import BIOPROCESS, CAUSAL_DECREASE_RELATIONS, CAUSAL_INCREASE_RELATIONS, RELATION
from ..filters.node_selection import get_nodes_by_function
from ..generation import generate_bioprocess_mechanisms, generate_mechanism
from ..grouping import get_subgraphs_by_annotation

__all__ = [
    'RESULT_LABELS',
    'Runner',
    'multirun',
    'workflow_aggregate',
    'workflow',
    'workflow_all',
    'workflow_all_aggregate',
    'calculate_average_score_by_annotation',
    'calculate_average_scores_on_subgraphs',
]

log = logging.getLogger(__name__)

#: Signifies the CMPA score in the node's data dictionary
CMPA_SCORE = 'score'

#: The default score for CMPA
DEFAULT_SCORE = 0

#: The columns in the score tuples
RESULT_LABELS = [
    'avg',
    'stddev',
    'normality',
    'median',
    'neighbors',
    'subgraph_size',
]


class Runner:
    """This class houses the data related to a single run of the CMPA analysis"""

    def __init__(self, graph, target_node, key, tag=None, default_score=None):
        """Initializes the CMPA runner class

        :param pybel.BELGraph graph: A BEL graph
        :param tuple target_node: The BEL node that is the focus of this analysis
        :param str key: The key for the nodes' data dictionaries that points to their original experimental measurements
        :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
        :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
        """
        self.graph = graph.copy()
        self.target_node = target_node
        self.key = key

        self.default_score = DEFAULT_SCORE if default_score is None else default_score
        self.tag = CMPA_SCORE if tag is None else tag

        for node, data in self.graph.iter_node_data_pairs():
            if not self.graph.predecessors(node):
                self.graph.node[node][self.tag] = data.get(key, 0)
                log.log(5, 'initializing %s with %s', target_node, self.graph.node[node][self.tag])

    def iter_leaves(self):
        """Returns an iterable over all nodes that are leaves. A node is a leaf if either:

         - it doesn't have any predecessors, OR
         - all of its predecessors have CMPA score in their data dictionaries

        :return: An iterable over all leaf nodes
        :rtype: iter
        """
        for node in self.graph:
            if self.tag in self.graph.node[node]:
                continue

            if not any(self.tag not in self.graph.node[p] for p in self.graph.predecessors_iter(node)):
                yield node

    def has_leaves(self):
        """Returns if the current graph has any leaves.

        Implementation is not that smart currently, and does a full sweep.

        :return: Does the current graph have any leaves?
        :rtype: bool
        """
        leaves = list(self.iter_leaves())
        return leaves

    def in_out_ratio(self, node):
        """Calculates the ratio of in-degree / out-degree of a node

        :param tuple node: A BEL node
        :return: The in-degree / out-degree ratio for the given node
        :rtype: float
        """
        return self.graph.in_degree(node) / float(self.graph.out_degree(node))

    def unscored_nodes_iter(self):
        """Iterates over all nodes without a CMPA score"""
        for node, data in self.graph.iter_node_data_pairs():
            if self.tag not in data:
                yield node

    def get_random_edge(self):
        """This function should be run when there are no leaves, but there are still unscored nodes. It will introduce
        a probabilistic element to the algorithm, where some edges are disregarded randomly to eventually get a score
        for the network. This means that the CMPA score can be averaged over many runs for a given graph, and a better
        data structure will have to be later developed that doesn't destroy the graph (instead, annotates which edges
        have been disregarded, later)

           1. get all unscored
           2. rank by in-degree
           3. weighted probability over all in-edges where lower in-degree means higher probability
           4. pick randomly which edge

        :return: A random in-edge to the lowest in/out degree ratio node. This is a 3-tuple of (node, node, key)
        :rtype: tuple
        """
        nodes = [
            (n, self.in_out_ratio(n))
            for n in self.unscored_nodes_iter()
            if n != self.target_node
        ]

        node, deg = min(nodes, key=itemgetter(1))
        log.log(5, 'checking %s (in/out ratio: %.3f)', node, deg)

        possible_edges = self.graph.in_edges(node, keys=True)
        log.log(5, 'possible edges: %s', possible_edges)

        edge_to_remove = random.choice(possible_edges)
        log.log(5, 'chose: %s', edge_to_remove)

        return edge_to_remove

    def remove_random_edge(self):
        """Removes a random in-edge from the node with the lowest in/out degree ratio"""
        u, v, k = self.get_random_edge()
        log.log(5, 'removing %s, %s (%s)', u, v, k)
        self.graph.remove_edge(u, v, k)

    def remove_random_edge_until_has_leaves(self):
        """Removes random edges until there is at least one leaf node"""
        while True:
            leaves = set(self.iter_leaves())
            if leaves:
                return
            self.remove_random_edge()

    def score_leaves(self):
        """Calculates the CMPA score for all leaves

        :return: The set of leaf nodes that were scored
        :rtype: set
        """
        leaves = set(self.iter_leaves())

        if not leaves:
            log.warning('no leaves.')
            return set()

        for leaf in leaves:
            self.graph.node[leaf][self.tag] = self.calculate_score(leaf)
            log.log(5, 'chomping %s', leaf)

        return leaves

    def run(self):
        """Calculates CMPA scores for all leaves until there are none, removes edges until there are, and repeats until
        all nodes have been scored
        """
        while not self.done_chomping():
            self.remove_random_edge_until_has_leaves()
            self.score_leaves()

    def run_with_graph_transformation(self):
        """Calculates CMPA scores for all leaves until there are none, removes edges until there are, and repeats until
        all nodes have been scored. Also, yields the current graph at every step so you can make a cool animation
        of how the graph changes throughout the course of the algorithm

        :return: An iterable of BEL graphs
        :rtype: iter
        """
        yield self.get_remaining_graph()
        while not self.done_chomping():
            while not list(self.iter_leaves()):
                self.remove_random_edge()
                yield self.get_remaining_graph()
            self.score_leaves()
            yield self.get_remaining_graph()

    def done_chomping(self):
        """Determines if the algorithm is complete by checking if the target node of this analysis has been scored
        yet. Because the algorithm removes edges when it gets stuck until it is un-stuck, it is always guaranteed to
        finish.

        :return: Is the algorithm done running?
        :rtype: bool
        """
        return self.tag in self.graph.node[self.target_node]

    def get_final_score(self):
        """Returns the final score for the target node

        :return: The final score for the target node
        :rtype: float
        """
        if not self.done_chomping():
            raise ValueError('Algorithm has not completed')

        return self.graph.node[self.target_node][self.tag]

    def calculate_score(self, node):
        """Calculates the score of the given node

        :param tuple node: A node in the BEL graph
        :return: The new score of the node
        :rtype: float
        """
        score = self.graph.node[node][self.tag] if self.tag in self.graph.node[node] else self.default_score

        for predecessor, _, d in self.graph.in_edges_iter(node, data=True):
            if d[RELATION] in CAUSAL_INCREASE_RELATIONS:
                score += self.graph.node[predecessor][self.tag]
            elif d[RELATION] in CAUSAL_DECREASE_RELATIONS:
                score -= self.graph.node[predecessor][self.tag]

        return score

    def get_remaining_graph(self):
        """Allows for introspection on the algorithm at a given point by returning the subgraph induced
        by all unscored nodes

        :return: The remaining unscored BEL graph
        :rtype: pybel.BELGraph
        """
        return self.graph.subgraph(self.unscored_nodes_iter())


def multirun(graph, node, key, tag=None, default_score=None, runs=None, use_tqdm=False):
    """Runs CMPA multiple times and yields the :class:`Runner` object after each run has been completed

    :param pybel.BELGraph graph: A BEL graph
    :param tuple node: The BEL node that is the focus of this analysis
    :param str key: The key for the nodes' data dictionaries that points to their original experimental measurements
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :param bool use_tqdm: Should there be a progress bar for runners?
    :return: An iterable over the runners after each iteration
    :rtype: iter[Runner]
    """
    runs = 1000 if runs is None else runs
    it = range(runs)

    if use_tqdm:
        it = tqdm(it, total=runs, desc=str(graph))

    for i in it:
        try:
            runner = Runner(graph, node, key, tag=tag, default_score=default_score)
            runner.run()
            yield runner
        except Exception:
            log.debug('Run %s failed for %s', i, node)


def workflow(graph, node, key, tag=None, default_score=None, runs=None):
    """Generates candidate mechanisms and runs CMPA.

    :param pybel.BELGraph graph: A BEL graph
    :param tuple node: The BEL node that is the focus of this analysis
    :param str key: The key in the node data dictionary representing the experimental data
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :return: A list of runners
    :rtype: list[Runner]
    """
    sg = generate_mechanism(graph, node, key)

    if sg.number_of_nodes() <= 1:  # Don't even bother trying to get reasonable scores if it's too small
        return []

    runners = multirun(sg, node, key, tag=tag, default_score=default_score, runs=runs)
    return list(runners)


def workflow_aggregate(graph, node, key, tag=None, default_score=None, runs=None, aggregator=None):
    """Gets the average CMPA score over multiple runs.

    This function is very simple, and can be copied to do more interesting statistics over the :class:`Runner`
    instances. To iterate over the runners themselves, see :func:`workflow`

    :param pybel.BELGraph graph: A BEL graph
    :param tuple node: The BEL node that is the focus of this analysis
    :param str key: The key for the nodes' data dictionaries that points to their original experimental measurements
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :param aggregator: A function that aggregates a list of scores. Defaults to :func:`numpy.average`.
                       Could also use: :func:`numpy.mean`, :func:`numpy.median`, :func:`numpy.min`, :func:`numpy.max`
    :type aggregator: Optional[list[float] -> float]
    :return: The average score for the target node
    :rtype: float
    """
    runners = workflow(graph, node, key, tag=tag, default_score=default_score, runs=runs)
    scores = [runner.get_final_score() for runner in runners]

    if not scores:
        log.warning('Unable to run CMPA on %s', node)
        return None

    if aggregator is None:
        return np.average(scores)

    return aggregator(scores)


def workflow_all(graph, key, tag=None, default_score=None, runs=None):
    """Runs CMPA and get runners for every possible candidate mechanism

    1. Get all biological processes
    2. Get candidate mechanism induced two level back from each biological process
    3. CMPA on each candidate mechanism for multiple runs
    4. Return all runner results

    :param pybel.BELGraph graph: A BEL graph
    :param str key: The key in the node data dictionary representing the experimental data
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :return: A dictionary of {node: list of runners}
    :rtype: dict
    """
    results = {}

    for node in get_nodes_by_function(graph, BIOPROCESS):
        results[node] = workflow(graph, node, key, tag=tag, default_score=default_score, runs=runs)

    return results


def workflow_all_aggregate(graph, key, tag=None, default_score=None, runs=None, aggregator=None):
    """Runs CMPA to get average score for every possible candidate mechanism

    1. Get all biological processes
    2. Get candidate mechanism induced two level back from each biological process
    3. CMPA on each candidate mechanism for multiple runs
    4. Report average CMPA scores for each candidate mechanism

    :param pybel.BELGraph graph: A BEL graph
    :param str key: The key in the node data dictionary representing the experimental data
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :param aggregator: A function that aggregates a list of scores. Defaults to :func:`numpy.average`.
                       Could also use: :func:`numpy.mean`, :func:`numpy.median`, :func:`numpy.min`, :func:`numpy.max`
    :type aggregator: Optional[list[float] -> float]
    :return: A dictionary of {node: upstream causal subgraph}
    :rtype: dict
    """
    results = {}

    for node in get_nodes_by_function(graph, BIOPROCESS):
        sg = generate_mechanism(graph, node, key)

        try:
            results[node] = workflow_aggregate(
                graph=sg,
                node=node,
                key=key,
                tag=tag,
                default_score=default_score,
                runs=runs,
                aggregator=aggregator
            )
        except Exception:
            log.exception('could not run on %', node)

    return results


def calculate_average_scores_on_subgraphs(candidate_mechanisms, key, tag=None, default_score=None, runs=None,
                                          use_tqdm=False):
    """Calculates the scores over precomputed candidate mechanisms
    
    :param candidate_mechanisms: A dictionary of {tuple node: pybel.BELGraph candidate mechanism}
    :type candidate_mechanisms: dict[tuple, pybel.BELGraph]
    :param str key: The key in the node data dictionary representing the experimental data
    :param str tag: The key for the nodes' data dictionaries where the CMPA scores will be put. Defaults to 'score'
    :param float default_score: The initial CMPA score for all nodes. This number can go up or down.
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :return: A dictionary of {pybel node tuple: results tuple}
    :rtype: dict[tuple, tuple]
    
    Example Usage:
    
    >>> import pandas as pd
    >>> import pybel_tools as pbt
    >>> from pybel_tools.analysis.cmpa import *
    >>> # load graph and data
    >>> key = ...
    >>> graph = ...
    >>> candidate_mechanisms = pbt.generation.generate_bioprocess_mechanisms(graph, key)
    >>> scores = calculate_average_scores_on_subgraphs(candidate_mechanisms, key)
    >>> pd.DataFrame.from_items(scores.items(), orient='index', columns=RESULT_LABELS)
    """
    results = {}

    log.info('calculating results for %d candidate mechanisms using %d permutations', len(candidate_mechanisms), runs)

    it = candidate_mechanisms.items()

    if use_tqdm:
        it = tqdm(it, total=len(candidate_mechanisms), desc='Candidate mechanisms')

    for node, subgraph in it:
        number_first_neighbors = subgraph.in_degree(node)
        number_first_neighbors = 0 if isinstance(number_first_neighbors, dict) else number_first_neighbors
        mechanism_size = subgraph.number_of_nodes()

        runners = workflow(subgraph, node, key, tag=tag, default_score=default_score, runs=runs)
        scores = [runner.get_final_score() for runner in runners]

        if 0 == len(scores):
            results[node] = (
                None,
                None,
                None,
                None,
                number_first_neighbors,
                mechanism_size,
            )
            continue

        scores = np.array(scores)

        average_score = np.average(scores)
        score_std = np.std(scores)
        med_score = np.median(scores)
        chi_2_stat, norm_p = stats.normaltest(scores)

        results[node] = (
            average_score,
            score_std,
            norm_p,
            med_score,
            number_first_neighbors,
            mechanism_size,
        )

    return results


# TODO reinvestigate statistical bootstrapping/resampling/distribution normalization
def calculate_average_score_by_annotation(graph, key, annotation, runs=None):
    """For each subgraph induced over the edges matching the annotation, calculate the average CMPA score
    for all of the contained biological processes

    Assumes you haven't done anything yet

    1. Generates biological process upstream candidate mechanistic subgraphs with :func:`generate_bioprocess_mechanisms`
    2. Calculates scores for each subgraph with :func:`calculate_average_scores_on_subgraphs`
    3. Overlays data with pbt.integration.overlay_data
    4. Calculates averages with pbt.selection.group_nodes.average_node_annotation

    :param pybel.BELGraph graph: A BEL graph
    :param str key: The key in the node data dictionary representing the experimental data
    :param str annotation: A BEL annotation
    :param int runs: The number of times to run the CMPA algorithm. Defaults to 1000.
    :return: A dictionary from {str annotation value: tuple scores}
    :rtype: dict[str,tuple]


    Example Usage:

    >>> import pybel
    >>> from pybel_tools.integration import overlay_data
    >>> from pybel_tools.analysis.ucmpa import calculate_average_score_by_annotation
    >>> graph = pybel.from_path(...)
    >>> key = ...
    >>>
    >>> scores = calculate_average_score_by_annotation(graph, key, 'Subgraph')
    """
    candidate_mechanisms = generate_bioprocess_mechanisms(graph, key)

    #: {bp tuple: list of scores}
    scores = calculate_average_scores_on_subgraphs(candidate_mechanisms, key, runs=runs)

    subgraphs = get_subgraphs_by_annotation(graph, annotation)

    subgraph_bp = defaultdict(list)

    for annotation_value, subgraph in subgraphs.items():
        subgraph_bp[annotation_value].extend(get_nodes_by_function(subgraph, BIOPROCESS))

    final_scores = {}
    for annotation_value, bps in subgraph_bp.items():
        #: Pick the average by slicing with 0. Refer to :func:`calculate_average_score_on_subgraphs`
        bp_scores = [scores[bp][0] for bp in bps]
        final_scores[annotation_value] = np.average(bp_scores)

    return scores
