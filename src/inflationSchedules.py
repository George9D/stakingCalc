import datetime

##### INFLATION / STAKING REWARDS SCHEDULE - token issued YEARLY to stakers #####
junoInflationSchedule = [(25961297, datetime.datetime(2022, 10, 24)),
                      (18172908, datetime.datetime(2023, 10, 24)),
                      (10903744, datetime.datetime(2024, 10, 24)),
                      (10794707, datetime.datetime(2025, 10, 24)),
                      (10458872, datetime.datetime(2026, 10, 24)),
                      (9883634, datetime.datetime(2027, 10, 24)),
                      (9064704, datetime.datetime(2028, 10, 24)),
                      (8007155, datetime.datetime(2029, 10, 24)),
                      (6726010, datetime.datetime(2030, 10, 24)),
                      (5246288, datetime.datetime(2031, 10, 24)),
                      (3602451, datetime.datetime(2032, 10, 24)),
                      (1837250, datetime.datetime(2033, 10, 24))]

evmosInflationSchedule = [(309375000, datetime.datetime(2023, 6, 1)),
                       (159375000, datetime.datetime(2024, 6, 1)),
                       (84375000, datetime.datetime(2025, 6, 1)),
                       (46875000, datetime.datetime(2026, 6, 1))]

atomInflationSchedule = []
totalAtom = 304610169
for i in range(10):
    atomInflationSchedule.append((totalAtom * (pow(1.126, i+1)-1), datetime.datetime(2023+i, 8, 10)))

sifchainInflationSchedule = []
totalRowan = 2330748000
for i in range(10):
    sifchainInflationSchedule.append((totalRowan * (pow(1.42, i+1)-1), datetime.datetime(2023+1, 8, 10)))

starsInflationSchedule = [(1000000000, datetime.datetime(2022, 12, 31)),
                        (666666666.7, datetime.datetime(2023, 12, 31)),
                        (444444444.4, datetime.datetime(2024, 12, 31)),
                        (296296296.3, datetime.datetime(2025, 12, 31)),
                        (197530864.2, datetime.datetime(2026, 12, 31)),
                        (131687242.8, datetime.datetime(2027, 12, 31)),
                        (87791495.19, datetime.datetime(2028, 12, 31)),
                        (58527663.46, datetime.datetime(2029, 12, 31)),
                        (39018442.3, datetime.datetime(2030, 12, 31)),
                        (26012294.87, datetime.datetime(2031, 12, 31))]

toriInflationSchedule =[(300000000, datetime.datetime(2023, 10, 6)),
                        (200000000, datetime.datetime(2024, 10, 6)),
                        (133000000, datetime.datetime(2025, 10, 6)),
                        (88666666, datetime.datetime(2026, 10, 6)),
                        (59111111, datetime.datetime(2027, 10, 6)),
                        (39407407, datetime.datetime(2028, 10, 6)),
                        (26271604, datetime.datetime(2029, 10, 6)),
                        (17514403, datetime.datetime(2030, 10, 6)),
                        (11676268, datetime.datetime(2031, 10, 6)),
                        (7784179, datetime.datetime(2032, 10, 6))]

osmosInflationSchedule = [(300000000, datetime.datetime(2022, 6, 19)),
                        (200000000, datetime.datetime(2023, 6, 19)),
                        (133000000, datetime.datetime(2024, 6, 19)),
                        (88666666, datetime.datetime(2025, 6, 19)),
                        (59111111, datetime.datetime(2026, 6, 19)),
                        (39407407, datetime.datetime(2027, 6, 19)),
                        (26271604, datetime.datetime(2028, 6, 19)),
                        (17514403, datetime.datetime(2029, 6, 19)),
                        (11676268, datetime.datetime(2030, 6, 19)),
                        (7784179, datetime.datetime(2031, 6, 19))]

# not sure if this is correct -> calculated on my own using graphs published on their wesite!
rebusInflationSchedule = [(115250000, datetime.datetime(2023, 10, 1)),
                        (67416928, datetime.datetime(2024, 10, 1)),
                        (47833071, datetime.datetime(2025, 10, 1)),
                        (37102212, datetime.datetime(2026, 10, 1)),
                        (30314715, datetime.datetime(2027, 10, 1)),
                        (25630726, datetime.datetime(2028, 10, 1)),
                        (22202345, datetime.datetime(2029, 10, 1)),
                        (19583856, datetime.datetime(2030, 10, 1)),
                        (17518356, datetime.datetime(2031, 10, 1)),
                        (15847281, datetime.datetime(2032, 10, 1)),
                        (14467434, datetime.datetime(2033, 10, 1)),
                        (13308749, datetime.datetime(2034, 10, 1)),
                        (12321977, datetime.datetime(2035, 10, 1)),
                        (11471486, datetime.datetime(2036, 10, 1)),
                        (10730858, datetime.datetime(2037, 10, 1))]