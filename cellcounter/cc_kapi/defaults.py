import datetime

from pytz import utc

from .models import Keyboard

BUILTIN_DESKTOP_KEYBOARD_MAP = {
                        "user": None,
                        "label": u"Default desktop",
                        "created": datetime.datetime(2013, 10, 22, 12, 15, 5, 0, tzinfo=utc),
                        "last_modified": datetime.datetime(2013, 10, 22, 12, 15, 13, 0, tzinfo=utc),
                        "device_type": Keyboard.DESKTOP,
                        "mappings": [
                            {"cellid": 1, "key": u"q"},
                            {"cellid": 2, "key": u"w"},
                            {"cellid": 3, "key": u"e"},
                            {"cellid": 4, "key": u"r"},
                            {"cellid": 5, "key": u"t"},
                            {"cellid": 8, "key": u"a"},
                            {"cellid": 9, "key": u"s"},
                            {"cellid": 11, "key": u"d"},
                            {"cellid": 10, "key": u"f"},
                            {"cellid": 13, "key": u"g"},
                            {"cellid": 7, "key": u"z"},
                            {"cellid": 6, "key": u"x"},
                            {"cellid": 12, "key": u"c"}]
}


BUILTIN_MOBILE_KEYBOARD_MAP = {
                        "user": None,
                        "label": u"Default mobile",
                        "created": datetime.datetime(2016, 5, 21, 12, 33, 0, 0, tzinfo=utc),
                        "last_modified": datetime.datetime(2016, 5, 21, 12, 33, 0, 0, tzinfo=utc),
                        "device_type": Keyboard.MOBILE,
                        "mappings": [
                            {"cellid": 1, "key": u"q"},
                            {"cellid": 2, "key": u"w"},
                            {"cellid": 3, "key": u"e"},
                            {"cellid": 4, "key": u"r"},
                            {"cellid": 5, "key": u"t"},
                            {"cellid": 8, "key": u"a"},
                            {"cellid": 9, "key": u"s"},
                            {"cellid": 11, "key": u"d"},
                            {"cellid": 10, "key": u"f"},
                            {"cellid": 13, "key": u"g"},
                            {"cellid": 7, "key": u"z"},
                            {"cellid": 6, "key": u"x"},
                            {"cellid": 12, "key": u"c"}
                        ]
}

BUILTIN_KEYBOARDS = [BUILTIN_DESKTOP_KEYBOARD_MAP, BUILTIN_MOBILE_KEYBOARD_MAP]

MOCK_KEYBOARD = {"mappings": [{"cellid": 1, "key": "q"},
                              {"cellid": 2, "key": "w"},
                              {"cellid": 3, "key": "e"},
                              {"cellid": 4, "key": "r"},
                              {"cellid": 5, "key": "t"},
                              {"cellid": 8, "key": "a"},
                              {"cellid": 9, "key": "s"},
                              {"cellid": 11, "key": "d"},
                              {"cellid": 10, "key": "f"},
                              {"cellid": 13, "key": "g"},
                              {"cellid": 7, "key": "z"},
                              {"cellid": 6, "key": "x"},
                              {"cellid": 12, "key": "c"}],
                 "created": "2013-10-22T12:15:05.118Z",
                 "is_default": True,
                 "label": "Default",
                 "last_modified": "2013-10-22T12:15:13.201Z",
                 "user": None,
                 "device_type": 1}

MOCK_KEYBOARD2 = {"mappings": [{"cellid": 1, "key": "q"},
                              {"cellid": 2, "key": "w"},
                              {"cellid": 3, "key": "e"},
                              {"cellid": 4, "key": "r"},
                              {"cellid": 5, "key": "t"},
                              {"cellid": 8, "key": "a"},
                              {"cellid": 9, "key": "s"},
                              {"cellid": 11, "key": "d"},
                              {"cellid": 10, "key": "f"},
                              {"cellid": 13, "key": "g"},
                              {"cellid": 7, "key": "z"},
                              {"cellid": 6, "key": "x"},
                              {"cellid": 12, "key": "c"}],
                 "created": "2013-10-22T12:15:05.118Z",
                 "label": "Keyboard2",
                 "last_modified": "2013-10-22T12:15:13.201Z",
                 "user": None,
                 "device_type": 1}

