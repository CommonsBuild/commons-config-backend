import pandas as pd
import numpy as np
import math


class ConvictionVotingModel:
    def __init__(self,
                 spending_limit=None,
                 minimum_conviction=None,
                 conviction_growth=None,
                 voting_period_days=None):
        self.spending_limit = spending_limit if spending_limit is not None else 0.2
        self.minimum_conviction = minimum_conviction if minimum_conviction is not None else 0.05
        self.conviction_growth = conviction_growth if conviction_growth is not None else 2
        self.voting_period_days = voting_period_days if voting_period_days is not None else 7 
        self.staked_on_proposal = 1
        self.staked_on_other_proposals = 0
        self.min_active_stake_pct = 0.05
        self.table_scenarios = [
            {
                'label': 'scenario1',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 1_000,
                'amountInCommonPool': 10_000,
            },
            {
                'label': 'scenario2',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 1_000,
                'amountInCommonPool': 750_000,
            },
            {
                'label': 'scenario3',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 5_000,
                'amountInCommonPool': 100_000,
            },
            {
                'label': 'scenario4',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 5_000,
                'amountInCommonPool': 750_000,
            },
            {
                'label': 'scenario5',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 25_000,
                'amountInCommonPool': 100_000,
            },
            {
                'label': 'scenario6',
                'totalEffectiveSupply': 100_000,
                'requestedAmount': 25_000,
                'amountInCommonPool': 750_000,
            },
        ]
        self.output_dict = {}
        self.output_dict['input'] = {
            'spendingLimit': self.spending_limit,
            'minimumConviction': self.minimum_conviction,
            'convictionGrowth': self.conviction_growth,
            'convictionVotingPeriodDays': self.voting_period_days,
        }
    
    def get_decay(self):
        return (1 / 2) ** (1 / self.conviction_growth)

    def get_weight(self):
        return self.minimum_conviction * self.spending_limit ** 2
    
    def get_conviction(self, initial_conviction, amount, time):
        return initial_conviction * self.get_decay() ** time + (amount * (1 - self.get_decay() ** time)) / (1 - self.get_decay())

    def get_max_conviction(self, amount):
        return amount / (1 - self.get_decay())
    
    def get_staked_on_proposals(self):
        return self.staked_on_proposal + self.staked_on_other_proposals

    def get_staked(self, staked = None):
        if staked is None:
            staked = self.get_staked_on_proposals()
        return np.where(staked > self.min_active_stake_pct, staked, self.min_active_stake_pct)

    def get_threshold(self, requested_pct):
        return self.get_weight() / (self.spending_limit - requested_pct) ** 2 if np.any(requested_pct <= self.minimum_conviction) else float('inf')

    def current_conviction_pergentage_of_max(self, time):
        current_conviction = self.get_conviction(0, self.staked_on_proposal, time=time)
        max_conviction =    self.get_max_conviction(self.get_staked())
        current_conviction_percentage = current_conviction / max_conviction
        return current_conviction_percentage        

    def get_data(self):
        # Conviction Growth Chart Data
        x = np.linspace(0, 5 * self.conviction_growth,100)
        y = 100 * self.current_conviction_pergentage_of_max(time=x)
        df_growth = pd.DataFrame(zip(x, y), columns=['timeDays','convictionPercentage'])
        
        x2 = np.linspace(5 * self.conviction_growth,10 * self.conviction_growth,1000)
        y2 = y[-1] * self.get_decay()**x
        df_decay = pd.DataFrame(zip(x2, y2), columns=['timeDays','convictionPercentage'])
        
        df = pd.concat([df_growth, df_decay])
        self.output_dict['output'] = {'convictionGrowthChart' : df.to_dict(orient='list')}
        self.output_dict['output']['maxConvictionGrowthXY'] = {
            'x': df_growth.iloc[df_growth['convictionPercentage'].idxmax()]['timeDays'],
            'y': df_growth.iloc[df_growth['convictionPercentage'].idxmax()]['convictionPercentage'],
        }

        self.output_dict['output']['convictionGrowth80PercentageXY'] = {
            'x': df_growth.iloc[df_growth[df_growth.convictionPercentage >= 80].first_valid_index()]['timeDays'],
            'y': df_growth.iloc[df_growth[df_growth.convictionPercentage >= 80].first_valid_index()]['convictionPercentage'],
        }

        # Conviction Threshold Chart Data
        x = np.linspace(1, 100 * (self.spending_limit - np.sqrt(self.get_weight())), 100)
        y = 100 * (self.get_threshold(x / 100) / self.current_conviction_pergentage_of_max(time=self.voting_period_days))
        df = pd.DataFrame(zip(x,y), columns=['requestedPercentage', 'thresholdPercentage'])
        self.output_dict['output']['convictionThresholdChart'] = df.to_dict(orient='list')

        # Conviction Threshold Scenarios Data
        table_scenarios = []
        for scenario in self.table_scenarios:
            percentage_requested = scenario['requestedAmount'] / scenario['amountInCommonPool']
            percentage_requested_threshold = self.get_threshold(percentage_requested)
            if math.isinf(percentage_requested_threshold):
                scenario['minTokensToPass'] = 'Not possible'
                scenario['tokensToPassIn2Weeks'] = 'Not possible'
            else:
                scenario['minTokensToPass'] = int(
                    scenario['totalEffectiveSupply'] *
                    self.get_threshold(percentage_requested)
                )
                scenario['tokensToPassIn2Weeks'] = int(
                    scenario['minTokensToPass'] / 
                    self.current_conviction_pergentage_of_max(time=4)
                )
            table_scenarios.append(scenario)
        self.output_dict['output']['table'] = table_scenarios

        return self.output_dict
