import json
import collections

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from datetime import datetime

from galacteek.core import isoformat
from galacteek.core.jtraverse import traverseParser
from galacteek import log


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PubsubMessage):
            return obj.data
        if isinstance(obj, MarksBroadcastMessage):
            return obj.data
        if isinstance(obj, PeerIdentMessageV1):
            return obj.data
        return json.JSONEncoder.default(self, obj)


class PubsubMessage(collections.UserDict):
    def __init__(self, *args, **kw):
        super(PubsubMessage, self).__init__(*args, **kw)
        self.schema = None

    def __str__(self):
        return json.dumps(self.data)

    def pretty(self):
        return json.dumps(self.data, indent=4)

    @property
    def parser(self):
        return traverseParser(self.data)

    def validSchema(self, schema=None):
        sch = schema if schema else self.__class__.schema

        try:
            validate(self.data, sch)
        except ValidationError as verr:
            log.debug('Invalid JSON schema error: {}'.format(str(verr)))
            return False
        else:
            return True

    def valid(self):
        return self.validSchema()

    @staticmethod
    def make(*args, **kw):
        raise Exception('Implement static method make')


class MarksBroadcastMessage(PubsubMessage):
    TYPE = 'hashmarks.broadcast'

    schema = {
        "title": "Hashmarks broadcast",
        "description": "Hashmarks broadcast message",
        "type": "object",
        "properties": {
            "msgtype": {"type": "string"},
            "msg": {
                "type": "object",
                "properties": {
                    "peerid": {"type": "string"},
                    "ipfsmarks": {
                        "type": "object",
                        "properties": {
                            "categories": {"type": "object"}
                        }
                    }
                },
                "required": ["peerid", "ipfsmarks"]
            },
        },
        "required": ["msgtype", "msg"]
    }

    @staticmethod
    def make(peerid, ipfsmarks):
        msg = MarksBroadcastMessage({
            'msgtype': MarksBroadcastMessage.TYPE,
            'msg': {
                'peerid': peerid,
                'ipfsmarks': ipfsmarks
            }
        })
        return msg

    @property
    def peer(self):
        return self.parser.traverse('msg.peerid')

    @property
    def marks(self):
        return self.parser.traverse('msg.ipfsmarks')


