import pytest
import json
from flask_jwt_extended import create_access_token
from src import create_app
from config import TestConfig

@pytest.fixture(scope='module')
def app():
    _app = create_app(TestConfig)
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app, mocker):
    # Mock JWT token creation
    with app.app_context():
        additional_claims = {"role_id": 2}
        return create_access_token(identity="admin_user", additional_claims=additional_claims)

@pytest.mark.usefixtures("mocker")  # Add this line to use the mocker fixture
def test_get_all_coach_forms(client, admin_token):
    # Mock the get_all_coach_forms service
    mocker.patch(
        'src.routes.admin.get_all_coach_forms',
        return_value=({"message": "Success"}, 200)
    )

    response = client.get(
        '/admin/',
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert b"Success" in response.data

@pytest.mark.usefixtures("mocker")  # Add this line to use the mocker fixture
def test_approve_coach_form(client, admin_token):
    # Mock the update_coach service
    mocker.patch(
        'src.routes.admin.update_coach',
        return_value=({"message": "Coach Approved"}, 200)
    )

    data = {"coach_id": 1, "approved": True}
    response = client.put(
        '/admin/',
        headers={"Authorization": f"Bearer {admin_token}"},
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert b"Coach Approved" in response.data
