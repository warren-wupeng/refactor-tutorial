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


def htmlStatement(invoice, plays):
    return renderHtml(createStatementData(invoice, plays))


def renderHtml(data):
    result = f"<h1>Statement for {data['customer']}<h1>\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"
    for perf in data['performances']:
        result += f"<tr>" \
                  f"<td>{perf['play']['name']}</td><td>{perf['audience']}</td> "
        result += f"<td>{usd(perf['amount'])}</td></tr>\n"
    result += "</table>\n"
    result += f"<p>Amount owed is <em>{usd(data['totalAmount'])}</em></p>\n"
    result += f"<p>" \
              f"You earned <em>{data['totalVolumeCredits']}</em> credits</p>\n"
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
    aHtmlStatement = htmlStatement(invoice=INVOICE, plays=PLAYS)
    expectedHtml = """<h1>Statement for BigCo<h1>
<table>
<tr><th>play</th><th>seats</th><th>cost</th></tr>
<tr><td>Hamlet</td><td>55</td> <td>$650.00</td></tr>
<tr><td>As You Like It</td><td>35</td> <td>$580.00</td></tr>
<tr><td>Othello</td><td>40</td> <td>$500.00</td></tr>
</table>
<p>Amount owed is <em>$1,730.00</em></p>
<p>You earned <em>47</em> credits</p>
"""
    assert aHtmlStatement == expectedHtml, f"{aHtmlStatement}!={expected}"
