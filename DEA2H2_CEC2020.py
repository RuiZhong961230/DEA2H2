from copy import deepcopy
import os
from scipy.stats import levy
from opfunu.cec_based.cec2020 import *


DimSize = 10
PopSize = 100
Func_num = 1
Pop = np.zeros((PopSize, DimSize))
FitPop = np.zeros(PopSize)

MaxFEs = 1000 * DimSize
curIter = 0
MaxIter = int(MaxFEs / PopSize)
LB = [-100] * DimSize
UB = [100] * DimSize
Cr = 0.7
Trials = 30
BestIndi = np.zeros(DimSize)
FitBest = float("inf")



def InitialPop(func):
    global PopSize, DimSize, Pop, FitPop, BestIndi, FitBest, Success
    Pop = np.zeros((PopSize, DimSize))
    FitPop = np.zeros(PopSize)
    for i in range(PopSize):
        for j in range(DimSize):
            Pop[i][j] = LB[j] + np.random.rand() * (UB[j] - LB[j])
        FitPop[i] = func(Pop[i])
    best_idx = np.argmin(FitPop)
    FitBest = FitPop[best_idx]
    BestIndi = deepcopy(Pop[best_idx])


def LocalSearch1(Off, i):
    global DimSize, Pop, FitPop, BestIndi
    for j in range(DimSize):
        Off[i][j] = Pop[i][j] + np.random.uniform(-1, 1)
    Off[i] = np.clip(Off[i], LB, UB)


def LocalSearch2(Off, i):
    global DimSize, Pop, FitPop, BestIndi
    for j in range(DimSize):
        Off[i][j] = Pop[i][j] + np.random.normal(0, 1)
    Off[i] = np.clip(Off[i], LB, UB)


def LevyFlight(Off, i):
    global DimSize, Pop, FitPop, BestIndi
    for j in range(DimSize):
        Off[i][j] = Pop[i][j] + levy.rvs()
    Off[i] = np.clip(Off[i], LB, UB)


def DEbest(Off, i):
    global DimSize, Pop, FitPop, BestIndi, PopSize
    r1, r2 = np.random.choice(list(range(PopSize)), 2, replace=False)
    Off[i] = BestIndi + np.random.rand() * (Pop[r1] - Pop[r2])
    Off[i] = np.clip(Off[i], LB, UB)


def DErand(Off, i):
    global DimSize, Pop, FitPop, PopSize
    r1, r2, r3 = np.random.choice(list(range(PopSize)), 3, replace=False)
    Off[i] = Pop[r1] + np.random.rand() * (Pop[r1] - Pop[r2])
    Off[i] = np.clip(Off[i], LB, UB)


def DEcur2best(Off, i):
    global DimSize, Pop, FitPop, BestIndi, PopSize
    candi = list(range(PopSize))
    candi.remove(i)
    r1, r2 = np.random.choice(candi, 2, replace=False)
    Off[i] = Pop[i] + np.random.rand() * (BestIndi - Pop[i]) + np.random.rand() * (Pop[r1] - Pop[r2])
    Off[i] = np.clip(Off[i], LB, UB)


def BinBest(Off, i):
    global DimSize, Pop, FitPop, PopSize, BestIndi, Cr
    jrand = np.random.randint(0, DimSize)
    for j in range(DimSize):
        if np.random.rand() < Cr and j != jrand:
            Off[i][j] = Pop[i][j]
        else:
            Off[i][j] = BestIndi[j]


def BinRand(Off, i):
    global DimSize, Pop, FitPop, PopSize, Cr
    jrand = np.random.randint(0, DimSize)
    idx = np.random.randint(0, PopSize)
    while idx == i:
        idx = np.random.randint(0, PopSize)
    for j in range(DimSize):
        if np.random.rand() < Cr and j != jrand:
            Off[i][j] = Pop[idx][j]
        else:
            Off[i][j] = BestIndi[j]


def ExpoBest(Off, i):
    global DimSize, Pop, FitPop, PopSize, Cr, BestIndi
    Off[i] = deepcopy(Pop[i])
    jstart = np.random.randint(0, DimSize - 1)
    Off[i][jstart] = BestIndi[jstart]
    jstart += 1
    while jstart < DimSize and np.random.rand() < Cr:
        Off[i][jstart] = BestIndi[jstart]
        jstart += 1


def ExpoRand(Off, i):
    global DimSize, Pop, FitPop, PopSize, Cr, BestIndi
    Off[i] = deepcopy(Pop[i])
    idx = np.random.randint(0, PopSize)
    while idx == i:
        idx = np.random.randint(0, PopSize)
    jstart = np.random.randint(0, DimSize - 1)
    Off[i][jstart] = Pop[idx][jstart]
    jstart += 1
    while jstart < DimSize and np.random.rand() < Cr:
        Off[i][jstart] = Pop[idx][jstart]
        jstart += 1



Operators = [LocalSearch1, LocalSearch2, LevyFlight, DErand, DEbest, DEcur2best, BinBest, BinRand, ExpoBest, ExpoRand]
OperNum = len(Operators)
Success = np.random.randint(0, OperNum, PopSize)

def DEAH(func):
    global PopSize, DimSize, curIter, MaxIter, Pop, FitPop, BestIndi, FitBest, Success, OperNum, Operators

    InitialPop(func)
    Off = np.zeros((PopSize, DimSize))
    FitOff = np.zeros(PopSize)

    Trace = []
    for i in range(MaxIter):
        for j in range(PopSize):
            Search = Operators[Success[j]]
            Search(Off, j)
            FitOff[j] = func(Off[j])
            if FitOff[j] < FitPop[j]:
                FitPop[j] = FitOff[j]
                Pop[j] = deepcopy(Off[j])
                if FitOff[j] < FitBest:
                    BestIndi = deepcopy(Off[j])
                    FitBest = FitOff[j]
            else:
                Success[j] = np.random.randint(0, OperNum)
        Trace.append(FitBest)
    return Trace


def main(dim):
    global DimSize, LB, UB, MaxFEs, MaxIter, Trials
    DimSize = dim
    LB = [-100] * dim
    UB = [100] * dim

    PopSize = 100
    MaxFEs = 1000 * dim
    MaxIter = int(MaxFEs / PopSize)

    CEC2020 = [F12020(dim), F22020(dim), F32020(dim), F42020(dim), F52020(dim),
               F62020(dim), F72020(dim), F82020(dim), F92020(dim), F102020(dim)]

    for i in range(len(CEC2020)):
        All_Trial_Best = []
        for j in range(Trials):
            np.random.seed(2024 + 88 * j)
            Trace = DEAH(CEC2020[i].evaluate)
            All_Trial_Best.append(Trace)
        np.savetxt("./DEAH_Data/CEC2020/F" + str(i + 1) + "_" + str(dim) + "D.csv", All_Trial_Best, delimiter=",")


if __name__ == "__main__":
    if os.path.exists('DEAH_Data/CEC2020') == False:
        os.makedirs('DEAH_Data/CEC2020')
    Dims = [10, 30, 50, 100]
    for dim in Dims:
        main(dim)

