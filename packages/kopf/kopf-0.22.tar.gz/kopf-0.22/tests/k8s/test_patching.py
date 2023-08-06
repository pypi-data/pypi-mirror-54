import json

import pykube.exceptions
import pytest
import requests

from kopf.clients.patching import patch_obj


@pytest.mark.resource_clustered  # see `req_mock`
async def test_by_name_clustered(req_mock, resource):
    patch = {'x': 'y'}
    res = await patch_obj(resource=resource, namespace=None, name='name1', patch=patch)
    assert res is None  # never return any k8s-client specific things

    assert req_mock.patch.called
    assert req_mock.patch.call_count == 1

    url = req_mock.patch.call_args_list[0][1]['url']
    assert 'namespaces/' not in url
    assert f'apis/{resource.api_version}/{resource.plural}/name1' in url

    data = json.loads(req_mock.patch.call_args_list[0][1]['data'])
    assert data == {'x': 'y'}


async def test_by_name_namespaced(req_mock, resource):
    patch = {'x': 'y'}
    res = await patch_obj(resource=resource, namespace='ns1', name='name1', patch=patch)
    assert res is None  # never return any k8s-client specific things

    assert req_mock.patch.called
    assert req_mock.patch.call_count == 1

    url = req_mock.patch.call_args_list[0][1]['url']
    assert 'namespaces/' in url
    assert f'apis/{resource.api_version}/namespaces/ns1/{resource.plural}/name1' in url

    data = json.loads(req_mock.patch.call_args_list[0][1]['data'])
    assert data == {'x': 'y'}


@pytest.mark.resource_clustered  # see `req_mock`
async def test_by_body_clustered(req_mock, resource):
    patch = {'x': 'y'}
    body = {'metadata': {'name': 'name1'}}
    res = await patch_obj(resource=resource, body=body, patch=patch)
    assert res is None  # never return any k8s-client specific things

    assert req_mock.patch.called
    assert req_mock.patch.call_count == 1

    url = req_mock.patch.call_args_list[0][1]['url']
    assert 'namespaces/' not in url
    assert f'apis/{resource.api_version}/{resource.plural}/name1' in url

    data = json.loads(req_mock.patch.call_args_list[0][1]['data'])
    assert data == {'x': 'y'}


async def test_by_body_namespaced(req_mock, resource):
    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    res = await patch_obj(resource=resource, body=body, patch=patch)
    assert res is None  # never return any k8s-client specific things

    assert req_mock.patch.called
    assert req_mock.patch.call_count == 1

    url = req_mock.patch.call_args_list[0][1]['url']
    assert 'namespaces/' in url
    assert f'apis/{resource.api_version}/namespaces/ns1/{resource.plural}/name1' in url

    data = json.loads(req_mock.patch.call_args_list[0][1]['data'])
    assert data == {'x': 'y'}


async def test_raises_when_body_conflicts_with_namespace(req_mock, resource):
    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    with pytest.raises(TypeError):
        await patch_obj(resource=resource, body=body, namespace='ns1', patch=patch)

    assert not req_mock.patch.called


async def test_raises_when_body_conflicts_with_name(req_mock, resource):
    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    with pytest.raises(TypeError):
        await patch_obj(resource=resource, body=body, name='name1', patch=patch)

    assert not req_mock.patch.called


async def test_raises_when_body_conflicts_with_ids(req_mock, resource):
    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    with pytest.raises(TypeError):
        await patch_obj(resource=resource, body=body, namespace='ns1', name='name1', patch=patch)

    assert not req_mock.patch.called


@pytest.mark.parametrize('status', [404])
async def test_ignores_absent_objects_with_requests_httperror(req_mock, resource, status):
    response = requests.Response()
    response.status_code = status
    error = requests.exceptions.HTTPError("boo!", response=response)
    req_mock.patch.side_effect = error

    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    await patch_obj(resource=resource, body=body, patch=patch)


@pytest.mark.parametrize('status', [404])
async def test_ignores_absent_objects_with_pykube_httperror(req_mock, resource, status):
    error = pykube.exceptions.HTTPError(status, "boo!")
    req_mock.patch.side_effect = error

    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    await patch_obj(resource=resource, body=body, patch=patch)


@pytest.mark.parametrize('namespace', [None, 'ns1'], ids=['without-namespace', 'with-namespace'])
@pytest.mark.parametrize('status', [400, 401, 403, 500, 666])
async def test_raises_api_errors(req_mock, resource, namespace, status):
    response = requests.Response()
    response.status_code = status
    error = requests.exceptions.HTTPError("boo!", response=response)
    req_mock.patch.side_effect = error

    patch = {'x': 'y'}
    body = {'metadata': {'namespace': 'ns1', 'name': 'name1'}}
    with pytest.raises(requests.exceptions.HTTPError) as e:
        await patch_obj(resource=resource, body=body, patch=patch)
    assert e.value.response.status_code == status
