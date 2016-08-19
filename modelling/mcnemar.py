def mcNemar(model1, model2, labels):
    """
    Compute the McNemar statistic for two classification models
    :param model1: list of predictions from model 1
    :param model2: list of predictions from model 2
    :param labels: list of class labels
    :return: statistic value, degrees of freedom
    """
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0

    df = len(labels)
    for i in range(df):
        p1 = model1[i]
        p2 = model2[i]
        l = labels[i]

        if p1 == p2 and p1 == l:
            n11 += 1
        elif p1 == l:
            n01 += 1
        elif p2 == l:
            n10 += 1
        else:
            n00 += 1

    result = (abs(n01 - n10) - 1) ** 2 / float(n01 + n10)

    return result, df

