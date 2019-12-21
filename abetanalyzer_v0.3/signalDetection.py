from __future__ import division
from scipy.stats import norm
from math import exp, sqrt
import decimal
from scipy import stats
Z = norm.ppf

def signalDetection1(hits, misses, CRs, FAs):
    hits = int(hits)
    misses = int(misses)
    CRs = int(CRs)
    FAs = int(FAs)
    try:
        HR = hits / (hits + misses)
    except ZeroDivisionError:
        HR = 0
    try:
        FAR = FAs / (FAs + CRs)
    except ZeroDivisionError:
        FAR = 0

    # Avoid d' infinity
    if HR == 1:
        HR = (hits - 0.5) / (hits + misses)
    if HR == 0:
        if (hits + misses) > 0:
            HR = (hits + 0.5) / (hits + misses)
        else:
            HR = 0
    if FAR == 1:
        FAR = (FAs - 0.5) / (FAs + CRs)
    if FAR == 0:
        if (FAs + CRs) > 0:
            FAR = (FAs + 0.5) / (FAs + CRs)
        else:
            FAR = 0

    if (FAR != 0) and (HR != 0):
        try:
            d = (Z(HR) - Z(FAR))
        except (ZeroDivisionError):
            d = 0
        try:
            criterion = (-(Z(HR) + Z(FAR)) / 2)
        except (ZeroDivisionError):
            criterion = 0
        try:
            beta = (exp((Z(FAR) ** 2 - Z(HR) ** 2) / 2))
        except (ZeroDivisionError):
            beta = 0
        try:
            SI = ((HR - FAR) / (2 * (HR + FAR) - (HR + FAR) ** 2))
        except (ZeroDivisionError):
            SI = 0
        try:
            RI = ((HR - FAR - 1) / 1 - ((HR - FAR) ** 2))
        except (ZeroDivisionError):
            RI = 0
        HR = round(HR, 2)
        FAR = round(FAR, 2)
        d = round(d, 2)
        criterion = round(criterion, 2)
        beta = round(beta, 2)
        SI = round(SI, 2)
        RI = round(RI, 2)
    else:
        HR = FAR = d = criterion = beta = SI = RI = 0
    
    return HR, FAR, d, criterion, beta, SI, RI


def signalDetection2(hits, misses, CR_corrected, FAs_corrected):
    hits = int(hits)
    misses = int(misses)
    CR_corrected = int(CR_corrected)
    FAs_corrected = int(FAs_corrected)
    try:
        HR_corrected = hits / (hits + misses)
    except ZeroDivisionError:
        HR_corrected = 0
    try:
        FAR_corrected = FAs_corrected / (FAs_corrected + CR_corrected)
    except ZeroDivisionError:
        FAR_corrected = 0

    # Avoid d' infinity
    if HR_corrected == 1:
        HR_corrected = (hits - 0.5) / (hits + misses)
    if HR_corrected == 0:
        if (hits + misses) > 0:
            HR_corrected = (hits + 0.5) / (hits + misses)
        else:
            HR_corrected = 0
    if FAR_corrected == 1:
        FAR_corrected = (FAs - 0.5) / (FAs_corrected + CR_corrected)
    if FAR_corrected == 0:
        if (FAs_corrected + CR_corrected) > 0:
            FAR_corrected = (FAs_corrected + 0.5) / (FAs_corrected + CR_corrected)
        else:
            FAR_corrected = 0

    if (FAR_corrected != 0) and (HR_corrected != 0):
        try:
            d_corrected = (Z(HR_corrected) - Z(FAR_corrected))
        except (ZeroDivisionError):
            d_corrected = 0
        try:
            c_corrected = (-(Z(HR_corrected) + Z(FAR_corrected)) / 2)
        except (ZeroDivisionError):
            c_corrected = 0
        try:
            beta_corrected = (exp((Z(FAR_corrected) ** 2 - Z(HR_corrected) ** 2) / 2))
        except (ZeroDivisionError):
            beta_corrected = 0
        try:
            SI_corrected = ((HR_corrected - FAR_corrected) / (2 * (HR_corrected + FAR_corrected) - (HR_corrected + FAR_corrected) ** 2))
        except (ZeroDivisionError):
            SI_corrected = 0
        try:
            RI_corrected = ((HR_corrected - FAR_corrected - 1) / 1 - ((HR_corrected - FAR_corrected) ** 2))
        except (ZeroDivisionError):
            RI_corrected = 0
        HR_corrected = round(HR_corrected, 2)
        FAR_corrected = round(FAR_corrected, 2)
        d_corrected = round(d_corrected, 2)
        c_corrected = round(c_corrected, 2)
        beta_corrected = round(beta_corrected, 2)
        SI_corrected = round(SI_corrected, 2)
        RI_corrected = round(RI_corrected, 2)
    else:
        HR_corrected = FAR_corrected = d_corrected = c_corrected = beta_corrected = SI_corrected = RI_corrected = 0

    return HR_corrected, FAR_corrected, d_corrected, c_corrected, beta_corrected, SI_corrected, RI_corrected
