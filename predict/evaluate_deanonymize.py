#!/usr/bin/env python3

from random import sample
from pickle import load
from argparse import ArgumentParser

import pdb

from bayes_deanonymize import BayesDeanonymize
from classify_relationship import unpickle_length_classifier
from population import PopulationUnpickler

parser = ArgumentParser(description = "Evaluate performance of classification.")
parser.add_argument("population")
parser.add_argument("classifier")
parser.add_argument("--num_node", "-n", type = int, default = 10)
args = parser.parse_args()


print("Loading population.")
with open(args.population, "rb") as pickle_file:
    population = PopulationUnpickler(pickle_file).load()

print("Loading classifier")
classifier = unpickle_length_classifier(args.classifier)

last_generation = population.generations[-1].members

bayes = BayesDeanonymize(population, classifier)

id_mapping = population.id_mapping
labeled_nodes = set(id_mapping[node_id] for node_id
                    in classifier._labeled_nodes)

unlabeled = sample(list(set(last_generation) - labeled_nodes),
                   args.num_node)
# unlabeled = [choice(list(set(last_generation) - labeled_nodes))]
correct = 0
incorrect = 0
print("Attempting to identify {} random nodes.".format(len(unlabeled)))
i = 0
for node in unlabeled:
    print(i)
    identified = bayes.identify(node.genome, node)
    # pdb.set_trace()
    if node in identified:
        correct += 1
        print("correct")
    else:
        print("incorrect")
        incorrect += 1
    i += 1


print("{} correct, {} incorrect, {} total.".format(correct, incorrect,
                                                  len(unlabeled)))
print("{} percent accurate.".format(correct / len(unlabeled)))
