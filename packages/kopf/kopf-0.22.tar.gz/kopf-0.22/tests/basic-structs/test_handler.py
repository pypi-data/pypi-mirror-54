import pytest

from kopf.reactor.registries import Handler


def test_no_args():
    with pytest.raises(TypeError):
        Handler()


def test_all_args(mocker):
    fn = mocker.Mock()
    id = mocker.Mock()
    event = mocker.Mock()
    field = mocker.Mock()
    timeout = mocker.Mock()
    initial = mocker.Mock()
    labels = mocker.Mock()
    annotations = mocker.Mock()
    handler = Handler(
        fn=fn,
        id=id,
        event=event,
        field=field,
        timeout=timeout,
        initial=initial,
        labels=labels,
        annotations=annotations,
    )
    assert handler.fn is fn
    assert handler.id is id
    assert handler.event is event
    assert handler.field is field
    assert handler.timeout is timeout
    assert handler.initial is initial
    assert handler.labels is labels
    assert handler.annotations is annotations
