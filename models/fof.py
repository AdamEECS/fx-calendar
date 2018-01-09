from . import MongoModel


class Fof(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('returnA', str, ''),
            ('structureForm', str, ''),
            ('nav', str, ''),
            ('intervalReturn', str, ''),
            ('dataFreq', str, ''),
            ('index', int, -1),
            ('investmentTarget', str, ''),
            ('sharpA', str, ''),
            ('stypeCodeName1', str, ''),
            ('pY', str, ''),
            ('region', str, ''),
            ('fundId', str, ''),
            ('maxRetracement', str, ''),
            ('orgId', str, ''),
            ('fundMember', str, ''),
            ('orgName', str, ''),
            ('fundName', str, ''),
            ('isInternal', str, ''),
            ('foundationDate', str, ''),
            ('navDate', str, ''),
            ('fundStatus', str, ''),
            ('fundNameFlag', str, ''),
            ('addedNav', str, ''),
            ('statisticDate', str, ''),
            ('stdevA', str, ''),
            ('stypeCodeName3', str, ''),

        ]
        fields.extend(super()._fields())
        return fields
