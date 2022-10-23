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

    totalAmount = 0
    volumeCredits = 0
    result = f"Statement for {invoice['customer']}\n"

    for perf in invoice['performances']:
        play = plays[perf['playID']]
        if play['type'] == "tragedy":
            thisAmount = 40000
            if perf['audience'] > 30:
                thisAmount += 1000 * (perf['audience'] - 30)
        elif play['type'] == "comedy":
            thisAmount = 30000
            if perf['audience'] > 20:
                thisAmount += 10000 + 500 * (perf['audience'] - 20)
                thisAmount += 300 * perf['audience']
        else:
            raise ValueError(f"unknown type: {play['type']}")
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
    print(statement(invoice=INVOICE, plays=PLAYS))
