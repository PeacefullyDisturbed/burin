"""
Burin Filter Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# PyTest imports
import pytest

# Burin import
import burin


# Basic testing values
testLevel = burin.INFO
testLineNumber = 10
testMessage = "This is a log message"
testPathname = "/test/path"

# Names for the test log records to create the hierarchy
childName = "A.B"
grandchildName = "A.B.C"
parentName = "A"
siblingName = "A.BB"
similarName = "AA"

@pytest.fixture
def parent_record():
    """
    Creates a log record that would by at the top of a hierarchy.
    """

    return burin.BurinLogRecord(parentName, testLevel, testPathname,
                                testLineNumber, testMessage, (), None)

@pytest.fixture
def child_record():
    """
    Creates a log record that is a child of a parent in the hierarchy.
    """

    return burin.BurinLogRecord(childName, testLevel, testPathname,
                                testLineNumber, testMessage, (), None)

@pytest.fixture
def grandchild_record():
    """
    Creates a log record that is a grandchild of a parent in the hierarchy.
    """

    return burin.BurinLogRecord(grandchildName, testLevel, testPathname,
                                testLineNumber, testMessage, (), None)

@pytest.fixture
def sibling_record():
    """
    Creates a log record that is a sibling of a child in the hierarchy.
    """

    return burin.BurinLogRecord(siblingName, testLevel, testPathname,
                                testLineNumber, testMessage, (), None)

@pytest.fixture
def similar_record():
    """
    Creates a log record that is a similar to the parent in the hierarchy.
    """

    return burin.BurinLogRecord(similarName, testLevel, testPathname,
                                testLineNumber, testMessage, (), None)

@pytest.fixture
def empty_filter():
    """
    Creates a filter that allows all records.
    """

    return burin.BurinFilter()

@pytest.fixture
def parent_filter():
    """
    Creates a filter that only allows a parent and lower hierarchical records.
    """

    return burin.BurinFilter(parentName)

@pytest.fixture
def child_filter():
    """
    Creates a filter that only allows a child and lower hierarchical records.
    """

    return burin.BurinFilter(childName)


class TestFilter:
    """
    Tests the default filter class.
    """

    def test_empty_filter(self, empty_filter, parent_record, child_record,
                          grandchild_record, sibling_record, similar_record):
        """
        Tests that an empty filter string allows any log record.
        """

        assert empty_filter.filter(parent_record) is True
        assert empty_filter.filter(child_record) is True
        assert empty_filter.filter(grandchild_record) is True
        assert empty_filter.filter(sibling_record) is True
        assert empty_filter.filter(similar_record) is True

    def test_parent_filter(self, parent_filter, parent_record, child_record,
                           grandchild_record, sibling_record, similar_record):
        """
        Tests filtering records at the parent level.
        """

        assert parent_filter.filter(parent_record) is True
        assert parent_filter.filter(child_record) is True
        assert parent_filter.filter(grandchild_record) is True
        assert parent_filter.filter(sibling_record) is True
        assert parent_filter.filter(similar_record) is False

    def test_child_filter(self, child_filter, parent_record, child_record,
                          grandchild_record, sibling_record, similar_record):
        """
        Tests filtering records at the child level.
        """

        assert child_filter.filter(parent_record) is False
        assert child_filter.filter(child_record) is True
        assert child_filter.filter(grandchild_record) is True
        assert child_filter.filter(sibling_record) is False
        assert child_filter.filter(similar_record) is False


@pytest.fixture
def basic_filterer():
    """
    Creates a basic filterer instance.
    """

    return burin.BurinFilterer()


class LineIncrementFilter(burin.BurinFilter):
    """
    Returns a new record instance with an incremented line number.

    This is purely for testing modification filters within a filterer.
    """

    def filter(self, record):
        """
        Creates a new record instance with an incremented line number.

        :param record: The record to alter.
        :type record: BurinLogRecord
        :returns: A new record instance with an incremented line number.
        :rtype: BurinLogRecord
        """

        return burin.BurinLogRecord(record.name, record.levelno, record.pathname, record.lineno + 1,
                                    record.msg, record.args,record.exc_info, record.funcName,
                                    record.stack_info, **record.kwargs)


class TestFilterer:
    """
    Tests the filterer base class used for loggers and handlers.
    """

    def test_add_filter(self, basic_filterer, empty_filter, parent_filter,
                        child_filter):
        """
        Tests adding multiple filters.
        """

        testFilters = [empty_filter, parent_filter, child_filter]

        for eachFilter in testFilters:
            basic_filterer.add_filter(eachFilter)

        assert len(basic_filterer.filters) == len(testFilters)

        for i in range(len(testFilters)):
            assert basic_filterer.filters[i] is testFilters[i]

    def test_readd_filter(self, basic_filterer, empty_filter):
        """
        Tests that re-adding the same filter doesn't duplicate it in the list.
        """

        basic_filterer.add_filter(empty_filter)
        basic_filterer.add_filter(empty_filter)

        assert len(basic_filterer.filters) == 1
        assert basic_filterer.filters[0] is empty_filter

    def test_remove_filter(self, basic_filterer, empty_filter, parent_filter,
                           child_filter):
        """
        Tests removing a filter.
        """

        testFilters = [empty_filter, parent_filter, child_filter]

        for eachFilter in testFilters:
            basic_filterer.add_filter(eachFilter)

        assert len(basic_filterer.filters) == len(testFilters)

        basic_filterer.remove_filter(parent_filter)

        assert len(basic_filterer.filters) == (len(testFilters) - 1)
        assert parent_filter not in basic_filterer.filters

    def test_remove_non_present_filter(self, basic_filterer, empty_filter,
                                       parent_filter):
        """
        Tests removing a filter not in filter list doesn't impact the list.
        """

        basic_filterer.add_filter(empty_filter)
        basic_filterer.remove_filter(parent_filter)

        assert len(basic_filterer.filters) == 1
        assert basic_filterer.filters[0] is empty_filter

    def test_single_filter_checks(self, basic_filterer, parent_filter,
                                  parent_record, child_record,
                                  grandchild_record, sibling_record,
                                  similar_record):
        """
        Tests a single filter check with different records.
        """

        basic_filterer.add_filter(parent_filter)

        assert basic_filterer.filter(parent_record) is parent_record
        assert basic_filterer.filter(child_record) is child_record
        assert basic_filterer.filter(grandchild_record) is grandchild_record
        assert basic_filterer.filter(sibling_record) is sibling_record
        assert basic_filterer.filter(similar_record) is False

    def test_multi_filter_checks(self, basic_filterer, parent_filter,
                                 child_filter, parent_record, child_record,
                                 grandchild_record, sibling_record,
                                 similar_record):
        """
        Tests multiple filter checks with different records.
        """

        basic_filterer.add_filter(parent_filter)
        basic_filterer.add_filter(child_filter)

        assert basic_filterer.filter(parent_record) is False
        assert basic_filterer.filter(child_record) is child_record
        assert basic_filterer.filter(grandchild_record) is grandchild_record
        assert basic_filterer.filter(sibling_record) is False
        assert basic_filterer.filter(similar_record) is False

    def test_modifying_filters(self, basic_filterer, parent_record):
        """
        Tests that modified records are returned through the filter process.
        """

        # Use two filters to ensure the record is progressively modified.
        basic_filterer.add_filter(LineIncrementFilter())
        basic_filterer.add_filter(LineIncrementFilter())

        alteredRecord = basic_filterer.filter(parent_record)

        assert alteredRecord is not parent_record
        assert alteredRecord.lineno == (parent_record.lineno + 2)
