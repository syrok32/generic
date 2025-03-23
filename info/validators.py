import re
from rest_framework.validators import ValidationError
class YouTubeValidator:
    def __init__(self,  field):
        self.field= field

    def __call__(self, value):
        reg = re.search('youtube', value.get(self.field))

        if not reg:
            raise ValidationError('error')

