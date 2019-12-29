import json
import datetime as dt


class User:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = dt.datetime.fromtimestamp(birthdate)
        self.gender = gender

        assert self.gender in ['m', 'f', 'o'], 'unknown gender'

    def __repr__(self):
        if self.gender == 'm':
            gender = 'male'
        elif self.gender == 'f':
            gender = 'female'
        else:
            gender = 'other'
        
        birth_repr = self.birthdate.strftime('%B %d, %Y')

        return f'user {self.user_id}: {self.username}, born '\
               f'{birth_repr} ({gender})'

    def dict(self):
        return dict(user_id=self.user_id, 
                    username=self.username,
                    birthdate=int(self.birthdate.timestamp()),
                    gender=self.gender)

    def json(self):
        return json.dumps(self.dict())

    @classmethod
    def from_dict(cls, **kwargs):
        return User(kwargs['user_id'], kwargs['username'],
                    kwargs['birthdate'], kwargs['gender'])