class PeerIdentMessageV1(PubsubMessage):
    TYPE = 'peerident.v1'

    schema = {
        "title": "Peer ident",
        "description": "Peer identification message, V1",
        "type": "object",
        "properties": {
            "msgtype": {"type": "string"},
            "msg": {
                "type": "object",
                "properties": {
                    "peerid": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "publicdag": {
                                "type": "object",
                                "properties": {
                                    "cid": {"type": "string"},
                                    "ipns": {"type": "string"},
                                    "available": {"type": "boolean"}
                                },
                                "required": [
                                    "ipns",
                                    "cid"
                                ],
                            }
                        },
                        "required": [
                            "publicdag"
                        ],
                    },
                    "userinfo": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "firstname": {"type": "string"},
                            "lastname": {"type": "string"},
                            "altname": {"type": "string"},
                            "email": {"type": "string"},
                            "gender": {"type": "integer"},
                            "org": {"type": "string"},
                            "city": {"type": "string"},
                            "country": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "name": {"type": "string"},
                                },
                            },
                            "date": {"type": "object"},
                            "crypto": {
                                "type": "object",
                                "properties": {
                                    "rsa": {
                                        "type": "object",
                                        "properties": {
                                            "pubkeypem": {"type": "string"}
                                        }
                                    }
                                },
                                "required": [
                                    "rsa"
                                ]
                            }
                        },
                        "required": [
                            "username",
                            "firstname",
                            "lastname",
                            "email",
                            "gender",
                            "org",
                            "city",
                            "identtoken",
                            "country"
                        ],
                    },
                },
                "required": ["peerid"]
            },
        },
    }

    @staticmethod
    def make(peerId, uInfoCid, userInfo, userDagCid, userDagIpns, p2pServices):
        msg = PeerIdentMessageV1({
            'msgtype': PeerIdentMessageV1.TYPE,
            'version': 1,
            'msg': {
                'peerid': peerId,
                'user': {
                    'publicdag': {
                        'cid': userDagCid,
                        'available': True,
                        'ipns': userDagIpns if userDagIpns else ''
                    },
                },
                'p2pservices': p2pServices
            }
        })
        msg.data['msg'].update(userInfo)
        return msg

    @property
    def peer(self):
        return self.parser.traverse('msg.peerid')

    @property
    def username(self):
        return self.parser.traverse('msg.userinfo.username')

    @property
    def lastname(self):
        return self.parser.traverse('msg.userinfo.lastname')

    @property
    def country(self):
        return self.parser.traverse('msg.userinfo.country.name')

    @property
    def city(self):
        return self.parser.traverse('msg.userinfo.city')

    @property
    def location(self):
        if self.country != '' and self.city != '':
            return '{city}, {country}'.format(
                city=self.city,
                country=self.country
            )
        elif self.country != '':
            return self.country
        else:
            return 'Unknown'

    @property
    def dateCreated(self):
        return self.parser.traverse('msg.userinfo.date.created')

    @property
    def dagCid(self):
        return self.parser.traverse('msg.user.publicdag.cid')

    @property
    def dagIpns(self):
        return self.parser.traverse('msg.user.publicdag.ipns')

    @property
    def mainPagePath(self):
        return self.parser.traverse('msg.user.mainpage')

    @property
    def userInfoObjCid(self):
        return self.parser.traverse('msg.userinfoobjref')

    @property
    def rsaPubKeyPem(self):
        return self.parser.traverse('msg.userinfo.crypto.rsa.pubkeypem')

    @property
    def msgdata(self):
        return self.data['msg']

    def valid(self):
        return self.validSchema(schema=PeerIdentMessageV1.schema)


class PeerIdentMessageV2(PubsubMessage):
    TYPE = 'peerident.v2'

    schema = {
        "title": "Peer ident",
        "description": "Peer identification message, V2",
        "type": "object",
        "properties": {
            "msgtype": {"type": "string"},
            "msg": {
                "type": "object",
                "properties": {
                    "peerid": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "publicdag": {
                                "type": "object",
                                "properties": {
                                    "cid": {"type": "string"},
                                    "ipns": {"type": "string"},
                                    "available": {"type": "boolean"}
                                },
                                "required": [
                                    "ipns",
                                    "cid"
                                ],
                            }
                        },
                        "required": [
                            "publicdag"
                        ],
                    },
                    "userinfo": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "firstname": {"type": "string"},
                            "lastname": {"type": "string"},
                            "altname": {"type": "string"},
                            "email": {"type": "string"},
                            "gender": {"type": "integer"},
                            "org": {"type": "string"},
                            "city": {"type": "string"},
                            "country": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "name": {"type": "string"},
                                },
                            },
                            "date": {"type": "object"},
                            "crypto": {
                                "type": "object",
                                "properties": {
                                    "rsa": {
                                        "type": "object",
                                        "properties": {
                                            "pubkeypem": {"type": "string"}
                                        }
                                    }
                                },
                                "required": [
                                    "rsa"
                                ]
                            }
                        },
                        "required": [
                            "username",
                            "firstname",
                            "lastname",
                            "email",
                            "gender",
                            "org",
                            "city",
                            "identtoken",
                            "country"
                        ],
                    },
                },
                "required": ["peerid"]
            },
        },
    }

    @staticmethod
    def make(peerId, uInfoCid, userInfo, userDagCid, userDagIpns, p2pServices,
             orbitCfgMaps):
        msg = PeerIdentMessageV2({
            'msgtype': PeerIdentMessageV2.TYPE,
            'version': 2,
            'msg': {
                'peerid': peerId,
                'user': {
                    'publicdag': {
                        'cid': userDagCid,
                        'available': True,
                        'ipns': userDagIpns if userDagIpns else ''
                    },
                },
                'orbitcfgmaps': orbitCfgMaps,
                'p2pservices': p2pServices
            }
        })
        msg.data['msg'].update(userInfo)
        return msg

    @property
    def peer(self):
        return self.parser.traverse('msg.peerid')

    @property
    def username(self):
        return self.parser.traverse('msg.userinfo.username')

    @property
    def lastname(self):
        return self.parser.traverse('msg.userinfo.lastname')

    @property
    def country(self):
        return self.parser.traverse('msg.userinfo.country.name')

    @property
    def city(self):
        return self.parser.traverse('msg.userinfo.city')

    @property
    def location(self):
        if self.country != '' and self.city != '':
            return '{city}, {country}'.format(
                city=self.city,
                country=self.country
            )
        elif self.country != '':
            return self.country
        else:
            return 'Unknown'

    @property
    def dateCreated(self):
        return self.parser.traverse('msg.userinfo.date.created')

    @property
    def dagCid(self):
        return self.parser.traverse('msg.user.publicdag.cid')

    @property
    def dagIpns(self):
        return self.parser.traverse('msg.user.publicdag.ipns')

    @property
    def mainPagePath(self):
        return self.parser.traverse('msg.user.mainpage')

    @property
    def userInfoObjCid(self):
        return self.parser.traverse('msg.userinfoobjref')

    @property
    def rsaPubKeyPem(self):
        return self.parser.traverse('msg.userinfo.crypto.rsa.pubkeypem')

    @property
    def msgdata(self):
        return self.data['msg']

    def valid(self):
        return self.validSchema(schema=PeerIdentMessageV1.schema)


