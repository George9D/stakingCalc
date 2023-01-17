'''
The goal of this program is to calculate the future staking rewards of a given token.

Difference to stakingrewards.com:
 - takes inflation schedule into account, which has a significant influence on APR!
 - can account for different percentages of restaking -> not only 0 or 100 %
 - additional revenue for stakers in the form of tx fees possible

 -> can implement dynamic restaking -> e.g. reduce restaking each day by 0.1 %
 -> can implement dynamic prices -> include an appreciation/depreciation/random(?) factor
'''

##########################   IMPORTS ##########################
import datetime
import csv
########################################################################################################################

def calcRewards(nbrTokenStaked, stakingPeriod, commission, compoundingShare, token):
    # start & end date for each emission schedule
    startDate = datetime.datetime(2022, 10, 13)    #datetime.datetime.now()
    endDate = 0
    currentStakingRewards = 0
    currentStakingPeriod = 0
    restakedRewards = 0
    stakingRewardsProfits = 0

    L0 = token.levelLinearization
    T0 = token.trendLinearization
    t = 1

    fileName = "stakingRewardsDataForcAPR.csv"
    f = open(fileName, 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    #writer.writerow(['sep=,'])
    writer.writerow(['Date', 'Token', 'stakingRewards', 'cumStakingRewards', 'APR', 'forcastTokenStaked'])

    ### INITIALIZATION ###
    # search for current epoch & set staking rewards accordingly for each token
    for j in range(len(token.inflationSchedule)):
        if startDate < token.inflationSchedule[j][1]:
            endDate = token.inflationSchedule[j][1]
            currentStakingRewards = token.inflationSchedule[j][0] * \
                                    token.inflationShareStaking / 100 + token.yearlyTxFees
            currentStakingPeriod = j
            break

    # how many epochs (= days) until the first epoch period ends
    epochsPerPeriod = (endDate - startDate).days

    for t in range(stakingPeriod):
        # check period & update staking rewards if necessary
        if epochsPerPeriod == 0:
            currentStakingPeriod += 1
            # check if token emission schedule is at end -> stop calculation!
            if currentStakingPeriod == len(token.inflationSchedule):
                print("No more staking rewards due to inflation")
                currentStakingRewards = token.yearlyTxFees
            else:
                currentStakingRewards = token.inflationSchedule[currentStakingPeriod][0] *\
                                           token.inflationShareStaking / 100 + token.yearlyTxFees
                epochsPerPeriod = 365  # each epoch period lasts 1 year

        epochsPerPeriod -= 1

        # dailyAPR = currentStakingRewards / token.totalStakedToken / 365
        forcastTokenStaked = L0 + T0 * t

        dailyAPR = currentStakingRewards / forcastTokenStaked / 365

        stakingRewards = nbrTokenStaked * dailyAPR * (1 - commission / 100)

        # update nbr of token staked, taking restaking/compounding into account
        nbrTokenStaked += stakingRewards * compoundingShare / 100

        # nbr of token that were compounded -> restaking
        restakedRewards += stakingRewards * compoundingShare / 100

        # nbr of token that were not compounded -> profit taking
        stakingRewardsProfits += stakingRewards * (1 - compoundingShare / 100)

        writer.writerow([startDate+datetime.timedelta(days=t) ,token.name, stakingRewards, (restakedRewards+stakingRewardsProfits), dailyAPR*36500, forcastTokenStaked])

    f.close()
    return [restakedRewards, stakingRewardsProfits]
########################################################################################################################

def convertPeriods(compPeriod):
    for p in range(4):
        if compPeriod == "daily":
            return 365
        elif compPeriod == "weekly":
            return 52
        elif compPeriod == "monthly":
            return 12
        else:
            return 1