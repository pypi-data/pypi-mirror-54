"""Test file for stream graph."""
from stream_graph import TemporalLinkSetDF
from stream_graph import StreamGraph
from nose.tools import assert_equal


def test_stream_graph():
    for d in [False, True]:
        for w in [False, True]:
            if w:
                df = [(1, 2, 2, 3, 1), (1, 2, 3, 5, 1), (2, 1, 6, 8, 1), (2, 1, 1, 3, 1)]
            else:
                df = [(1, 2, 2, 3), (1, 2, 3, 5), (2, 1, 6, 8), (2, 1, 1, 3)]

            sga = TemporalLinkSetDF(df, disjoint_intervals=False, weighted=w, discrete=d).as_stream_graph_basic

            assert isinstance(sga, StreamGraph)
            assert bool(sga)
            assert not bool(StreamGraph())

            assert_equal(sga.n, 2.0)
            assert_equal(sga.m, 1.0 + 0.25 * int(d))

            assert_equal(sga.coverage, 1.0)
            assert_equal(sga.density, 0.5 + 0.125 * int(d))

            assert_equal(sga.node_contribution_of(1), 1.0)
            assert_equal(dict(sga.node_contribution_of()), {1: 1.0, 2: 1.0})

            if d:
                assert_equal(dict(sga.link_density_of()), {(1, 2): 0.5, (2, 1): 0.75})
                assert_equal(sga.link_density_of((1, 2)), 0.5)
                assert_equal(sga.link_density_of((1, 2), direction='in'), 0.75)
                assert_equal(sga.link_density_of((1, 2), direction='both'), 1.0)
            else:
                assert_equal(dict(sga.link_density_of()), {(1, 2): 0.42857142857142855, (2, 1): 0.5714285714285714})
                assert_equal(sga.link_density_of((1, 2)), 0.42857142857142855)
                assert_equal(sga.link_density_of((1, 2), direction='in'), 0.5714285714285714)
                assert_equal(sga.link_density_of((1, 2), direction='both'), 0.8571428571428571)

            t = (2 if d else 2.5)
            assert_equal(sga.node_contribution_at(t), 1.0)
            assert_equal(sga.node_contribution_at(10), 0.)
            assert_equal(sga.node_contribution_at(t), 1.0)

            assert_equal(sga.link_contribution_at(t), 1.0)
            if d:
                assert_equal(list(sga.node_contribution_at()), [(1, 1.0), (9, 0.0)])
                assert_equal(list(sga.density_at()), [(1, 0.5), (2, 1.0), (4, 0.5), (9, 0.0)])
            else:
                assert_equal(list(sga.node_contribution_at()), [((1, True), 1.0), ((8, not w), 0.0)])
                assert_equal(list(sga.density_at()), [((1, True), 0.5), ((2, True), 1.0), ((3, w), 0.5), ((5, w), 0.0), ((6, True), 0.5), ((8, False), 0.0)])

            if d:
                assert_equal(sga.node_density_of(1), 0.75)
                assert_equal(sga.node_density_of(1, direction='in'), 0.5)
                assert_equal(sga.node_density_of(1, direction='both'), 1.0)
                assert_equal(dict(sga.node_density_of()), {1: 0.75, 2: 0.5})
            else:
                assert_equal(sga.node_density_of(1), 0.5714285714285714)
                assert_equal(sga.node_density_of(1, direction='in'), 0.42857142857142855)
                assert_equal(sga.node_density_of(1, direction='both'), 0.8571428571428571)
                assert_equal(dict(sga.node_density_of()), {1: 0.5714285714285714, 2: 0.42857142857142855})

            assert_equal(sga.neighbor_coverage_at(1, t, weights=w), 0.5)
            assert_equal(sga.neighbor_coverage_at(1, t, direction='in', weights=w), 0.5)
            assert_equal(sga.neighbor_coverage_at(1, t, direction='both', weights=w), 0.5 + int(w) * 0.5)  # should this be different?

            assert_equal(sga.mean_degree_at(2, weights=w), 1.0)
            if d:
                if w:
                    assert_equal(list(sga.mean_degree_at(weights=w)), [(1, 0.5), (2, 1.0), (3, 1.5), (4, 0.5), (9, 0.0)])
                else:
                    assert_equal(list(sga.mean_degree_at(weights=w)), [(1, 0.5), (2, 1.0), (4, 0.5), (9, 0.0)])
            else:
                assert_equal(list(sga.mean_degree_at(weights=w)), [((1, True), 0.5), ((2, True), 1.0), ((3, w), 0.5), ((5, w), 0.0), ((6, True), 0.5), ((8, False), 0.0)])


if __name__ == "__main__":
    test_stream_graph()
