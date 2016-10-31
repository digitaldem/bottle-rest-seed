# Standard Library imports
from __future__ import print_function

# Package imports
from inflect import engine
from newrelic.agent import set_transaction_name

# Local imports


def get(offset, limit):
    set_transaction_name('rest.area.entity:get')

    inflection = engine()
    examples = [{'id': x, 'name': inflection.number_to_words(x)} for x in range(1, 51)]

    return examples[offset:offset + limit], len(examples)