BAD_KEYBOARD = {"mappings": [{"cellid": 1, "key": "q"},
                              {"cellid": 2, "key": "w"},
                              {"cellid": 3, "key": "e"},
                              {"cellid": 4, "key": "r"},
                              {"cellid": 5, "key": "t"},
                              {"cellid": 8, "key": "a"},
                              {"cellid": 9, "key": "s"},
                              {"cellid": 11, "key": "d"},
                              {"cellid": 10, "key": "f"},
                              {"cellid": 13, "key": "g"},
                              {"cellid": 7, "key": "z"},
                              {"cellid": 6, "key": "x"},
                              {"cellid": 12, "key": "c"}],
                 "created": "2013-10-22T12:15:05.118Z",
                 "is_default": True,
                 "labelxxx": "Default",
                 "last_modified": "2013-10-22T12:15:13.201Z",
                 "userxxx": None,
                 "device_type": "desktop"}

BUILTIN_DESKTOP_KEYBOARD_STRING = """{"mappings":[{"cellid":1,"key":"q"},{"cellid":2,"key":"w"},{"cellid":3,"key":"e"},{"cellid":4,"key":"r"},{"cellid":5,"key":"t"},{"cellid":8,"key":"a"},{"cellid":9,"key":"s"},{"cellid":11,"key":"d"},{"cellid":10,"key":"f"},{"cellid":13,"key":"g"},{"cellid":7,"key":"z"},{"cellid":6,"key":"x"},{"cellid":12,"key":"c"}],"created":"2013-10-22T12:15:05.118Z","is_default":true,"label":"Default","last_modified":"2013-10-22T12:15:13.201Z","user":null,"device_type":"desktop"}"""

BUILTIN_MOBILE_KEYBOARD_STRING = """{"mappings":[{"cellid":1,"key":"q"},{"cellid":2,"key":"w"},{"cellid":3,"key":"e"},{"cellid":4,"key":"r"},{"cellid":5,"key":"t"},{"cellid":8,"key":"a"},{"cellid":9,"key":"s"},{"cellid":11,"key":"d"},{"cellid":10,"key":"f"},{"cellid":13,"key":"g"},{"cellid":7,"key":"z"},{"cellid":6,"key":"x"},{"cellid":12,"key":"c"}],"created":"2013-10-22T12:15:05.118Z","is_default":true,"label":"Default","last_modified":"2013-10-22T12:15:13.201Z","user":null,"device_type":"mobile"}"""

BUILTIN_KEYBOARD_STRING = """[{"id":1,"user":null,"label":"Default desktop","created":"2013-10-22T12:15:05Z","last_modified":"2013-10-22T12:15:13Z","is_default":true,"device_type":"desktop","href":"/api/keyboards/desktop/builtin/"},{"id":2,"user":null,"label":"Default mobile","created":"2016-05-21T12:33:00Z","last_modified":"2016-05-21T12:33:00Z","is_default":true,"device_type":"mobile","href":"/api/keyboards/mobile/builtin/"}]"""

BUILTIN_KEYBOARD_STRING_LOGGED_IN = """[{"id":1,"user":null,"label":"Default desktop","created":"2013-10-22T12:15:05Z","last_modified":"2013-10-22T12:15:13Z","is_default":true,"device_type":"desktop","href":"/api/keyboards/desktop/builtin/"},{"id":2,"user":null,"label":"Default mobile","created":"2016-05-21T12:33:00Z","last_modified":"2016-05-21T12:33:00Z","is_default":true,"device_type":"mobile","href":"/api/keyboards/mobile/builtin/"}]"""

