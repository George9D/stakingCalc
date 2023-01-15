# price: current price of the token
# inflationSchedule: nbr token issued per period + end of period as date
# totalStakedToken: total amount of token staked right at the moment
# bondedRatio:  portion of staked tokens in the network
# inflationShareStaking: share of inflation issued to stakers
# containing sum of staking rewards earned by GATA delegators on each chain

class Token:
    def __init__(self, name, price, inflationSchedule, totalStakedToken,
                 inflationShareStaking, yearlyTxFees, levelLinearization, trendLinearization):
        self.name = name
        self.price = price
        self.inflationSchedule = inflationSchedule
        self.totalStakedToken = totalStakedToken
        self.inflationShareStaking = inflationShareStaking
        self.yearlyTxFees = yearlyTxFees
        self.levelLinearization = levelLinearization
        self.trendLinearization = trendLinearization

    def get_token_name(self):
        return self.name