from babel.numbers import format_currency

from step21.createStatementData21 import createStatementData

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
    return renderPlainText(createStatementData(invoice, plays))


def renderPlainText(data):

    result = f"Statement for {data['customer']}\n"
    for perf in data['performances']:
        # print line for this order
        result += f"  {perf['play']['name']}: " \
                  f"{usd(perf['amount'])} " \
                  f"({perf['audience']} seats)\n"

    result += f"Amount owed is " \
              f"{usd(data['totalAmount'])}\n"
    result += f"You earned {data['totalVolumeCredits']} credits\n"
    return result


def usd(aNumber):
    return format_currency(aNumber / 100, 'USD', locale='en_US')


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
