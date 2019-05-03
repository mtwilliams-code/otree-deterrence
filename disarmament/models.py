from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

author = 'Matthew Williams'

doc = """
Two players make decisions about how to treat their nuclear stockpile.
"""


class Constants(BaseConstants):
    name_in_url = 'disarmament'
    players_per_group = 2
    num_rounds = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        info = itertools.cycle(['perfect','perfect','imperfect','imperfect'])
        for p in self.get_players():
            if not 'nukes' in p.participant.vars:
                p.participant.vars['nukes'] = 50
            if not 'payoff' in p.participant.vars:
                p.participant.vars['payoff'] = 0
            if not 'information' in p.participant.vars:
                p.participant.vars['information'] = next(info)
        for p in self.get_players():
            if p.participant.vars['information'] == 'perfect':
                p.information = 'num'
            elif p.participant.vars['information'] == 'imperfect':
                p.information = random.choices(['num','move','none'],weights=[10,25,65])[0]
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    information = models.StringField()

    stockpileAdjustment = models.IntegerField(
        label="How many nuclear warheads do you want to build/destroy?",
        min=-15,
        max=15
    )

    startWar = models.BooleanField(
        label="Do you want to attack and start a nuclear war?",
        choices=[
            [True, "Yes"],
            [False, "No"],
        ]
    )

    def get_payoff(self):
        return self.participant.vars['nukes']

    def role(self):
        if self.id_in_group == 1:
            return 'USA'
        elif self.id_in_group == 2:
            return 'USSR'

    pass
