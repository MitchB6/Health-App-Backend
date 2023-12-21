from unittest.mock import patch
from src.services.exercise_services import get_equipment

def test_get_equipment_success():
    # Mock the database query
    with patch('src.services.exercise_services.db.session') as mock_session:
        mock_query = mock_session.query.return_value
        mock_query.distinct.return_value.all.return_value = [('Dumbbell',), ('Barbell',)]

        # Mock jsonify to check the output
        with patch('src.services.exercise_services.jsonify', side_effect=lambda x: x) as mock_jsonify:
            response, status_code = get_equipment()

    assert status_code == 200
    assert response == ['Dumbbell', 'Barbell'] 



def test_get_equipment_exception():
    # Mock the database query to simulate an exception
    with patch('src.services.exercise_services.db.session') as mock_session:
        mock_session.query.side_effect = Exception('Simulated datbase error')

        response, status_code = get_equipment()

    assert status_code == 500
    assert response == {"message": "Simulated database error"}
