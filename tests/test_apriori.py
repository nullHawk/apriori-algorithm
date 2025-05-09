import unittest
from apriori_algorithm import apriori, generate_rules

class TestAprioriAlgorithm(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            ['milk', 'bread', 'nuts', 'apple'],
            ['milk', 'bread', 'nuts'],
            ['milk', 'bread'],
            ['milk', 'apple'],
            ['bread', 'apple']
        ]
        self.min_support = 0.6
        self.min_confidence = 0.7

    def test_frequent_itemsets(self):
        expected = {
            frozenset({'milk'}): 0.8,
            frozenset({'bread'}): 0.8,
            frozenset({'apple'}): 0.6,
            frozenset({'milk', 'bread'}): 0.6
        }
        result = apriori(self.transactions, self.min_support)
        for itemset in expected:
            self.assertAlmostEqual(result.get(itemset, 0), expected[itemset], places=2)

    def test_generate_rules(self):
        frequent_itemsets = apriori(self.transactions, self.min_support)
        rules = generate_rules(frequent_itemsets, self.min_confidence)
        rule_strs = [f"{set(a)} => {set(c)}" for a, c, _, _ in rules]

        self.assertIn("{'bread'} => {'milk'}", rule_strs)
        self.assertIn("{'milk'} => {'bread'}", rule_strs)
        self.assertTrue(all(conf >= self.min_confidence for *_, conf in rules))

if __name__ == '__main__':
    unittest.main()
