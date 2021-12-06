from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
from dotenv import load_dotenv

from models.disputable_voting import DisputableVotingModel
from models.token_lockup import TokenLockupModel
from models.augmented_bonding_curve import BondingCurveHandler
from models.issue_generator import IssueGeneratorModel
from models.conviction_voting import ConvictionVotingModel
import models.import_params as import_params

app = Flask(__name__)
api = Api(app)
CORS(app)
load_dotenv()


class status(Resource):
    def get(self):
        try:
            return {'data': 'Api running'}
        except(error):
            return {'data': error}


class TokenLockup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('openingPrice', type=float)
        parser.add_argument('tokenFreeze', type=float)
        parser.add_argument('tokenThaw', type=float)
        parameters = parser.parse_args()
        opening_price = parameters['openingPrice']
        token_freeze_period = parameters['tokenFreeze']
        token_thaw_period = parameters['tokenThaw']

        token_lockup_model = TokenLockupModel(opening_price=opening_price,
                                              token_freeze_period=token_freeze_period,
                                              token_thaw_period=token_thaw_period)

        return jsonify(token_lockup_model.get_data())


class DisputableVoting(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('supportRequired', type=float)
        parser.add_argument('minimumQuorum', type=float)
        parser.add_argument('voteDuration', type=float)
        parser.add_argument('delegatedVotingPeriod', type=float)
        parser.add_argument('quietEndingPeriod', type=float)
        parser.add_argument('quietEndingExtension', type=float)
        parser.add_argument('executionDelay', type=float)
        parameters = parser.parse_args()
        support_required = parameters['supportRequired']
        minimum_quorum = parameters['minimumQuorum']
        vote_duration = parameters['voteDuration']
        delegated_voting_period = parameters['delegatedVotingPeriod']
        quiet_ending_period = parameters['quietEndingPeriod']
        quiet_ending_extension = parameters['quietEndingExtension']
        execution_delay = parameters['executionDelay']

        disputable_voting_model = DisputableVotingModel(support_required=support_required,
                                                        minimum_quorum=minimum_quorum,
                                                        vote_duration=vote_duration,
                                                        delegated_voting_period=delegated_voting_period,
                                                        quiet_ending_period=quiet_ending_period,
                                                        quiet_ending_extension=quiet_ending_extension,
                                                        execution_delay=execution_delay)

        return jsonify(disputable_voting_model.get_data())


class AugmentedBondingCurve(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('commonsTribute', type=str)
        parser.add_argument('openingPrice', type=str)
        parser.add_argument('entryTribute', type=str)
        parser.add_argument('exitTribute', type=str)
        parser.add_argument('ragequitAmount', type=str)
        parser.add_argument('initialBuy', type=str)
        parser.add_argument('stepList', action='append')
        parser.add_argument('virtualSupply', type=str)
        parser.add_argument('virtualBalance', type=str)
        parser.add_argument('zoomGraph', type=str)
        parser.add_argument('includeMilestones', type=str)
        parameters = parser.parse_args()
        commons_percentage = float(
            parameters['commonsTribute']) if parameters['commonsTribute'] is not None else 0.05
        opening_price = float(
            parameters['openingPrice']) if parameters['openingPrice'] is not None else 1.50
        entry_tribute = float(
            parameters['entryTribute']) if parameters['entryTribute'] is not None else 0.05
        exit_tribute = float(
            parameters['exitTribute']) if parameters['exitTribute'] is not None else 0.05
        ragequit_amount = float(
            parameters['ragequitAmount']) if parameters['ragequitAmount'] is not None else 0
        initial_buy = float(
            parameters['initialBuy']) if parameters['initialBuy'] is not None else 0
        steplist = parameters['stepList'] if parameters['stepList'] is not None else [
        ]
        virtual_supply = float(
            parameters['virtualSupply']) if parameters['virtualSupply'] is not None else 1
        virtual_balance = float(
            parameters['virtualBalance']) if parameters['virtualBalance'] is not None else 1
        zoom_graph = int(
            parameters['zoomGraph']) if parameters['zoomGraph'] is not None else 0
        include_milestones = int(
            parameters['includeMilestones']) if parameters['includeMilestones'] is not None else 0

        # add default steps
        steplist.insert(0, "[5000, 'wxDAI']")
        steplist.insert(1, "[100000, 'wxDAI']")
        steplist.insert(2, "[3000, 'TEC']")

        try:
            augmented_bonding_curve_model = BondingCurveHandler(
                commons_percentage=commons_percentage,
                ragequit_amount=ragequit_amount,
                opening_price=opening_price,
                entry_tribute=entry_tribute,
                exit_tribute=exit_tribute,
                initial_buy=initial_buy,
                virtual_supply=virtual_supply,
                virtual_balance=virtual_balance,
                steplist=steplist,
                zoom_graph=zoom_graph,
                include_milestones=include_milestones
            )
        except ValueError as ve:
            return jsonify(str(ve))

        return jsonify(augmented_bonding_curve_model.get_data())


class IssueGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('overallStrategy', type=str)
        parser.add_argument('tokenLockup', type=dict)
        parser.add_argument('augmentedBondingCurve', type=dict)
        parser.add_argument('taoVoting', type=dict)
        parser.add_argument('convictionVoting', type=dict)
        parser.add_argument('advancedSettings', type=dict)

        parameters = json.loads(request.form.get('body'))
        image_files = request.files
        title = parameters['title']
        overall_strategy = parameters['overallStrategy']
        token_lockup = parameters['tokenLockup']
        abc = parameters['augmentedBondingCurve']
        tao_voting = parameters['taoVoting']
        conviction_voting = parameters['convictionVoting']
        advanced_settings = parameters['advancedSettings']

        abc['commonsTribute'] = float(
            abc['commonsTribute']) if abc['commonsTribute'] is not None else 0.05
        abc['openingPrice'] = float(
            abc['openingPrice']) if abc['openingPrice'] is not None else 1.50
        abc['entryTribute'] = float(
            abc['entryTribute']) if abc['entryTribute'] is not None else 0.05
        abc['exitTribute'] = float(
            abc['exitTribute']) if abc['exitTribute'] is not None else 0.05
        abc['ragequitAmount'] = float(
            abc['ragequitAmount']) if abc['ragequitAmount'] is not None else 0
        abc['initialBuy'] = float(
            abc['initialBuy']) if abc['initialBuy'] is not None else 0
        # removed this line following the feature cut 25/11/21
        #abc['reserveBalance'] = float(abc['reserveBalance']) if abc['reserveBalance'] is not None else (1571223.57 - abc.initial_buy - abc.ragequit_amount)*(1-abc.commons_percentage)
        # change to account for new default steps
        abc['stepList'] = abc['stepList'] if abc['stepList'] is not abc else []
        abc['stepList'].insert(0, "[5000, 'wxDAI']")
        abc['stepList'].insert(1, "[100000, 'wxDAI']")
        abc['stepList'].insert(2, "[3000, 'TEC']")
        abc['virtualSupply'] = float(
            abc['virtualSupply']) if abc['virtualSupply'] is not None else 1
        abc['virtualBalance'] = float(
            abc['virtualBalance']) if abc['virtualBalance'] is not None else 1
        abc['zoomGraph'] = int(
            abc['zoomGraph']) if abc['zoomGraph'] is not None else 0
        # added the milestone generation for the issue generator
        abc['includeMilestones'] = int(1)

        issue_generator = IssueGeneratorModel(
            raw_body=parameters,
            title=title,
            token_lockup=token_lockup,
            abc=abc,
            tao_voting=tao_voting,
            conviction_voting=conviction_voting,
            advanced_settings=advanced_settings,
            overall_strategy=overall_strategy,
            image_files=image_files
        )

        return jsonify(issue_generator.generate_output())


class ConvictionVoting(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('spendingLimit', type=float)
        parser.add_argument('minimumConviction', type=float)
        parser.add_argument('convictionGrowth', type=int)
        parser.add_argument('convictionVotingPeriodDays', type=float)
        parser.add_argument('tableScenarios', type=list, action='append')
        parameters = parser.parse_args()
        spending_limit = parameters['spendingLimit']
        minimum_conviction = parameters['minimumConviction']
        conviction_growth = parameters['convictionGrowth']
        voting_period_days = parameters['convictionVotingPeriodDays']
        table_scenarios = parameters['tableScenarios']

        conviction_voting_model = ConvictionVotingModel(
            spending_limit=spending_limit,
            minimum_conviction=minimum_conviction,
            conviction_growth=conviction_growth,
            voting_period_days=voting_period_days,
            table_scenarios=table_scenarios
        )

        return jsonify(conviction_voting_model.get_data())


class ImportParams(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('issueNumber', type=int)
        parameters = parser.parse_args()
        issue_number = parameters.get('issueNumber', '')

        return jsonify(import_params.get_data(issue_number))


api.add_resource(status, '/')
api.add_resource(ImportParams, '/import-parameters/')
api.add_resource(TokenLockup, '/token-lockup/')
api.add_resource(DisputableVoting, '/disputable-voting/')
api.add_resource(AugmentedBondingCurve, '/augmented-bonding-curve/')
api.add_resource(IssueGenerator, '/issue-generator/')
api.add_resource(ConvictionVoting, '/conviction-voting/')


if __name__ == '__main__':
    app.run(debug=True)
