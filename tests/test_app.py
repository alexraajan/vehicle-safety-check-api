import unittest
from unittest.mock import patch
from app import app


class DummyVehicle:
    def __init__(self, data):
        self.__dict__ = data


class TestVehicleAPIWithMocks(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.test_data = {
            "vehicle_no": "TEST1234",
            "no_of_safety_check": 3,
            "isCompleted": True
        }

    # ---------------------------
    # POST /api/vehicle-details
    # ---------------------------
    @patch('app.vehicle_service.vehicle_details')
    def test_1_post_vehicle_success(self, mock_vehicle_details):
        response = self.client.post('/api/vehicle-details', json=self.test_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())
        mock_vehicle_details.assert_called_once()

    @patch('app.vehicle_service.vehicle_details')
    def test_1_post_vehicle_conflict(self, mock_vehicle_details):
        mock_vehicle_details.side_effect = Exception("Vehicle already exists")
        response = self.client.post('/api/vehicle-details', json=self.test_data)
        self.assertEqual(response.status_code, 409)
        self.assertIn("error", response.get_json())
        mock_vehicle_details.assert_called_once()

    # ---------------------------
    # GET /api/vehicle-details (specific vehicle)
    # ---------------------------
    @patch('app.vehicle_service.get_all_vehicle_details')
    def test_2_get_specific_vehicle_found(self, mock_get_vehicle):
        mock_vehicle = DummyVehicle(self.test_data)
        mock_get_vehicle.return_value = mock_vehicle

        response = self.client.get(f'/api/vehicle-details?vehicle_no={self.test_data["vehicle_no"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["vehicle_no"], self.test_data["vehicle_no"])

    @patch('app.vehicle_service.get_all_vehicle_details')
    def test_2_get_specific_vehicle_not_found(self, mock_get_vehicle):
        mock_get_vehicle.return_value = None
        response = self.client.get(f'/api/vehicle-details?vehicle_no={self.test_data["vehicle_no"]}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    # ---------------------------
    # PUT /api/vehicle-details
    # ---------------------------
    @patch('app.vehicle_service.update_vehicle_details')
    def test_3_update_vehicle_success(self, mock_update):
        mock_update.return_value = True
        response = self.client.put('/api/vehicle-details', json=self.test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    @patch('app.vehicle_service.update_vehicle_details')
    def test_3_update_vehicle_fail(self, mock_update):
        mock_update.return_value = False
        response = self.client.put('/api/vehicle-details', json=self.test_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    # ---------------------------
    # GET /api/vehicle-details (all vehicles)
    # ---------------------------
    @patch('app.vehicle_service.get_all_vehicle_details')
    def test_4_get_all_vehicles_success(self, mock_get_all):
        mock_vehicle = DummyVehicle(self.test_data)
        mock_get_all.return_value = [mock_vehicle]
        response = self.client.get('/api/vehicle-details')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    @patch('app.vehicle_service.get_all_vehicle_details')
    def test_4_get_all_vehicles_empty(self, mock_get_all):
        mock_get_all.return_value = []
        response = self.client.get('/api/vehicle-details')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    # ---------------------------
    # DELETE /api/vehicle-details
    # ---------------------------
    @patch('app.vehicle_service.delete_vehicle')
    def test_5_delete_vehicle_success(self, mock_delete):
        mock_delete.return_value = True
        response = self.client.delete(f'/api/vehicle-details?vehicle_no={self.test_data["vehicle_no"]}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    @patch('app.vehicle_service.delete_vehicle')
    def test_5_delete_vehicle_not_found(self, mock_delete):
        mock_delete.return_value = False
        response = self.client.delete(f'/api/vehicle-details?vehicle_no={self.test_data["vehicle_no"]}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_5_delete_vehicle_missing_param(self):
        response = self.client.delete('/api/vehicle-details')  # Missing vehicle_no
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == '__main__':
    unittest.main()
