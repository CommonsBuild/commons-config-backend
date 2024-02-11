# Token Engineering Commons Upgrade Dashboard Backend

This repository contains the API for the four models of the Token Engineering Commons Upgrade Dashboard:
1. Token Freeze and Token Thaw
2. Augmented Bonding Curve (ABC)
3. Tao Voting
4. Conviction Voting

## Models

### 1. Token Freeze and Token Thaw
The model inputs are:
- `openingPrice` (the initial price floor for the token)
- `tokenFreeze` (number of weeks that the opening price will be kept the same)
- `tokenThaw` (number of weeks in which the price floor will go from the opening price to zero)

The model output is a linechart data of the price floor over time and a table with the price floor and % of tokens unlocked in specific weeks.

To do an API call with the model input and receive the model outputs, it uses a POST request through the route `/token-lockup/` with the following body:
```json
{
  "openingPrice": 5,
  "tokenFreeze": 20,
  "tokenThaw": 15
}
```

### 2. Augmented Bonding Curve
The model inputs are:
- `commonsPercentage` (Percentage of funds that get substracted from the total funding to go to the commons pool. Between 0 and 95)
- `ragequitPercentage` (Percentage of supply burned before the bonding curve gets initialized. Between 0 and 20)
- `initialPrice` (Initial token prive. No real limit but, expected to be between 1 and 4)
- `entryTribute` (Percentage of funds substracted on buy (mint) operations before interacting with the bonding curve. Between 0 and 99)
- `exitTribute` (Percentage of funds substracted on sell (burn) operations after interacting with the boding curve.  Between 0 and 99)
- `stepList` Set of buy/sell operations applied to the bonding curve. AMOUNT IN THOUSANDS. List with format `[[AMOUNT, "TOKEN"],[AMOUNT, "TOKEN"]]`
- `zoomGraph` optional, value 0 or 1. Used to specify if the draw function should show the whole curve(0) or "zoom in" into the area where operations are happening (1)

The model output is a linechart data of the price plotted over the wxDai balance and a table showing how price evolves when the steps are applied and the resulting tribute/slippage.

To do an API call with the model input and receive the model outputs, it uses a POST request through the route `/augmented-bonding-curve/` with the following body:
```json
{
  "commonsTribute": 0.5,
  "ragequitAmount": 60,
  "openingPrice": 1.65,
  "entryTribute": 0.02,
  "exitTribute": 0.15,
  "reserveBalance": 1571.22357,
  "initialBuy": 0,
  "stepList": [[100, "wxDai"]],
  "zoomGraph": 0
}
```

### 3. Tao Voting
The model inputs are:
- `supportRequired` (Minimum percentage of "yes" votes in relation to the total votes needed to a proposal pass)
- `minimumQuorum` (Minimum percentage of quorum needed to a proposal pass)
- `voteDuration` (Vote duration in days)
- `delegatedVotingPeriod` (Delegated voting period in days)
- `quietEndingPeriod` (Quiet ending period in days)
- `quietEndingExtension` (Quiet ending extension in days)
- `executionDelay` (Execution delay in days)

The model output is a bar chart plot of the voting timeline and a pie chart of the division of periods within the Tao voting.

To do an API call with the model input and receive the model outputs, it uses a POST request through the route `/disputable-voting/` (the old name for Tao Voting) with the following body:
```json
{
  "supportRequired": 0.4,
  "minimumQuorum": 0.1,
  "voteDuration": 7,
  "delegatedVotingPeriod": 3,
  "quietEndingPeriod": 2,
  "quietEndingExtension": 1,
  "executionDelay": 1
}
```

### 4. Conviction Voting
The model inputs are:
- `convictionGrowth` (Number of days to a staked vote to acquire 50% of the maximum conviction)
- `convictionVotingPeriodDays` (Number of days that a vote is staked and acquiring conviction)
- `minimumConviction` (Minimum conviction to pass the smallest proposal possible)
- `spendingLimit` (Maximum percentage of the Commons Pool requested by a proposal)

The model output is a line chart plot of the percentage of effective supply voting on a proposal over the percentage of the commons pool funds being requested and a table showing different scenarios of the amount in the Commons Pool.

To do an API call with the model input and receive the model outputs, it uses a POST request through the route `/conviction-voting/` with the following body:
```json
{
  "convictionGrowth": 2,
  "convictionVotingPeriodDays": 7,
  "minimumConviction": 0.05,
  "spendingLimit": 0.2
}
```

### 5. Output Generator
This endpoint takes as input all the previous model inputs and generate a github issue with all the selected parameters and outputs. 

To do an API call with the model input and receive the model outputs, it uses a POST request through the route `/issue-generator/` with the following body:
```json
{
  "title": "TEC Dashboard Parameters Proposal",
  "overallStrategy": "",
  "tokenLockup": {
    "strategy": "",
    "openingPrice": 5,
    "tokenFreeze": 20,
    "tokenThaw": 15
  },
  "augmentedBondingCurve": {
    "strategy": "",
    "commonsTribute": 0.5,
    "ragequitAmount": 60,
    "openingPrice": 1.65,
    "entryTribute": 0.02,
    "exitTribute": 0.15,
    "reserveBalance": 1571.22357,
    "initialBuy": 0,
    "stepList": [[5000, "wxDai"], [100000, "wxDai"], [3000, "TEC"]],
    "zoomGraph": 0
  },
  "taoVoting": {
    "strategy": "",
    "supportRequired": 40,
    "minimumQuorum": 10,
    "voteDuration": 7,
    "delegatedVotingPeriod": 3,
    "quietEndingPeriod": 2,
    "quietEndingExtension": 1,
    "executionDelay": 1
  },
  "convictionVoting": {
    "strategy": "",
    "convictionGrowth": 2,
    "minimumConviction": 0.01,
    "votingPeriodDays": 7,
    "spendingLimit": 0.2
  },
  "advancedSettings": {
    "minimumEffectiveSupply": 4,
    "hatchersRageQuit": 3,
    "virtualBalance": 3000000
  }
}
```

### 6. Import Parameters
This endpoint takes as input the output issue number and return all of its parameters into a JSON format.
To do an API call with the model input and receive the model outputs, it uses a GET request through the route `/import-parameters/` with the following body:
```json
{
	"issueNumber": 177
}
```

## Install

For setting up the Python3 virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

To install the requirements
```bash
pip install -r requirements.txt
```

## Usage

To run the development server locally
```bash
python main.py 
```
It can be reached at http://127.0.0.1:5000/.
