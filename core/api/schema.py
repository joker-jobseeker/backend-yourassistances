from core.ext import ma
from core.models import YourAssistance

class YoaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = YourAssistance
        include_fk = True

yoa_schemas = YoaSchema(many=True)
yoa_schema = YoaSchema()