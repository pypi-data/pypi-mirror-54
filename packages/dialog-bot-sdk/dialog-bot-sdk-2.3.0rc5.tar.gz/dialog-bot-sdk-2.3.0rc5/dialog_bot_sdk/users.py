from .service import ManagedService
from dialog_api import contacts_pb2, peers_pb2, users_pb2, messaging_pb2, search_pb2


class Users(ManagedService):
    """Class for handling users

    """

    def get_user_outpeer_by_id(self, uid):
        request = messaging_pb2.RequestLoadDialogs(
            min_date=0,
            limit=1,
            peers_to_load=[peers_pb2.Peer(type=peers_pb2.PEERTYPE_PRIVATE, id=uid)]
        )
        result = self._load_dialogs(request)

        for outpeer in result.user_peers:
            if outpeer.uid == uid:
                return peers_pb2.OutPeer(
                    type=peers_pb2.PEERTYPE_PRIVATE,
                    id=outpeer.uid,
                    access_hash=outpeer.access_hash
                )

    @staticmethod
    def get_user_peer_by_id(uid):
        return peers_pb2.Peer(type=peers_pb2.PEERTYPE_PRIVATE, id=uid)

    def find_user_outpeer_by_nick(self, nick):
        """Returns user's Outpeer object by nickname for direct messaging

        :param nick: user's nickname
        :return: Outpeer object of user
        """
        users = self._search_contacts(
            contacts_pb2.RequestSearchContacts(
                request=nick
            )
        ).users

        for user in users:
            if user.data.nick.value == nick:
                outpeer = peers_pb2.OutPeer(
                    type=peers_pb2.PEERTYPE_PRIVATE,
                    id=int(user.id),
                    access_hash=int(user.access_hash)
                )
                return outpeer
        return None

    def get_user_by_nick(self, nick):
        """Returns User object by nickname

        :param nick: user's nickname
        :return: User object
        """
        users = self._search_contacts(
            contacts_pb2.RequestSearchContacts(
                request=nick
            )
        ).users

        for user in users:
            if user.data.nick.value == nick:
                return user

    def get_user_full_profile_by_nick(self, nick):
        """Returns FullUser object by nickname

        :param nick: user's nickname
        :return: FullUser object
        """
        user = self.find_user_outpeer_by_nick(nick)
        request = users_pb2.RequestLoadFullUsers(
            user_peers=[
                peers_pb2.UserOutPeer(
                    uid=user.id,
                    access_hash=user.access_hash
                )
            ]
        )
        full_profile = self._load_full_users(request)

        if full_profile:
            if hasattr(full_profile, 'full_users'):
                if len(full_profile.full_users) > 0:
                    return full_profile.full_users[0]

    def get_user_custom_profile_by_nick(self, nick):
        """Returns custom_profile field of FullUser object by nickname

        :param nick: user's nickname
        :return: user's custom profile string
        """
        full_profile = self.get_user_full_profile_by_nick(nick)

        if hasattr(full_profile, 'custom_profile'):
            return str(full_profile.custom_profile)

    def get_user_custom_profile_by_peer(self, peer):
        """Returns custom_profile field of FullUser object by Peer object

        :param peer: user's Peer object
        :return: user's custom profile string
        """
        outpeer = self.manager.get_outpeer(peer)

        request = users_pb2.RequestLoadFullUsers(
            user_peers=[
                peers_pb2.UserOutPeer(
                    uid=outpeer.id,
                    access_hash=outpeer.access_hash
                )
            ]
        )
        full_profile = self._load_full_users(request)

        if full_profile:
            if hasattr(full_profile, 'full_users'):
                if len(full_profile.full_users) > 0:
                    if hasattr(full_profile.full_users[0], 'custom_profile'):
                        return str(full_profile.full_users[0].custom_profile)

    def search_users_by_nick_substring(self, query):
        """Returns list of User objects by substring of nickname (not complete coincidence!)

        :param query: user's nickname
        :return: list User objects
        """
        request = search_pb2.RequestPeerSearch(
            query=[
                search_pb2.SearchCondition(
                    searchPeerTypeCondition=search_pb2.SearchPeerTypeCondition(
                        peer_type=search_pb2.SEARCHPEERTYPE_CONTACTS)
                ),
                search_pb2.SearchCondition(
                    searchPieceText=search_pb2.SearchPieceText(query=query)
                )
            ]
        )
        return self._peer_search(request).users

    @staticmethod
    def get_user_outpeer_by_outpeer(outpeer):
        """Return UserOutPeer by OutPeer

        :param outpeer: OutPeer
        :return: UserOutPeer object
        """
        return peers_pb2.UserOutPeer(
            uid=outpeer.id,
            access_hash=outpeer.access_hash
        )

    def _load_dialogs(self, request):
        return self.internal.messaging.LoadDialogs(request)

    def _search_contacts(self, request):
        return self.internal.contacts.SearchContacts(request)

    def _load_full_users(self, request):
        return self.internal.users.LoadFullUsers(request)

    def _peer_search(self, request):
        return self.internal.search.PeerSearch(request)
