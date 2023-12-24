"""Step decorators.

Example:

@given("I have an article", target_fixture="article")
def _(author):
    return create_test_article(author=author)


@when("I go to the article page")
def _(browser, article):
    browser.visit(urljoin(browser.url, "/articles/{0}/".format(article.id)))


@then("I should not see the error message")
def _(browser):
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".message.error").first


Multiple names for the steps:

@given("I have an article")
@given("there is an article")
def _(author):
    return create_test_article(author=author)


Reusing existing fixtures for a different step name:


@given("I have a beautiful article")
def _(article):
    pass

"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from itertools import count
from typing import Any, Callable, Iterable, Literal, TypeVar

import pytest
from _pytest.fixtures import FixtureDef, FixtureRequest
from typing_extensions import ParamSpec

from .parser import Step
from .parsers import StepParser, get_parser
from .types import GIVEN, THEN, WHEN
from .utils import get_caller_module_locals

P = ParamSpec("P")
T = TypeVar("T")


@enum.unique
class StepNamePrefix(enum.Enum):
    step_def = "pytestbdd_stepdef"
    step_impl = "pytestbdd_stepimpl"


@dataclass
class StepFunctionContext:
    type: Literal["given", "when", "then"] | None
    step_func: Callable[..., Any]
    parser: StepParser
    converters: dict[str, Callable[[str], Any]] = field(default_factory=dict)
    target_fixture: str | None = None


def get_step_fixture_name(step: Step) -> str:
    """Get step fixture name"""
    return f"{StepNamePrefix.step_impl.value}_{step.type}_{step.name}"


def given(
    name: str | StepParser,
    converters: dict[str, Callable[[str], Any]] | None = None,
    target_fixture: str | None = None,
    stacklevel: int = 1,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Given step decorator.
