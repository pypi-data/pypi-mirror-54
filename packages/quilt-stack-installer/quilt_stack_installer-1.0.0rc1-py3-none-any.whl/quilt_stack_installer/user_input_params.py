import re

import boto3





class UserInputParam:
    def __init__(self, param_name, description, default_value, is_password=False, validation_regex=None, required=True):
        self.name = param_name
        self.description = description
        self.default = default_value
        self.is_password = is_password
        self.validation_regex = validation_regex
        self.required = required
        self._actual = "_NOT_SET"

    def is_valid(self, user_input):
        if self.required:
            if user_input is None:
                return False, f"{self.name} is a required parameter."
            if user_input.strip() == "":
                return False, f"{self.name} is a required parameter."

        if self.validation_regex is not None and user_input is not None:
            if re.match(self.validation_regex, user_input) is None:
                return False, f"{self.name} is required to match the regex {self.validation_regex}"

        return True, None

    @property
    def val_is_set(self):
        return self._actual != "_NOT_SET"

    @property
    def param_value(self):
        if not self.val_is_set:
            raise RuntimeError("Trying to retrieve param value that hasn't been set")
        return self._actual

    def set_val(self, val):
        self._actual = val

    def input_prompt(self):
        return f"{self.name}"
