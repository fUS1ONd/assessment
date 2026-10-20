"""Поиск вершин ориентированного графа, достижимых из всех других вершин.

Граф читается из файла с матрицей инцидентности, формат описан в README.md.
Запуск: python reachable.py <файл>
"""

import re
import sys
from collections import deque

_INT = re.compile(r"-?[0-9]+")


def _to_int(token):
    """Переводит токен в целое число, допуская только цифры и минус."""
    if not _INT.fullmatch(token):
        raise ValueError(f"не число: {token!r}")
    return int(token)


def parse_graph(text):
    """Разбирает матрицу инцидентности и возвращает пару (n, edges).

    edges — список рёбер в виде пар (откуда, куда).
    При некорректных данных бросает ValueError.
    """
    lines = [line.split() for line in text.splitlines() if line.strip()]
    if not lines or len(lines[0]) != 2:
        raise ValueError("первая строка должна содержать n и m")
    n, m = (_to_int(x) for x in lines[0])
    if n < 0 or m < 0:
        raise ValueError("n и m не могут быть отрицательными")
    rows = [[_to_int(x) for x in line] for line in lines[1:]]
    # при m = 0 строки матрицы пустые и уже отброшены выше
    if m == 0 and not rows:
        return n, []
    if len(rows) != n or any(len(row) != m for row in rows):
        raise ValueError("размеры матрицы не совпадают с n и m")

    edges = []
    for j in range(m):
        column = [row[j] for row in rows]
        if any(x not in (-1, 0, 1, 2) for x in column):
            raise ValueError(f"недопустимое число в столбце {j}")
        nonzero = [x for x in column if x]
        if sorted(nonzero) == [2]:
            v = column.index(2)
            edges.append((v, v))
        elif sorted(nonzero) == [-1, 1]:
            edges.append((column.index(-1), column.index(1)))
        else:
            raise ValueError(f"столбец {j} не описывает ребро")
    return n, edges


def reachable_from_all(n, edges):
    """Возвращает отсортированный список вершин, достижимых из всех других.

    Из вершины v достижимы все остальные по развёрнутым рёбрам ровно тогда,
    когда v достижима из всех по исходным, поэтому для каждой вершины
    делается обход в ширину по обратному графу.
    """
    reverse = [[] for _ in range(n)]
    for u, v in edges:
        reverse[v].append(u)

    result = []
    for start in range(n):
        seen = {start}
        queue = deque([start])
        while queue:
            for u in reverse[queue.popleft()]:
                if u not in seen:
                    seen.add(u)
                    queue.append(u)
        if len(seen) == n:
            result.append(start)
    return result


def main():
    """Читает граф из файла, указанного в аргументах, и печатает ответ."""
    if len(sys.argv) != 2:
        sys.exit("использование: python reachable.py <файл>")
    try:
        with open(sys.argv[1], encoding="utf-8-sig") as f:
            vertices = reachable_from_all(*parse_graph(f.read()))
    except (OSError, ValueError) as e:
        sys.exit(f"ошибка: {e}")
    if vertices:
        print("Да:", *vertices)
    else:
        print("Нет")


if __name__ == "__main__":
    main()
