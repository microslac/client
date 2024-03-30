import random
from tests.client import ClientTestBase
from tests.factories import AuthFactory


class TestFindTeams(ClientTestBase):
    def test_find_teams_success(self):
        auth = AuthFactory(id="A0123456789")
        n, m = random.randint(1, 9), random.randint(1, 9)
        current_teams, _ = list(zip(*[self.setup_team(auth) for _ in range(n)]))
        invited_teams, _ = list(zip(*[self.setup_team(is_open=True) for _ in range(m)]))
        other_teams, _ = list(zip(*[self.setup_team(is_open=False) for _ in range(2)]))

        data = dict(auth=auth.id)
        response = self.client.post(f"{self.URL}/find-teams", json=data)

        assert response.status_code == 200

        resp = self.objectify(response.json())
        assert len(resp.invited_teams) == len(invited_teams)
        assert len(resp.current_teams) == len(current_teams)
