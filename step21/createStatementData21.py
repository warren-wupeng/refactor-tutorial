def createStatementData(invoice, plays):
    def enrichPerformance(aPerformance):

        def playFor(aPerformance):
            play = plays[aPerformance['playID']]
            return play

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

        result = dict() | aPerformance
        result['play'] = playFor(result)
        result['amount'] = amountFor(result)
        result['volumeCredits'] = volumeCreditFor(result)
        return result

    def totalAmount(data):
        result = sum(perf['amount'] for perf in data['performances'])
        return result

    def totalVolumeCredits(data):
        result = sum(perf['volumeCredits'] for perf in data['performances'])
        return result

    statementData = dict()
    statementData['customer'] = invoice['customer']
    statementData['performances'] = list(
        map(enrichPerformance, invoice['performances'])
    )
    statementData['totalAmount'] = totalAmount(statementData)
    statementData['totalVolumeCredits'] = totalVolumeCredits(statementData)
    return statementData
