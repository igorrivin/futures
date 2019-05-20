import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def midpoint(df):
    return(df.iloc[0].bidPrice+df.iloc[0].askPrice)/2
 
def myts(df):
    return df.iloc[0].timestamp

def mungdf(dfp):
    thets = dfp[0]
    df = dfp[1]
    midprice = midpoint(df)
    newdf = df.copy()
    newdf.bidPrice = newdf.bidPrice/midprice
    newdf.askPrice = newdf.askPrice/midprice
    newrow = np.append(np.ndarray.flatten(newdf.values), midprice)
    return thets, newrow

def mungdflist(dfl, offset=None):
    pairlist = [mungdf(i) for i in dfl]
    thedates = [i[0] for i in pairlist]
    theind = pd.DatetimeIndex(thedates)
    thevals = np.stack([i[1] for i in pairlist])
    mydf =  pd.DataFrame(thevals, index=theind)
    mydf = mydf.astype('float')
    if offset is None:
        newdf = mydf.resample('1T').mean()
    else:
        td = timedelta(seconds=datetime.now().second)
        mydf.index = mydf.index - td
        newdf=mydf.resample('1T', loffset=td).mean()
        #mydf.index = mydf.index + td
    return newdf

def makegain(df):
    return df[df.columns[-1]].pct_change().shift(-1)