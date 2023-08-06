# mypy: allow-untyped-defs, no-check-untyped-defs

import unittest
from datasetmaker.onto.manager import read_concepts
from datasetmaker.utils import ALLOWED_CONCEPT_TYPES


class TestOntology(unittest.TestCase):
    def test_only_allowed_concept_types(self):
        concepts = read_concepts()
        for t in concepts.concept_type:
            self.assertIn(t, ALLOWED_CONCEPT_TYPES)

    def test_no_duplicate_concepts(self):
        concepts = read_concepts()
        self.assertFalse(concepts.concept.duplicated().any())

    def test_all_concepts_have_required_fields(self):
        concepts = read_concepts()
        have_concept = concepts.concept.notnull().all()
        have_concept_type = concepts.concept_type.notnull().all()
        have_name = concepts.name.notnull().all()
        self.assertTrue(all([have_concept, have_concept_type, have_name]))
