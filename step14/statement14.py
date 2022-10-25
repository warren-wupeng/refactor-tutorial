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
    # step14 move playFor to enrichPerformance
    def enrichPerformance(aPerformance):
        def playFor(aPerformance):
            play = plays[aPerformance['playID']]
            return play

        result = dict() | aPerformance
        result['play'] = playFor(result)
        return result

    statementData = dict()
    statementData['customer'] = invoice['customer']
    statementData['performances'] = list(
        map(enrichPerformance, invoice['performances'])
    )

    return renderPlainText(statementData, plays)


def renderPlainText(data, plays):

    def amountFor(aPerformance):
        # extract function
        play = aPerformance['play']
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

    def volumeCreditFor(aPerformance):
        # add volume credits
        result = 0
        result += max(aPerformance['audience'] - 30, 0)
        # add extra credit for every five comedy attendees
        if "comedy" == aPerformance['play']['type']:
            result += round(aPerformance['audience'] / 5)
        return result

    def usd(aNumber):
        return format_currency(aNumber / 100, 'USD', locale='en_US')

    def totalVolumeCredits():
        result = 0
        for perf in data['performances']:
            result += volumeCreditFor(perf)
        return result

    def totalAmount():
        result = 0
        for perf in data['performances']:
            result += amountFor(perf)
        return result

    result = f"Statement for {data['customer']}\n"
    for perf in data['performances']:
        # print line for this order
        result += f"  {perf['play']['name']}: " \
                  f"{usd(amountFor(perf))} " \
                  f"({perf['audience']} seats)\n"
    result += f"Amount owed is " \
              f"{usd(totalAmount())}\n"
    result += f"You earned {totalVolumeCredits()} credits\n"
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
