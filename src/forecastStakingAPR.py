import datetime
import pandas as pd
import inflationSchedules as ifs
from tokenClass import Token

def convertPeriod(compPeriod):
    for p in range(4):
        if compPeriod == "daily":
            return 1
        elif compPeriod == "weekly":
            return 7
        elif compPeriod == "monthly":
            return 30
        else:
            return 365

def calcRewardsNew(token, stakingAmount, stakingPeriod, commission, compingPeriod, compShare):
    startDate = datetime.datetime.now()
    endDate = 0
    currentStakingRewards = 0
    currentStakingPeriod = 0
    restakedRewards = 0
    takenOutRewards = 0
    unusedStakingRewards = 0
    compPeriod = convertPeriod(compingPeriod)
    cumStakingRewards = 0
    initStakingAmount = stakingAmount
    basicStakingRwds = 0

    L0 = token.levelLinearization
    T0 = token.trendLinearization
    t = 1

    columns = ['Date', 'APR', 'StakingRewards', 'cumStakingRewards', 'compRewards', 'takenOutRewards']
    df =  pd.DataFrame(columns=columns)

    DATE = []
    APR = []
    STAKINGREWARDS = []
    COMPREWARDS = []
    TAKENOUTREWARDS = []
    CUMSTAKINGREWARDS = []
    BASICSTAKINGREWARDS = []

# ----------------------------------- INITIALIZATION --------------------------------------------------
    # search for current epoch & set staking rewards accordingly for each token
    for j in range(len(token.inflationSchedule)):
        if startDate < token.inflationSchedule[j][1]:
            endDate = token.inflationSchedule[j][1]
            currentStakingRewards = token.inflationSchedule[j][0] * \
                                    token.inflationShareStaking / 100 + token.yearlyTxFees
            currentStakingPeriod = j
            break

    # how many epochs (=days) until the current period ends
    remainingEpochs = (endDate - startDate).days

    for t in range(stakingPeriod):
        # check period & update staking rewards if necessary
        if remainingEpochs == 0:
            currentStakingPeriod += 1
            # check if token emission schedule has ended -> stop calculation!
            if currentStakingPeriod == len(token.inflationSchedule):
                # print("No more staking rewards due to inflation - only TxFees taken into account!")
                currentStakingRewards = token.yearlyTxFees
            else:
                currentStakingRewards = token.inflationSchedule[currentStakingPeriod][0] * \
                                        token.inflationShareStaking / 100 + token.yearlyTxFees
                remainingEpochs = 365  # each period lasts 1 year

        remainingEpochs -= 1
        currentDate = startDate + datetime.timedelta(days=t)
        DATE.append(currentDate.date())

        # forecast the nbr of token staked using double exponential smoothing
        forcastTokenStaked = L0 + T0 * t
        #t += 1

        dailyAPR = currentStakingRewards / forcastTokenStaked / 365
        APR.append(dailyAPR*36500)

        stakingRewards = stakingAmount * dailyAPR * (1 - commission / 100)
        STAKINGREWARDS.append(stakingRewards)
        BASICSTAKINGREWARDS.append(initStakingAmount * dailyAPR * (1 - commission / 100))

        cumStakingRewards += stakingRewards
        CUMSTAKINGREWARDS.append(cumStakingRewards)

        if (t+1) % compPeriod != 0:
            unusedStakingRewards += stakingRewards
            COMPREWARDS.append(0)
            TAKENOUTREWARDS.append(0)
        else:
            # update nbr of token staked, taking compounding into account
            stakingAmount += (stakingRewards + unusedStakingRewards) * compShare / 100

            # nbr of token that were compounded -> restaking
            compRewards = (stakingRewards + unusedStakingRewards) * compShare / 100
            COMPREWARDS.append(compRewards)

            # nbr of token that were not compounded -> profit taking
            takenOutRewards = (stakingRewards + unusedStakingRewards) * (1 - compShare / 100)
            TAKENOUTREWARDS.append(takenOutRewards)

            unusedStakingRewards = 0

    df['Date'] = DATE
    df['APR'] = APR
    df['stakingRewards'] = STAKINGREWARDS
    df['compRewards'] = COMPREWARDS
    df['takenOutRewards'] = TAKENOUTREWARDS
    df['cumStakingRewards'] = CUMSTAKINGREWARDS
    df['basicStakingRewards'] = BASICSTAKINGREWARDS

    return df