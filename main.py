import getPEData
import getZZ800Data
import stock_strategy

if __name__=='__main__':
    getPEData.getPEData()
    getZZ800Data.getZZ800List() 
    getPEData.drewPEDateLines()
    stock_strategy.MAAvgSystem()