import asyncio
import logging

import pytest

import kopf
from kopf.reactor.causation import ALL_CAUSES, HANDLER_CAUSES
from kopf.reactor.handling import custom_object_handler


@pytest.mark.parametrize('cause_type', ALL_CAUSES)
async def test_all_logs_are_prefixed(registry, resource, handlers,
                                     logstream, cause_type, cause_mock):
    cause_mock.event = cause_type

    await custom_object_handler(
        lifecycle=kopf.lifecycles.all_at_once,
        registry=registry,
        resource=resource,
        event={'type': 'irrelevant', 'object': cause_mock.body},
        freeze=asyncio.Event(),
        replenished=asyncio.Event(),
        event_queue=asyncio.Queue(),
    )

    lines = logstream.getvalue().splitlines()
    assert lines  # no messages means that we cannot test it
    assert all(line.startswith('prefix [ns1/name1] ') for line in lines)


@pytest.mark.parametrize('diff', [
    pytest.param((('op', ('field',), 'old', 'new'),), id='realistic-diff'),
    pytest.param((), id='empty-tuple-diff'),
    pytest.param([], id='empty-list-diff'),
])
@pytest.mark.parametrize('cause_type', HANDLER_CAUSES)
async def test_diffs_logged_if_present(registry, resource, handlers, cause_type, cause_mock,
                                       caplog, assert_logs, diff):
    caplog.set_level(logging.DEBUG)
    cause_mock.event = cause_type
    cause_mock.diff = diff
    cause_mock.new = object()  # checked for `not None`
    cause_mock.old = object()  # checked for `not None`

    await custom_object_handler(
        lifecycle=kopf.lifecycles.all_at_once,
        registry=registry,
        resource=resource,
        event={'type': 'irrelevant', 'object': cause_mock.body},
        freeze=asyncio.Event(),
        replenished=asyncio.Event(),
        event_queue=asyncio.Queue(),
    )
    assert_logs([
        " event: ",
        " diff: "
    ])


@pytest.mark.parametrize('cause_type', HANDLER_CAUSES)
async def test_diffs_not_logged_if_absent(registry, resource, handlers, cause_type, cause_mock,
                                          caplog, assert_logs):
    caplog.set_level(logging.DEBUG)
    cause_mock.event = cause_type
    cause_mock.diff = None  # same as the default, but for clarity

    await custom_object_handler(
        lifecycle=kopf.lifecycles.all_at_once,
        registry=registry,
        resource=resource,
        event={'type': 'irrelevant', 'object': cause_mock.body},
        freeze=asyncio.Event(),
        replenished=asyncio.Event(),
        event_queue=asyncio.Queue(),
    )
    assert_logs([
        " event: ",
    ], prohibited=[
        " diff: "
    ])
