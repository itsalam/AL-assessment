from tests import BaseTest
import json

class AuthTest(BaseTest):

    def test_auth_point_no_body(self):
        result = self.client.post("/api/token")
        self.assertEqual(result.status_code, 400)

    def get_auth_point(self):
        result = self.get_auth_point()
        self.assert200(result, 200)

    def test_auth_point_bad_body(self):
        result = self.client.post("/api/token", headers={"Content-Type": "application/json"}, data=json.dumps({"junkfield":"testusername"}))
        self.assertEqual(result.status_code, 400)

    def test_auth_req(self):
        result = self.client.get("/api/", headers={"Content-Type": "application/json"})
        self.assert401(result)