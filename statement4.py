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
    def playFor(aPerformance):
        play = plays[aPerformance['playID']]
        return play

    def amountFor(aPerformance, play):
        # extract function
        if playFor(aPerformance)['type'] == "tragedy":
            result = 40000
            if aPerformance['audience'] > 30:
                result += 1000 * (aPerformance['audience'] - 30)
        elif playFor(aPerformance)['type'] == "comedy":
            result = 30000
            if aPerformance['audience'] > 20:
                result += 10000 + 500 * (aPerformance['audience'] - 20)
                result += 300 * aPerformance['audience']
        else:
            raise ValueError(f"unknown type: {playFor(aPerformance)['type']}")
        return result

    totalAmount = 0
    volumeCredits = 0
    result = f"Statement for {invoice['customer']}\n"

    for perf in invoice['performances']:
        # add volume credits
        volumeCredits += max(perf['audience'] - 30, 0)
        # add extra credit for every five comedy attendees
        if "comedy" == playFor(perf)['type']:
            volumeCredits += round(perf['audience'] / 5)
        # print line for this order
        result += f"  {playFor(perf)['name']}: " \
                  f"{format_currency(amountFor(perf, playFor(perf)) / 100, 'USD', locale='en_US')} " \
                  f"({perf['audience']} seats)\n"
        totalAmount += amountFor(perf, playFor(perf))
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
