import unittest
from unittest.mock import ANY, MagicMock, Mock, patch

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.reply_reaction import ReplyReaction
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.reply import ReplyCreate, ReplyUpdate, ReplyReactionCreate
from forum_system_api.services import reply_service
from forum_system_api.services.user_service import is_admin
from tests.services import test_data_const as tc
from tests.services import test_data_obj as tobj
from tests.services.utils import assert_filter_called_with


class ReplyServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(**tobj.USER_1)
        self.reply = Reply(**tobj.VALID_REPLY)
        self.topic = Topic(**tobj.VALID_TOPIC_1)
        self.category = Category(**tobj.VALID_CATEGORY_1)
        self.reaction = ReplyReaction(**tobj.VALID_REPLY_REACTION_TRUE)

    def test_getById_returnsReply(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.reply

        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            reply = reply_service.get_by_id(self.user, self.reply.id, self.db)

            self.assertEqual(reply, self.reply)

            self.db.query.assert_called_once_with(Reply)
            assert_filter_called_with(query_mock, Reply.id == self.reply.id)

    def test_getById_noReply_returns404(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        with patch(
            "forum_system_api.services.reply_service.verify_topic_permission",
            return_value=None,
        ):
            with self.assertRaises(HTTPException) as context:
                reply_service.get_by_id(self.user, self.reply.id, self.db)

                self.assertEqual(
                    context.exception.status_code, status.HTTP_404_NOT_FOUND
                )
                self.assertEqual(context.exception.detail, "Reply not found")
                self.db.query.assert_called_once_with(Reply)
                assert_filter_called_with(query_mock, Reply.id == self.reply.id)

    def test_getById_invalidTopicPermission_raises403(self):
        with patch(
            "forum_system_api.services.reply_service.verify_topic_permission"
        ) as topic_permission_mock:
            topic_permission_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.get_by_id(self.user, self.reply.id, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Unauthorized")

    def test_create_createsReply(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with (
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            new_reply = reply_service.create(
                self.topic.id, reply_create, self.user, self.db
            )

            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(new_reply)
            self.assertEqual(new_reply.topic_id, self.topic.id)
            self.assertEqual(new_reply.author_id, self.user.id)
            self.assertEqual(new_reply.content, tc.VALID_REPLY_CONTENT)


    def test_createReply_invalidReplyAccess_raises403(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with (
            patch(
                "forum_system_api.services.reply_service._validate_reply_access"
            ) as valdate_reply_mock,
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            valdate_reply_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Topic is locked",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Topic is locked")

    def test_createReply_invalidTopicPermission_raises403(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with (
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission"
            ) as topic_permission_mock,
        ):
            topic_permission_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Unauthorized")

    def test_update_updatesReply_content_authorIsUser(self):
        reply_update = ReplyUpdate(content=tc.VALID_REPLY_CONTENT_2)

        self.reply.author_id = self.user.id

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            updated_reply = reply_service.update(
                self.user, self.reply.id, reply_update, self.db
            )

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(self.reply)
            self.assertEqual(updated_reply.content, self.reply.content)

    def test_update_authorIsNotUser_raises403(self):
        reply_update = ReplyUpdate(content=tc.VALID_REPLY_CONTENT_2)

        self.reply.author_id = tc.VALID_USER_ID_2

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                reply_service.update(self.user, self.reply.id, reply_update, self.db)

                self.assertEqual(
                    context.exception.status_code, status.HTTP_403_FORBIDDEN
                )
                self.assertEqual(context.exception.detail, "Cannot reply to this post")

    def test_update_noContent_noUpdate(self):
        reply_update = ReplyUpdate(content="")

        self.reply.author_id = self.user.id

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            updated_reply = reply_service.update(
                self.user, self.reply.id, reply_update, self.db
            )

            self.assertEqual(updated_reply.content, self.reply.content)
            self.db.commit.assert_not_called()
            self.db.refresh.assert_not_called()

    def test_vote_addsVote_notExists(self):
        reaction = tobj.VALID_REPLY_REACTION_TRUE

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._get_vote_by_id",
                return_value=None,
            ),
            patch(
                "forum_system_api.services.reply_service.create_vote",
                return_value=self.reply,
            ),
        ):
            result = reply_service.vote(self.reply.id, reaction, self.user, self.db)

            self.assertEqual(result, self.reply)

    def test_vote_sameVote_deletesVote(self):
        existing_reaction_mock = Mock()
        existing_reaction_mock.reaction = tc.VALID_REPLY_REACTION_TRUE
        reply_reaction = ReplyReactionCreate(reaction=tc.VALID_REPLY_REACTION_TRUE)
        self.reply.reactions = []

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._get_vote_by_id",
                return_value=existing_reaction_mock,
            ),
        ):
            result = reply_service.vote(
                self.reply.id, reply_reaction, self.user, self.db
            )

            self.assertEqual(result.reactions, self.reply.reactions)
            self.db.delete.assert_called_once_with(existing_reaction_mock)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(result)

    def test_vote_sameVote_updatesVote(self):
        existing_reaction_mock = Mock()
        existing_reaction_mock.reaction = tc.VALID_REPLY_REACTION_FALSE
        reply_reaction = ReplyReactionCreate(reaction=tc.VALID_REPLY_REACTION_TRUE)
        self.reply.reactions = []

        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service._get_vote_by_id",
                return_value=existing_reaction_mock,
            ),
        ):
            result = reply_service.vote(
                self.reply.id, reply_reaction, self.user, self.db
            )

            self.assertEqual(result.reactions, self.reply.reactions)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(result)

    def test_create_vote_createsVote(self):
        reaction_create = ReplyReactionCreate(reaction=tc.VALID_REPLY_REACTION_TRUE)
        self.reply.reactions = [self.reaction]

        result = reply_service.create_vote(
            self.user.id, self.reply, reaction_create, self.db
        )

        added_vote = self.db.add.call_args[0][0]
        self.assertEqual(added_vote.user_id, self.user.id)
        self.assertEqual(added_vote.reply_id, self.reply.id)
        self.assertEqual(added_vote.reaction, tc.VALID_REPLY_REACTION_TRUE)

        self.assertEqual(result, self.reply)
        self.db.add.assert_called_once_with(added_vote)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(result)

    def test_get_vote_by_id_returnsVote_voteExists(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter_by.return_value
        filter_mock.first.return_value = self.reaction

        result = reply_service._get_vote_by_id(self.reply.id, self.user.id, db=self.db)

        self.assertEqual(result, self.reaction)
        self.db.query.assert_called_once_with(ReplyReaction)
        query_mock.filter_by.assert_called_once_with(
            user_id=self.user.id, reply_id=self.reply.id
        )


    def test_get_vote_by_id_returnsNone_notExists(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter_by.return_value
        filter_mock.first.return_value = None
        self.reply.reactions = []

        result = reply_service._get_vote_by_id(self.reply.id, self.user.id, db=self.db)

        self.assertEqual(result, None)
        self.db.query.assert_called_once_with(ReplyReaction)
        query_mock.filter_by.assert_called_once_with(
            user_id=self.user.id, reply_id=self.reply.id
        )
        filter_mock.first.assert_called_once()

    def test_get_votes_returnsUpvotes(self):
        self.reaction.reaction = tc.VALID_REPLY_REACTION_TRUE
        self.reply.reactions = [self.reaction]

        result = reply_service.get_votes(self.reply)

        self.assertEqual(result, (1, 0))

    def test_get_votes_returnsDownvotes(self):
        self.reaction.reaction = tc.VALID_REPLY_REACTION_FALSE
        self.reply.reactions = [self.reaction]

        result = reply_service.get_votes(self.reply)

        self.assertEqual(result, (0, 1))

    def test_get_votes_returnsZero(self):
        self.reply.reactions = []

        result = reply_service.get_votes(self.reply)

        self.assertEqual(result, (0, 0))

    def test_get_votes_returnsMultiple(self):
        reaction1 = ReplyReaction(reaction=tc.VALID_REPLY_REACTION_TRUE)
        reaction2 = ReplyReaction(reaction=tc.VALID_REPLY_REACTION_FALSE)
        self.reply.reactions = [reaction1, reaction2, self.reaction]

        result = reply_service.get_votes(self.reply)

        self.assertEqual(result, (2, 1))

    def test_validate_reply_access_returnsTopic_topicNotLocked(self):
        self.topic.is_locked = tc.VALID_TOPIC_IS_LOCKED_2

        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.is_admin", return_value=False
            ),
        ):
            result = reply_service._validate_reply_access(
                self.topic.id, self.user, self.db
            )

            self.assertEqual(result, self.topic)

    def test_validate_reply_access_raises403_topicLocked_notAdmin(self):
        self.topic.is_locked = tc.VALID_TOPIC_IS_LOCKED_1

        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.is_admin", return_value=False
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                reply_service._validate_reply_access(
                    topic_id=self.topic.id, user=self.user, db=self.db
                )

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

            self.assertEqual(context.exception.detail, "Topic is locked")

    def test_validate_reply_returnsTopic_topicLocked_isAdmin(self):
        self.topic.is_locked = tc.VALID_TOPIC_IS_LOCKED_1

        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.is_admin", return_value=True
            ),
        ):
            result = reply_service._validate_reply_access(
                topic_id=self.topic.id, user=self.user, db=self.db
            )

            self.assertEqual(result, self.topic)
