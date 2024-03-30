from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.client.models import Team, Auth, User, Channel, ChannelMember
from app.client.schemas import TeamModel, UserModel, ChannelModel
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential_jitter,
    stop_after_attempt,
)


@retry(
    retry=retry_if_exception_type(NoResultFound),
    wait=wait_exponential_jitter(jitter=1, max=20),
    stop=stop_after_attempt(5),
    reraise=True,
)
async def find_teams(db: Session, auth_id: str) -> dict:
    auth = db.query(Auth).where(Auth.id == auth_id).one()
    subquery = select(User.team_id).where(User.auth_id == auth.id)

    curr_teams = db.query(Team).filter(Team.id.in_(subquery)).all()

    open_teams = (
        db.query(Team)
        .filter(Team.is_open.is_(True))
        .filter(Team.id.not_in([t.id for t in curr_teams]))
        .all()
    )

    def build_team_data(team: Team) -> dict:
        active_users = db.query(User).filter(User.team_id == team.id)
        display_users = active_users.limit(5).all()
        team_data = dict(
            id=team.id,
            name=team.name,
            domain=team.domain,
            creator=team.creator_id,
            active_users=active_users.count(),
            profile_photos=["" for _ in display_users],
        )
        return team_data

    current_teams = [build_team_data(team) for team in curr_teams]
    invited_teams = [build_team_data(team) for team in open_teams]

    return dict(
        confirmed_email=auth.email,
        current_teams=current_teams,
        invited_teams=invited_teams,
    )


@retry(
    retry=retry_if_exception_type(NoResultFound),
    wait=wait_exponential_jitter(jitter=1, max=20),
    stop=stop_after_attempt(5),
    reraise=True,
)
async def boot_client(db: Session, auth_id: str, team_id: str, user_id: str) -> dict:
    team = db.query(Team).filter(Team.id == team_id).one()

    users = (
        db.query(User).join(User.profile).filter(User.team_id == team.id).all()
    )  # TODO

    user = (
        db.query(User)
        .join(User.profile)
        .filter(User.id == user_id, User.auth_id == auth_id, User.team_id == team_id)
        .one()
    )

    user_channel_ids = select(ChannelMember.channel_id).where(
        ChannelMember.user_id == user.id
    )

    all_channels = (
        db.query(Channel)
        .filter(Channel.team_id == team.id)
        .filter(Channel.id.in_(user_channel_ids))
    )

    channels = all_channels.filter(Channel.is_channel.is_(True))
    im_channels = all_channels.filter(Channel.is_im.is_(True))

    def dump_im_channel(channel: Channel) -> dict:
        channel_data = ChannelModel.dump(channel)
        other_id = (
            db.query(ChannelMember.user_id)
            .filter(ChannelMember.user_id != user.id)
            .filter(ChannelMember.channel_id == channel.id)
            .one()
        )
        channel_data.update(user=other_id[0])
        return channel_data

    data = dict(
        team=TeamModel.dump(team),
        self=UserModel.dump(user),
        users=UserModel.dump(users, many=True),
        channels=ChannelModel.dump(channels, many=True),
        ims=[dump_im_channel(im_channel) for im_channel in im_channels],
        is_open=[im.id for im in im_channels if not im.is_archived],
        latest_event_ts=0,
        url="ws://test-url",
        prefs={},
    )

    return data
