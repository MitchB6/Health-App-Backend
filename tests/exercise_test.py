from unittest.mock import patch
from flask import Flask
from src.services.client_services import get_all_clients

def test_get_all_clients_success():
    # Create a Flask app and set it as the current app in the context
    app = Flask(__name__)
    app.testing = True
    with app.test_request_context():
        # Mock get_jwt_identity
        with patch('src.services.client_services.get_jwt_identity', return_value=123), \
             patch('src.services.client_services.CoachInfo.query') as mock_coach_query, \
             patch('src.services.client_services.CoachesMembersLink.query') as mock_link_query:

            # Mock the data for the test
            mock_coach_query.return_value.filter_by.return_value.first.return_value = {
                'coach_id': 1,
                'member_id': 123
                # Add other fields as needed
            }

            mock_link_query.return_value.filter_by.return_value.all.return_value = [
                {
                    'client_id': 2,
                    'coach_id': 1,
                    'status': 'approved'
                    # Add other fields as needed
                }
            ]

            # Perform the test
            response, status_code = get_all_clients()

    # Add assertions based on the expected behavior of your function
    assert status_code == 200
    assert response == [
        {
            'client_id': 2,
            'coach_id': 1,
            'status': 'approved'
            # Add other fields as needed
        }
    ]