class PeerLogoutMessage(PubsubMessage):
    TYPE = 'peerlogout'

    schema = {
        "type": "object",
        "properties": {
            "msgtype": {"type": "string"},
            "msg": {
                "type": "object",
                "properties": {
                    "peerid": {"type": "string"},
                },
                "required": ["peerid"]
            },
        },
    }

    @staticmethod
    def make(peerid):
        msg = PeerLogoutMessage({
            'msgtype': PeerLogoutMessage.TYPE,
            'msg': {
                'peerid': peerid,
            }
        })
        return msg

    @property
    def peer(self):
        return self.parser.traverse('msg.peerid')

    def valid(self):
        return self.validSchema(schema=PeerLogoutMessage.schema)


class ChatRoomMessage(PubsubMessage):
    TYPE = 'chatroommessage'

    CHANNEL_GENERAL = 'general'

    schema = {
        "type": "object",
        "properties": {
            "msgtype": {"type": "string"},
            "msg": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "message": {"type": "string"},
                    "channel": {"type": "string"},
                    "sender": {"type": "string"},
                    "level": {"type": "integer"},
                    "links": {"type": "array"},
                    "attachments": {"type": "array"}
                },
                "required": [
                    "message",
                    "date",
                    "sender",
                    "level",
                    "links",
                    "attachments",
                    "channel"
                ]
            },
        },
    }

    @staticmethod
    def make(sender, channel, message, links=[], attachments=[], date=None,
             level=0):
        msgDate = date if date else isoformat(datetime.now(),
                                              timespec='minutes')
        msg = ChatRoomMessage({
            'msgtype': ChatRoomMessage.TYPE,
            'version': 1,
            'msg': {
                'date': msgDate,
                'sender': sender,
                'channel': channel,
                'message': message,
                'links': links,
                'attachments': attachments,
                'level': level
            }
        })
        return msg

    @property
    def message(self):
        return self.parser.traverse('msg.message')

    @property
    def sender(self):
        return self.parser.traverse('msg.sender')

    @property
    def channel(self):
        return self.parser.traverse('msg.channel')

    @property
    def date(self):
        return self.parser.traverse('msg.date')

    @property
    def level(self):
        return self.parser.traverse('msg.level')

    @property
    def links(self):
        return self.data['msg']['links']

    def valid(self):
        schemaOk = self.validSchema(schema=ChatRoomMessage.schema)
        if schemaOk:
            return len(self.message) < 1024
