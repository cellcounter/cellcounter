import json
import validictory
from validictory.validator import FieldValidationError
from cellcounter.keyboardapi.defaults import TEST_POST_KEYBOARD_MAP
from django.core.exceptions import ValidationError

class ValidJSONValidator(object):
    schema = {
        "patternProperties": {
            "[a-z]": {
                "properties": {
                    "cellid": {
                        "type": "integer"}
                }, "additionalProperties": False,
            }
        }, "additionalProperties": False,
    }
    code = 'invalid'
    message = ''

    def __call__(self, json_string):
        try:
            validictory.validate(json.loads(json_string), self.schema)
        except FieldValidationError:
            self.message = 'Invalid formatted data passed to keyboard'
            raise ValidationError(self.message, code=self.code)
        except ValueError:
            self.message = 'Malformed JSON presented to keyboard'
            raise ValidationError(self.message, code=self.code)
