from unittest import TestCase

import six

from .mocking import mock_instrument, mock_bar, mock_tick
from .fixtures import (
    MagicMock,
    RQAlphaFixture,
    EnvironmentFixture,
    UniverseFixture,
    DataProxyFixture,
    BaseDataSourceFixture,
    BarDictPriceBoardFixture,
    MatcherFixture,
    BookingFixture,
)


class RQAlphaTestCase(TestCase):
    def init_fixture(self):
        pass

    def assertObj(self, obj, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, dict) and not isinstance(getattr(obj, k), dict):
                self.assertObj(getattr(obj, k), **v)
            else:
                self.assertEqual(getattr(obj, k), v)

    def setUp(self):
        self.init_fixture()


__all__ = [
    "MagicMock",
    "RQAlphaFixture",
    "RQAlphaTestCase",
    "EnvironmentFixture",
    "UniverseFixture",
    "DataProxyFixture",
    "BaseDataSourceFixture",
    "BarDictPriceBoardFixture",
    "MatcherFixture",
    "BookingFixture",
    "mock_instrument",
    "mock_bar",
    "mock_tick"
]
