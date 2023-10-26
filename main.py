from datetime import datetime
from pickle import load, dump
from pathlib import Path
import re
from abc import abstractmethod, ABC


class DataTransfer:

    @staticmethod
    def load_data(filename):
        if Path(filename).exists():
            with open(filename, 'rb') as file:
                return load(file)
        return None

    @staticmethod
    def save_data(filename, data):
        with open(filename, 'wb') as file:
            dump(data, file)


class AbstractSerializer(ABC):

    @abstractmethod
    def serialize(self):
        pass
    @abstractmethod
    def deserialize(self, data):
        pass
    @abstractmethod
    def add_item(self, item):
        pass
    @abstractmethod
    def del_item(self, item):
        pass

class Serializable(AbstractSerializer):

    def load(self):
        data = DataTransfer.load_data(self.filename)
        if data:
            self.deserialize(data)

    def save(self):
        data = self.serialize()
        DataTransfer.save_data(self.filename, data)


class AddressBook(Serializable):

    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def add_item(self, key, item):
        self.data[key] = item

    def del_item(self, key):
        if key in self.data:
            del self.data[key]

    def serialize(self):
        return self.data

    def deserialize(self, data):
        self.data = data


class AbstractRecord(ABC):
    @abstractmethod
    def add_phone(self, phone):
        pass

    @abstractmethod
    def remove_phone(self, rem_phone):
        pass

    @abstractmethod
    def add_birthday(self, birthday):
        pass

    @abstractmethod
    def add_email(self, email):
        pass

    @abstractmethod
    def add_address(self, address):
        pass

    @abstractmethod
    def days_to_birthday(self):
        pass


class Record(AbstractRecord):

    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, rem_phone):
        self.phones = [phone for phone in self.phones if phone.value != rem_phone.value]

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
            birthday = birthday.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            return (birthday - today).days
        return None


class AbstractField(ABC):
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def set_value(self, value):
        pass


class Field(AbstractField):

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field, AbstractField):

    @Field.value.setter
    def value(self, value):
        if value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit() or value.isdigit() and len(value) in (
                10, 12):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format. Please enter the phone in the format'
                                          ' +000000000000, 000000000000, or 0000000000')


class Birthday(Field, AbstractField):

    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        try:
            birthday = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            birthday = None
        if birthday is not None and birthday < today:
            self._value = value
        else:
            raise BirthdayInvalidFormatError('Invalid birthday format. Please enter the birthday'
                                             ' in the format YYYY-MM-DD')


class Email(Field):

    @Field.value.setter
    def value(self, value):
        pattern = r"[A-Za-z][A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]{2,}"
        if re.match(pattern, value) is not None:
            self._value = value
        else:
            raise EmailInvalidFormatError('Invalid email format')


class Notes(Serializable):

    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def add_item(self, item):
        self.data.append(item)

    def del_item(self, item):
        self.data.remove(item)

    def serialize(self):
        return self.data

    def deserialize(self, data):
        self.data = data

class AbstractNode(ABC):
    pass

class Note:

    def __init__(self, text, tags=None, title=None):
        self.text = text
        self.tags = tags
        self.title = title


class Address(Field):
    pass


class PhoneInvalidFormatError(Exception):
    pass


class BirthdayInvalidFormatError(Exception):
    pass


class EmailInvalidFormatError(Exception):
    pass


class NoteInputInvalidFormatError(Exception):
    pass


address_book = AddressBook('address_book.bin')
note_book = Notes('note_book.bin')
