"""Тесты поиска вершин, достижимых из всех других."""

import pytest

from reachable import parse_graph, reachable_from_all


def test_example_from_readme():
    text = "3 3\n-1 0 0\n1 -1 1\n0 1 -1\n"
    assert reachable_from_all(*parse_graph(text)) == [1, 2]


def test_cycle_all_vertices():
    edges = [(0, 1), (1, 2), (2, 0)]
    assert reachable_from_all(3, edges) == [0, 1, 2]


def test_no_such_vertex():
    # две вершины без рёбер не достижимы друг из друга
    assert reachable_from_all(2, []) == []


def test_single_vertex():
    assert reachable_from_all(1, []) == [0]


def test_loop_is_parsed():
    assert parse_graph("1 1\n2\n") == (1, [(0, 0)])


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("2 1\n-1\n", id="too-few-rows"),
        pytest.param("2 1\n-1\n3\n", id="bad-value"),
        pytest.param("2 1\n-1\n-1\n", id="not-an-edge"),
    ],
)
def test_invalid_input(text):
    with pytest.raises(ValueError):
        parse_graph(text)


def test_no_edges_is_parsed():
    assert parse_graph("2 0\n") == (2, [])
    assert parse_graph("1 0\n\n") == (1, [])


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("0 -1\n", id="negative-m"),
        pytest.param("-1 0\n", id="negative-n"),
        pytest.param("2 1\na\n1\n", id="not-a-number"),
        pytest.param("2 1\n-1\n+1\n", id="plus-sign"),
        pytest.param("2 1\n-1\n0_1\n", id="underscore"),
    ],
)
def test_bad_numbers(text):
    with pytest.raises(ValueError, match="число|отрицательн"):
        parse_graph(text)
