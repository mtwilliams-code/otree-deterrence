from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class StockpileAdjustment(Page):
    def vars_for_template(self):
        if self.player.information == 'num':
            info = "You learned that your opponent has " + str(self.player.get_others_in_group()[0].participant.vars['nukes']) + ' nuclear warheads.'
        elif self.player.information == 'move':
            info = "You learned that your opponent built " + str(self.player.get_others_in_group()[0].in_round(self.round_number-1).stockpileAdjustment) + ' nuclear warheads last round.'
        else:
            info = ""
        return {
            'nukes' : self.participant.vars['nukes'],
            'info' : info
        }
    form_model = 'player'
    form_fields = ['stockpileAdjustment']

    def before_next_page(self):
        if self.player.stockpileAdjustment > 0:
            self.player.participant.vars['payoff'] -= self.player.stockpileAdjustment * 0.5
        elif self.player.stockpileAdjustment < 0:
            self.player.participant.vars['payoff'] -= self.player.stockpileAdjustment * 0.2
        self.player.participant.vars['payoff'] -= self.player.participant.vars['nukes'] * 0.1
        self.player.participant.vars['nukes'] += self.player.stockpileAdjustment
    pass


class WarWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class War(Page):
    def vars_for_template(self):
        return {
            'nukes' : self.participant.vars['nukes'],
        }

    def before_next_page(self):
        for p in self.group.get_players():
            if p.startWar == True:
                nukes = [self.participant.vars['nukes'], self.player.get_others_in_group()[0].participant.vars['nukes']]

    form_model = 'player'
    form_model = 'player'
    form_fields = ['startWar']

    pass

class ResultsWaitPage(WaitPage):
 
    def after_all_players_arrive(self):
        pass


class Results(Page):
    def is_displayed(self):
        for p in self.group.get_players():
            if p.startWar == True:
                return True
        return False

    def vars_for_template(self):
        p = self.player.get_others_in_group()[0]

        if self.participant.vars['nukes'] == 0 and p.participant.vars['nukes'] >= 20:
            self.participant.vars['payoff'] += -200
        elif self.participant.vars['nukes'] == 0 and p.participant.vars['nukes'] < 20:
            self.participant.vars['payoff'] += -10 * p.participant.vars['nukes']

        elif self.participant.vars['nukes'] >= 20 and p.participant.vars['nukes'] == 0:
            self.participant.vars['payoff'] += 100
        elif self.participant.vars['nukes'] < 20 and p.participant.vars['nukes'] == 0:
            self.participant.vars['payoff'] += 5 * p.participant.vars['nukes']
        
        elif self.participant.vars['nukes'] == p.participant.vars['nukes']:
            self.participant.payoff += -100

        elif self.participant.vars['nukes'] < p.participant.vars['nukes']:
            self.participant.var['payoff'] += 1 - (self.participant.vars['nukes'] / p.participant.vars['nukes']) * -100 - 100
        elif self.participant.vars['nukes'] > p.participant.vars['nukes']:
            self.participant.vars['payoff'] += 1 - (p.participant.vars['nukes'] / self.participant.vars['nukes']) * -250 - 100
        
        result = ""
        if p.get_payoff() < self.player.get_payoff():
            result = "WON" 
        elif p.get_payoff() > self.player.get_payoff():
            result = 'LOST'
        else:
             result = "TIED"
             
        self.player.payoff = self.participant.vars['payoff']
        p.payoff = self.participant.vars['payoff']
            
        return {
            'result' : result,
            'yourCost' : self.participant.vars['payoff'],
            'theirCost' : p.participant.vars['payoff'],
            'yourNukes' : self.participant.vars['nukes'],
            'theirNukes' : p.participant.vars['nukes']
        }

    pass



page_sequence = [
    StockpileAdjustment,
    War,
    ResultsWaitPage,
    Results
]
