def createStatementData(invoice, plays):
    def enrichPerformance(aPerformance):

        def playFor(aPerformance):
            play = plays[aPerformance['playID']]
            return play

        calculator = PerformanceCalculator.create(
            aPerformance, playFor(aPerformance)
        )
        result = dict() | aPerformance
        result['play'] = calculator.play
        result['amount'] = calculator.amount
        result['volumeCredits'] = calculator.volumeCredit
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

    @classmethod
    def create(cls, aPerformance, aPlay):
        if aPlay['type'] == 'tragedy':
            return TragedyCalculator(aPerformance, aPlay)
        elif aPlay['type'] == 'comedy':
            return ComedyCalculator(aPerformance, aPlay)
        else:
            raise TypeError(f"unknown type: {aPlay['type']}")

    def __init__(self, aPerformance, aPlay):
        self.performance = aPerformance
        self.play = aPlay

    @property
    def amount(self):
        raise NotImplementedError

    @property
    def volumeCredit(self):
        result = 0
        result += max(self.performance['audience'] - 30, 0)
        return result


class TragedyCalculator(PerformanceCalculator):

    @property
    def amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):

    @property
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
            result += 300 * self.performance['audience']
        return result

    @property
    def volumeCredit(self):
        return super().volumeCredit + round(self.performance['audience'] / 5)


def totalAmount(data):
    result = sum(perf['amount'] for perf in data['performances'])
    return result


def totalVolumeCredits(data):
    result = sum(perf['volumeCredits'] for perf in data['performances'])
    return result
