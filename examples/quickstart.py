import re
from datetime import date
from pprint import pprint

import attr
import paxb as pb


xml = '''<?xml version="1.0" encoding="utf-8"?>
<doc:envelope xmlns="http://www.test.org"
              xmlns:doc="http://www.test1.org">
    <doc:user name="Alexey" surname="Ivanov" age="26">
    
        <doc:birthdate year="1992" month="06" day="14"/>

        <doc:contacts>
            <doc:phone>+79204563539</doc:phone>
            <doc:email>alex@gmail.com</doc:email>
            <doc:email>alex@mail.ru</doc:email>
        </doc:contacts>

        <doc:documents>
            <doc:passport series="3127" number="836815"/>
        </doc:documents>

        <data:occupations xmlns:data="http://www.test2.org">
            <data:occupation title="yandex">
                <data:address>Moscow</data:address>
                <data:employees>8854</data:employees>
            </data:occupation>
            <data:occupation title="skbkontur">
                <data:address>Yekaterinburg</data:address>
                <data:employees>7742</data:employees>
            </data:occupation>
        </data:occupations>

    </doc:user>
</doc:envelope>
'''


@pb.model(name='occupation', ns='data', ns_map={'data': 'http://www.test2.org'})
class Occupation:
    title = pb.attr()
    address = pb.field()
    employees = pb.field(converter=int)


@pb.model(name='user', ns='doc', ns_map={'doc': 'http://www.test1.org'})
class User:
    name = pb.attr()
    surname = pb.attr()
    age = pb.attr(converter=int)

    birth_year = pb.wrap('birthdate', pb.attr('year', converter=int))
    birth_month = pb.wrap('birthdate', pb.attr('month', converter=int))
    birth_day = pb.wrap('birthdate', pb.attr('day', converter=int))

    @property
    def birthdate(self):
        return date(year=self.birth_year, month=self.birth_month, day=self.birth_day)

    @birthdate.setter
    def birthdate(self, value):
        self.birth_year = value.year
        self.birth_month = value.month
        self.birth_day = value.day

    phone = pb.wrap('contacts', pb.field())
    emails = pb.wrap('contacts', pb.as_list(pb.field(name='email')))

    passport_series = pb.wrap('documents/passport', pb.attr('series'))
    passport_number = pb.wrap('documents/passport', pb.attr('number'))

    occupations = pb.wrap(
        'occupations', pb.lst(pb.nested(Occupation)), ns='data', ns_map={'data': 'http://www.test2.org'}
    )

    citizenship = pb.field(default='RU')

    @phone.validator
    def check(self, attribute, value):
        if not re.match(r'\+\d{11,13}', value):
            raise ValueError("phone number is incorrect")


try:
    user = pb.from_xml(User, xml, envelope='doc:envelope', ns_map={'doc': 'http://www.test1.org'})
    user.birthdate = user.birthdate.replace(year=1993)
    pprint(attr.asdict(user))

except (pb.exc.DeserializationError, ValueError) as e:
    print(f"deserialization error: {e}")
