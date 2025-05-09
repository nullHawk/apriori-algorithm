from itertools import combinations, chain

def get_support(transactions, itemset):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)

def generate_candidates(prev_frequent, k):
    items = set(chain(*prev_frequent))
    return [frozenset(c) for c in combinations(items, k)]

def filter_frequent(transactions, candidates, min_support):
    itemset_support = {}
    for itemset in candidates:
        support = get_support(transactions, itemset)
        if support >= min_support:
            itemset_support[itemset] = support
    return itemset_support

def apriori(transactions, min_support):
    transactions = list(map(set, transactions))
    all_frequent_itemsets = {}
    k = 1
    current_candidates = [frozenset([item]) for t in transactions for item in t]
    current_candidates = list(set(current_candidates))

    while current_candidates:
        frequent_itemsets = filter_frequent(transactions, current_candidates, min_support)
        if not frequent_itemsets:
            break
        all_frequent_itemsets.update(frequent_itemsets)
        current_candidates = generate_candidates(frequent_itemsets.keys(), k + 1)
        k += 1

    return all_frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) >= 2:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    if consequent and antecedent in frequent_itemsets:
                        support = frequent_itemsets[itemset]
                        confidence = support / frequent_itemsets[antecedent]
                        if confidence >= min_confidence:
                            rules.append((antecedent, consequent, support, confidence))
    return rules
