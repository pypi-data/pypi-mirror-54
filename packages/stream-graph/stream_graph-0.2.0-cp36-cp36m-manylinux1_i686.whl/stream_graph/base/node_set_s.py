from __future__ import absolute_import
from stream_graph import ABC
from stream_graph.exceptions import UnrecognizedNodeSet


class NodeSetS(ABC.NodeSet):
    """Set implementation of the ABC.NodeSet

    Parameters
    ----------
    nodes: Iterable, default=None
        The Iterable should contain a valid NodeId (int or str).

    """
    def __init__(self, nodes=None):
        if nodes is not None:
            self.nodes_ = set(nodes)

    def __bool__(self):
        return hasattr(self, 'nodes_') and (len(self.nodes_) > 0)

    @property
    def size(self):
        if bool(self):
            return len(self.nodes_)
        return 0

    def __contains__(self, n):
        if bool(self):
            return n in self.nodes_
        return False

    @property
    def nodes(self):
        if bool(self):
            return set(self.nodes_)
        else:
            return set()

    def issuperset(self, ns):
        if isinstance(ns, ABC.NodeSet):
            if bool(self):
                if not isinstance(ns, NodeSetS):
                    try:
                        return ns.issubset(self)
                    except (AttributeError, NotImplementedError):
                        ns = NodeSetS(ns)
                return NodeSetS(self.nodes & ns.nodes)
        else:
            raise UnrecognizedNodeSet('right operand')
        return False

    def __and__(self, ns):
        if isinstance(ns, ABC.NodeSet):
            if bool(self):
                if not isinstance(ns, NodeSetS):
                    try:
                        return ns & self
                    except NotImplementedError:
                        ns = NodeSetS(ns)
                return NodeSetS(self.nodes & ns.nodes)
        else:
            raise UnrecognizedNodeSet('right operand')
        return NodeSetS()

    def __or__(self, ns):
        if isinstance(ns, ABC.NodeSet):
            if bool(self):
                if not isinstance(ns, NodeSetS):
                    try:
                        return ns | self
                    except NotImplementedError:
                        ns = NodeSetS(ns)
                return NodeSetS(self.nodes | ns.nodes)
        else:
            raise UnrecognizedNodeSet('right operand')
        return ns.copy()

    def __sub__(self, ns):
        if isinstance(ns, ABC.NodeSet):
            if bool(self):
                if not isinstance(ns, NodeSetS):
                    try:
                        return ns.__rsub__(self)
                    except (AttributeError, NotImplementedError):
                        ns = NodeSetS(ns)
                return NodeSetS(self.nodes - ns.nodes)
        else:
            raise UnrecognizedNodeSet('right operand')
        return self.copy()

    def __iter__(self):
        if bool(self):
            return iter(self.nodes_)
        else:
            return iter({})
