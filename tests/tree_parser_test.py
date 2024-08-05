import unittest

# Need to add the .. folder to PATH to access a module via tests folder
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(sprint_1_directory)

from wdc.helpers.subset import Subset
from wdc.tree.tree_parser import make_process_query_from_tree
from wdc import Datacube


class TestQueryTreeParser(unittest.TestCase):
    def test_small_query(self):
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = (a + b).encode("image/png")
        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f2 := ${b.name}[ $index{b.name}],
        $f1 := ${a.name}[ $index{a.name}],
        $f0 := ($f1)+($f2)
    return encode($f0, \"image/png\")"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_query_integers(self):
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = ((a + b) + 15).encode("image/png")
        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f4 := 15,
        $f3 := ${b.name}[ $index{b.name}],
        $f2 := ${a.name}[ $index{a.name}],
        $f1 := ($f2)+($f3),
        $f0 := ($f1)+($f4)
    return encode($f0, "image/png")"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_avg(self):
        self.maxDiff = None
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = ((a + b) + 15).avg().encode("image/png")

        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f5 := 15,
        $f4 := ${b.name}[ $index{b.name}],
        $f3 := ${a.name}[ $index{a.name}],
        $f2 := ($f3)+($f4),
        $f1 := ($f2)+($f5),
        $f0 := avg(($f1))
    return encode($f0, "image/png")"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_min(self):
        self.maxDiff = None
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = ((a + b) + 15).min().encode("image/png")

        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f5 := 15,
        $f4 := ${b.name}[ $index{b.name}],
        $f3 := ${a.name}[ $index{a.name}],
        $f2 := ($f3)+($f4),
        $f1 := ($f2)+($f5),
        $f0 := min(($f1))
    return encode($f0, "image/png")"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_max(self):
        self.maxDiff = None
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = ((a + b) + 15).max([Subset("ansi", "2021-04-09")]).encode("image/png")

        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f5 := 15,
        $f4 := ${b.name}[ $index{b.name}],
        $f3 := ${a.name}[ $index{a.name}],
        $f2 := ($f3)+($f4),
        $f1 := ($f2)+($f5),
        $f0 := max(($f1)[ansi("2021-04-09")])
    return encode($f0, "image/png")"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_refactor(self):
        self.maxDiff = None
        a = Datacube(
            index='ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 )'
        )
        b = Datacube(
            index='ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 )'
        )
        c = Datacube.refactor(
            [("myfirstAxis", a + b), ("mySecondAxis", a - b), ("myThirdAxis", a / b)]
        )
        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    ${b.name} in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $f9 := ${b.name}[ $index{b.name}],
        $f8 := ${a.name}[ $index{a.name}],
        $f7 := ($f8)/($f9),
        $f6 := ${b.name}[ $index{b.name}],
        $f5 := ${a.name}[ $index{a.name}],
        $f4 := ($f5)-($f6),
        $f3 := ${b.name}[ $index{b.name}],
        $f2 := ${a.name}[ $index{a.name}],
        $f1 := ($f2)+($f3),
        $f0 := {{ myfirstAxis: $f1; mySecondAxis: $f4; myThirdAxis: $f7 }}
    return $f0"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))

    def test_subindex(self):
        self.maxDiff = None
        a = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        b = Datacube(
            index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ]
        )
        c = Datacube.refactor(
            [
                ("myfirstAxis", (a + b)[[Subset("ansi", "2021-04-09")]]),
                ("mySecondAxis", (a - b)[[Subset("ansi", "2021-04-09")]]),
                ("myThirdAxis", (a / b)[[Subset("ansi", "2021-04-09")]]),
            ]
        )
        query = f"""for ${a.name} in (S2_L2A_32631_TCI_60m),
    $c38 in (S2_L2A_32631_TCI_60m)
    let $index{a.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $index{b.name} := [ansi("2021-04-09"), E(670000:679000), N(4990220:4993220)],
        $indexf1 := [ansi("2021-04-09")],
        $indexf5 := [ansi("2021-04-09")],
        $indexf9 := [ansi("2021-04-09")],
        $f12 := ${b.name}[ $indexc38],
        $f11 := ${a.name}[ $indexc37],
        $f10 := ($f11)/($f12),
        $f9 := $f10[ $indexf9],
        $f8 := ${b.name}[ $indexc38],
        $f7 := ${a.name}[ $indexc37],
        $f6 := ($f7)-($f8),
        $f5 := $f6[ $indexf5],
        $f4 := ${b.name}[ $indexc38],
        $f3 := ${a.name}[ $indexc37],
        $f2 := ($f3)+($f4),
        $f1 := $f2[ $indexf1],
        $f0 := {{ myfirstAxis: $f1; mySecondAxis: $f5; myThirdAxis: $f9 }}
    return $f0"""
        self.assertEqual(query, make_process_query_from_tree(c.get_tree()))


if __name__ == "__main__":
    unittest.main()
