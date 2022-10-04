t = int(input())
for r in range(t):
    n = int(input())
    buy = [] #buy
    sell = [] #sell
    stockprice = 0 #stock price
    for y in range(n):
        inputs = input().split()
        type = inputs[0]
        shares = int(inputs[1])
        price = int(inputs[-1])
        if type == "buy":
            while len(sell) > 0:
                order = sell[0]
                if price < order[0]:
                    break
                if shares >= order[1]:
                    shares -= order[1]
                    del sell[0]
                    stockprice = order[0]                  
                else:                    
                    order[1] -= shares
                    shares = 0
                    stockprice = order[0]                    
                if shares == 0:
                    break 
            if shares > 0:
                i = 0
                while i < len(buy) and price < buy[i][0]:
                    i += 1
                if i<len(buy) and price == buy[i][0]:
                    buy[i][1] += shares
                else:
                    buy.insert(i, [price, shares])  

        elif type == "sell":
            while len(buy) > 0:
                order = buy[0]
                if price > order[0]:
                    break
                if shares >= order[1]:
                    shares -= order[1]
                    del buy[0]
                    stockprice = price
                else:                    
                    order[1] -= shares
                    shares = 0
                    stockprice = price
                if shares == 0:
                    break
            if shares > 0:
                i = 0
                while i < len(sell) and price > sell[i][0]:
                    i += 1
                if i<len(sell) and price == sell[i][0]:
                    sell[i][1] += shares
                else:
                    sell.insert(i, [price, shares])
        if len(sell)==0:
            print('-',end=' ')
        else:
            print(sell[0][0],end=' ')
        if len(buy)==0:
            print('-',end=' ')
        else:
            print(buy[0][0],end=' ')
        if stockprice == 0:
            print('-')
        else:
            print(stockprice)
            

