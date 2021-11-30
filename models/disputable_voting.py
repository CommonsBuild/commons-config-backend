import pandas as pd


class DisputableVotingModel:
    def __init__(self,
                 support_required=None,
                 minimum_quorum=None,
                 vote_duration=None,
                 delegated_voting_period=None,
                 quiet_ending_period=None,
                 quiet_ending_extension=None,
                 execution_delay=None):
        self.support_required = support_required if support_required is not None else 0.4
        self.minimum_quorum = minimum_quorum if minimum_quorum is not None else 0.1
        self.vote_duration = vote_duration if vote_duration is not None else 6
        self.delegated_voting_period = delegated_voting_period if delegated_voting_period is not None else 3
        self.quiet_ending_period = quiet_ending_period if quiet_ending_period is not None else 2
        self.quiet_ending_extension = quiet_ending_extension if quiet_ending_extension is not None else 1
        self.execution_delay = execution_delay if execution_delay is not None else 1
        self.non_quiet_voting_period = max(self.vote_duration - self.quiet_ending_period, 0)
        self.output_dict = {}
        self.output_dict['input'] = {
            'supportRequired': self.support_required,
            'minimumQuorum': self.minimum_quorum,
            'voteDuration': self.vote_duration,
            'delegatedVotingPeriod': self.delegated_voting_period,
            'quietEndingPeriod': self.quiet_ending_period,
            'quietEndingExtension': self.quiet_ending_extension,
            'executionDelay': self.execution_delay
        }

    def get_data(self):
        # Bar Chart Data
        bar_chart_items = {
            'totalProposalProcess': {
                'nonQuietVotingPeriod': self.non_quiet_voting_period,
                'quietEndingPeriod': self.quiet_ending_period,
                'executionDelay': self.execution_delay
            },
            'delegatedVoting': {
                'delegatedVotingPeriod': self.delegated_voting_period
            },
            'proposalProcessWithExtension': {
                'voteDuration': self.vote_duration,
                'quietEndingExtension': self.quiet_ending_extension,
                'executionDelay': self.execution_delay
            },
            'voteDuration': self.vote_duration,
        }
        self.output_dict['output'] = {'barChart': bar_chart_items}

        # Pie Chart Data
        pie_chart_items = {
            'nonQuietVotingPeriod': self.non_quiet_voting_period,
            'quietEndingPeriod': self.quiet_ending_period,
            'quietEndingExtension': self.quiet_ending_extension,
            'executionDelay': self.execution_delay
        }
        self.output_dict['output']['pieChart'] = pie_chart_items

        # Table Data
        time_vote = {
            'noExtension': self.vote_duration,
            'firstExtension': self.vote_duration + self.quiet_ending_extension,
            'secondExtension': self.vote_duration + (2 * self.quiet_ending_extension)
        }
        time_review = {
            'noExtension': self.vote_duration - self.delegated_voting_period,
            'firstExtension': self.vote_duration - self.delegated_voting_period + self.quiet_ending_extension,
            'secondExtension': self.vote_duration - self.delegated_voting_period + (2 * self.quiet_ending_extension)
        }
        time_execute = {
            'noExtension': self.vote_duration + self.execution_delay,
            'firstExtension': self.vote_duration + self.execution_delay + self.quiet_ending_extension,
            'secondExtension': self.vote_duration + self.execution_delay + (2 * self.quiet_ending_extension)
        }

        self.output_dict['output']['table'] = {
            'timeVote': [time_vote['noExtension'], time_vote['firstExtension'], time_vote['secondExtension']],
            'timeReview': [time_review['noExtension'], time_review['firstExtension'], time_review['secondExtension']],
            'timeExecute': [time_execute['noExtension'], time_execute['firstExtension'], time_execute['secondExtension']]
        }

        return self.output_dict
