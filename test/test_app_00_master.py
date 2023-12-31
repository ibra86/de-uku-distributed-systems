import pytest
from fastapi.testclient import TestClient

from app_00_master import app
from app_00_master import messages


@pytest.fixture
def client():
    yield TestClient(app)


def test_add_message(mocker, client):
    mocker.patch('service.MessageService.send_message', autospec=True, return_value='msg_sent')

    response = client.post(
        '/',
        json={'name': 'msg'}
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'msg'
    assert response.json()['timestamp']
    assert dict(messages[0])['name'] == 'msg'
