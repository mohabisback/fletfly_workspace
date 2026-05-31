# test_subway.py
import pytest
from fletfly import Airway, subway

def dummy_build(page):
    pass

# --- Class Decoration Cases ---

def test_01():
    """ @subway on class without parenthesis. """
    @subway
    class SampleSubway:
        build = dummy_build

    # Should behave as a full route container
    assert hasattr(SampleSubway, "build")


def test_02():
    """ @subway() on class with empty parenthesis. """
    @subway()
    class SampleSubway:
        build = dummy_build

    assert hasattr(SampleSubway, "build")


def test_03():
    """ @subway("/route") with explicit positional path string. """
    @subway("/dashboard")
    class DashboardSubway:
        build = dummy_build

    # Verify path and its clsattr are successfully injected into the target class
    assert getattr(DashboardSubway, "path", None) == "/dashboard"
    assert getattr(DashboardSubway, "path_clsattr", None) == "path"


def test_04():
    """ @subway(path="/route") with explicit keyword path string. """
    @subway(path="/analytics")
    class AnalyticsSubway:
        build = dummy_build

    assert getattr(AnalyticsSubway, "path", None) == "/analytics"
    assert getattr(AnalyticsSubway, "path_clsattr", None) == "path"


def test_05():
    """ Verify path is not deleted from config and is preserved for runtime recording. """
    @subway("/settings")
    class SettingsSubway:
        build = dummy_build

    # Ensure config retention for attr name rechecking in runtime loop
    assert hasattr(SettingsSubway, "path")
    assert SettingsSubway.path == "/settings"
    assert hasattr(SettingsSubway, "path_clsattr")
    assert SettingsSubway.path_clsattr == "path"


def test_06():
    """ Ensure no '_fletfly_subway' flag is explicitly set or required. """
    @subway("/profile")
    class ProfileSubway:
        build = dummy_build

    # As intended, subways are full routes processed via tree, no special flag needed
    assert getattr(ProfileSubway, "_fletfly_subway", None) is None