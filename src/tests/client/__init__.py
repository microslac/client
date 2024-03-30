from tests.base import TestBase
from tests.factories import AuthFactory, TeamFactory, UserFactory, ChannelFactory


class ClientTestBase(TestBase):
    URL = "/client"

    def setup_team(
        self, auth: AuthFactory = None, return_channels: bool = False, **data
    ):
        auth = auth or AuthFactory()
        team = TeamFactory(creator_id=auth.id, **data)
        user = UserFactory(team_id=team.id, auth_id=auth.id)
        general_channel = ChannelFactory(
            team_id=team.id, creator_id=user.id, is_general=True
        )
        random_channel = ChannelFactory(
            team_id=team.id, creator_id=user.id, is_random=True
        )

        if return_channels:
            return team, user, (general_channel, random_channel)
        return team, user
