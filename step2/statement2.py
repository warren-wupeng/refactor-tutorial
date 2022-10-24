from babel.numbers import format_currency

PLAYS = {
  "hamlet": {"name": "Hamlet", "type": "tragedy"},
  "as-like": {"name": "As You Like It", "type": "comedy"},
  "othello": {"name": "Othello", "type": "tragedy"}
}

INVOICE = {
   "customer": "BigCo",
   "performances": [
     {"playID": "hamlet", "audience": 55},
     {"playID": "as-like", "audience": 35},
     {"playID": "othello", "audience": 40}
   ]
}


def statement(invoice, plays):
    # step2 移除变量play
    # 使用手法1: 提取方法
    # 使用手法2：以查询代替临时变量
    def amountFor(aPerformance, play):
        # extract function
        if play['type'] == "tragedy":
            result = 40000
            if aPerformance['audience'] > 30:
                result += 1000 * (aPerformance['audience'] - 30)
        elif play['type'] == "comedy":
            result = 30000
            if aPerformance['audience'] > 20:
                result += 10000 + 500 * (aPerformance['audience'] - 20)
                result += 300 * aPerformance['audience']
        else:
            raise ValueError(f"unknown type: {play['type']}")
        return result

    totalAmount = 0
    volumeCredits = 0
    result = f"Statement for {invoice['customer']}\n"

    for perf in invoice['performances']:
        play = plays[perf['playID']]
        thisAmount = amountFor(perf, play)
        # add volume credits
        volumeCredits += max(perf['audience'] - 30, 0)
        # add extra credit for every five comedy attendees
        if "comedy" == play['type']:
            volumeCredits += round(perf['audience'] / 5)
        # print line for this order
        result += f"  {play['name']}: " \
                  f"{format_currency(thisAmount/100, 'USD', locale='en_US')} " \
                  f"({perf['audience']} seats)\n"
        totalAmount += thisAmount
    result += f"Amount owed is " \
              f"{format_currency(totalAmount/100, 'USD', locale='en_US')}\n"
    result += f"You earned {volumeCredits} credits\n"
    return result


if __name__ == '__main__':
    aStatement = statement(invoice=INVOICE, plays=PLAYS)
    expected = """Statement for BigCo
  Hamlet: $650.00 (55 seats)
  As You Like It: $580.00 (35 seats)
  Othello: $500.00 (40 seats)
Amount owed is $1,730.00
You earned 47 credits
"""
    assert aStatement == expected, f"{aStatement}!={expected}"