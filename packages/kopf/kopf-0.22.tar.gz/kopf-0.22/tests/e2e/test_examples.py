import re
import shlex
import subprocess
import time

import pytest

from kopf.testing import KopfRunner


def test_all_examples_are_runnable(mocker, with_crd, exampledir):

    # If the example has its own opinion on the timing, try to respect it.
    # See e.g. /examples/99-all-at-once/example.py.
    example_py = exampledir / 'example.py'
    m = re.search(r'^E2E_CREATE_TIME\s*=\s*(\d+)$', example_py.read_text(), re.M)
    e2e_create_time = eval(m.group(1)) if m else None
    m = re.search(r'^E2E_DELETE_TIME\s*=\s*(\d+)$', example_py.read_text(), re.M)
    e2e_delete_time = eval(m.group(1)) if m else None
    m = re.search(r'^E2E_TRACEBACKS\s*=\s*(\w+)$', example_py.read_text(), re.M)
    e2e_tracebacks = eval(m.group(1)) if m else None
    # check whether there are mandatory deletion handlers or not
    m = re.search(r'@kopf\.on\.delete\((\s|.*)?(optional=(\w+))?\)', example_py.read_text(), re.M)
    requires_finalizer = False
    if m:
        requires_finalizer = True
        if m.group(2):
            requires_finalizer = not eval(m.group(3))

    # Skip the e2e test if the framework-optional but test-required library is missing.
    m = re.search(r'import kubernetes', example_py.read_text(), re.M)
    if m:
        pytest.importorskip('kubernetes')

    # To prevent lengthy sleeps on the simulated retries.
    mocker.patch('kopf.reactor.handling.DEFAULT_RETRY_DELAY', 1)

    # To prevent lengthy threads in the loop executor when the process exits.
    mocker.patch('kopf.config.WatchersConfig.default_stream_timeout', 10)

    # Run an operator and simulate some activity with the operated resource.
    with KopfRunner(['run', '--standalone', '--verbose', str(example_py)], timeout=60) as runner:
        subprocess.run("kubectl apply -f examples/obj.yaml", shell=True, check=True)
        time.sleep(e2e_create_time or 2)  # give it some time to react and to sleep and to retry
        subprocess.run("kubectl delete -f examples/obj.yaml", shell=True, check=True)
        time.sleep(e2e_delete_time or 1)  # give it some time to react

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    # There are usually more than these messages, but we only check for the certain ones.
    # This just shows us that the operator is doing something, it is alive.
    if requires_finalizer:
        assert '[default/kopf-example-1] Adding the finalizer' in runner.stdout
    assert '[default/kopf-example-1] Creation event:' in runner.stdout
    if requires_finalizer:
        assert '[default/kopf-example-1] Deletion event:' in runner.stdout
    assert '[default/kopf-example-1] Deleted, really deleted' in runner.stdout
    if not e2e_tracebacks:
        assert 'Traceback (most recent call last):' not in runner.stdout
