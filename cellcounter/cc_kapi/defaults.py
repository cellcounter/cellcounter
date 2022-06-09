import datetime

from pytz import utc

DEFAULT_KEYBOARD_MAP = {
                        "user": None,
                        "label": u"Default",
                        "is_primary": True,
                        "created": datetime.datetime(2013, 10, 22, 12, 15, 5, 118910, tzinfo=utc),
                        "last_modified": datetime.datetime(2013, 10, 22, 12, 15, 13, 201494, tzinfo=utc),
                        "mappings": [
                            {"cellid": 1, "key": "q"},
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
                            {"cellid": 12, "key": "c"}
                        ]
}

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
                 "user": None}

DEFAULT_KEYBOARD_STRING = """{"label":"Default","mappings":[{"cellid":1,"key":"q"},{"cellid":2,"key":"w"},{"cellid":3,"key":"e"},{"cellid":4,"key":"r"},{"cellid":5,"key":"t"},{"cellid":8,"key":"a"},{"cellid":9,"key":"s"},{"cellid":11,"key":"d"},{"cellid":10,"key":"f"},{"cellid":13,"key":"g"},{"cellid":7,"key":"z"},{"cellid":6,"key":"x"},{"cellid":12,"key":"c"}],"created":"2013-10-22T12:15:05.118910Z","is_primary":true,"last_modified":"2013-10-22T12:15:13.201494Z","user":null}"""
