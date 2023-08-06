import inspect
from contextlib import suppress
from functools import partial, wraps
from typing import Callable, Dict, Iterable

from ward.models import WardMeta


class TestSetupError(Exception):
    pass


class CollectionError(TestSetupError):
    pass


class FixtureExecutionError(Exception):
    pass


class Fixture:
    def __init__(self, key: str, fn: Callable):
        self.key = key
        self.fn = fn
        self.gen = None
        self.resolved_val = None

    def deps(self):
        return inspect.signature(self.fn).parameters

    @property
    def is_generator_fixture(self):
        return inspect.isgeneratorfunction(inspect.unwrap(self.fn))

    def resolve(self, fix_cache) -> "Fixture":
        """Traverse the fixture tree to resolve the value of this fixture"""

        # If this fixture has no children, cache and return the resolved value
        if not self.deps():
            try:
                if self.is_generator_fixture:
                    self.gen = self.fn()
                    self.resolved_val = next(self.gen)
                else:
                    self.resolved_val = self.fn()
            except Exception as e:
                raise FixtureExecutionError(
                    f"Unable to execute fixture '{self.key}'"
                ) from e
            fix_cache.cache_fixture(self)
            return self

        # Otherwise, we have to find the child fixture vals, and call self
        children = self.deps()
        children_resolved = []
        for child in children:
            child_fixture = fix_cache[child].resolve(fix_cache)
            children_resolved.append(child_fixture)

        # We've resolved the values of all child fixtures
        try:
            child_resolved_vals = [child.resolved_val for child in children_resolved]
            if self.is_generator_fixture:
                self.gen = self.fn(*child_resolved_vals)
                self.resolved_val = next(self.gen)
            else:
                self.resolved_val = self.fn(*child_resolved_vals)
        except Exception as e:
            raise FixtureExecutionError(
                f"Unable to execute fixture '{self.key}'"
            ) from e

        fix_cache.cache_fixture(self)
        return self

    def teardown(self):
        if self.is_generator_fixture:
            next(self.gen)


class FixtureCache:
    def __init__(self):
        self._fixtures: Dict[str, Fixture] = {}

    def _get_fixture(self, fixture_name: str) -> Fixture:
        try:
            return self._fixtures[fixture_name]
        except KeyError:
            raise CollectionError(f"Couldn't find fixture '{fixture_name}'.")

    def cache_fixture(self, fixture: Fixture):
        """Update the fixture in the cache, for example, replace it with its resolved analogue"""
        # TODO: Caching can be used to implement fixture scoping,
        #  but currently resolved cached fixtures aren't used.
        self._fixtures[fixture.key] = fixture

    def cache_fixtures(self, fixtures: Iterable[Fixture]):
        for fixture in fixtures:
            self.cache_fixture(fixture)

    def teardown_all(self):
        """Run the teardown code for all generator fixtures in the cache"""
        for fixture in self._fixtures.values():
            with suppress(RuntimeError, StopIteration):
                fixture.teardown()

    def __contains__(self, key: str):
        return key in self._fixtures

    def __getitem__(self, item):
        return self._fixtures[item]

    def __len__(self):
        return len(self._fixtures)


fixture_cache = FixtureCache()


def fixture(func=None, *, description=None):
    if func is None:
        return partial(fixture, description=description)

    # By setting is_fixture = True, the framework will know
    # that if this fixture is provided as a default arg, it
    # is responsible for resolving the value.
    if hasattr(func, "ward_meta"):
        func.ward_meta.is_fixture = True
    else:
        func.ward_meta = WardMeta(is_fixture=True)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_cache_key_for_func(fixture: Callable):
    path = inspect.getfile(fixture)
    name = fixture.__name__
    return f"{path}::{name}"
