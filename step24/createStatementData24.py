def createStatementData(invoice, plays):
    def enrichPerformance(aPerformance):

        def playFor(aPerformance):
            play = plays[aPerformance['playID']]
            return play

        def amountFor(aPerformance):
            return PerformanceCalculator(aPerformance, playFor(aPerformance)).amount

        def volumeCreditFor(aPerformance):
            # add volume credits
            result = 0
            result += max(aPerformance['audience'] - 30, 0)
            # add extra credit for every five comedy attendees
            if "comedy" == aPerformance['play']['type']:
                result += round(aPerformance['audience'] / 5)
            return result

        calculator = PerformanceCalculator(aPerformance, playFor(aPerformance))
        result = dict() | aPerformance
        result['play'] = calculator.play
        result['amount'] = amountFor(result)
        result['volumeCredits'] = volumeCreditFor(result)
        return result

    statementData = dict()
    statementData['customer'] = invoice['customer']
    statementData['performances'] = list(
        map(enrichPerformance, invoice['performances'])
    )
    statementData['totalAmount'] = totalAmount(statementData)
    statementData['totalVolumeCredits'] = totalVolumeCredits(statementData)
    return statementData


class PerformanceCalculator:
    # step24 move amount calculation logic to PerformanceCalculator

    def __init__(self, aPerformance, aPlay):
        self.performance = aPerformance
        self.play = aPlay

    @property
    def amount(self):

        if self.play['type'] == "tragedy":
            result = 40000
            if self.performance['audience'] > 30:
                result += 1000 * (self.performance['audience'] - 30)
        elif self.play['type'] == "comedy":
            result = 30000
            if self.performance['audience'] > 20:
                result += 10000 + 500 * (self.performance['audience'] - 20)
                result += 300 * self.performance['audience']
        else:
            raise ValueError(f"unknown type: {self.play['type']}")
        return result


def totalAmount(data):
    result = sum(perf['amount'] for perf in data['performances'])
    return result


def totalVolumeCredits(data):
    result = sum(perf['volumeCredits'] for perf in data['performances'])
    return result
