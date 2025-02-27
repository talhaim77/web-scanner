import pytest
from builder import ResultBuilder
from models import ScanResult


def test_builder_add_data_merges_list_fields():
    builder = ResultBuilder("example.com")
    # Add first set of data
    builder.add_data({"related_ips": ["1.1.1.1", "2.2.2.2"], "technologies": ["TechA"]})
    # Add second set with overlapping and new values
    builder.add_data({"related_ips": ["2.2.2.2", "3.3.3.3"], "technologies": ["TechB"]})

    result: ScanResult = builder.build()
    # Verify that the related_ips list contains unique values
    assert set(result.related_ips) == {"1.1.1.1", "2.2.2.2", "3.3.3.3"}
    assert set(result.technologies) == {"TechA", "TechB"}
    assert result.domain == "example.com"
