from random import randint


def agreement_rate(pis:list):
    p = sum(pis)
    ar = 0
    for pi in pis:
        ar += 0.5* pi *(pi-1)
    return ar/(0.5*p*(p-1))

def agreement_score(pis:list):
    p = sum(pis)
    ar = 0
    for pi in pis:
        ar += (pi/p)**2
    return ar

def max_consensus(pis:list):
    p = sum(pis)
    return max(pis)/p


def consensus(pis:list):
    p = sum(pis)
    denominator = 0
    tau = 0.5
    delta= lambda i,j: 50#1 if i == j else 0
    for len in pis:
        for i in range(len):
            for j in range(i, len):
                denominator += delta(i,j) if delta(i,j) <= tau else 0
    return denominator/(0.5*p*(p-1))







def get_pi_values(p:int):
    pis = []
    while sum(pis) < p:
        rand_float = randint(1, p)
        if sum(pis) + rand_float <= p:
            pis.append(rand_float)
    if sum(pis) != p:
        pis.append(p-sum(pis))
    assert sum(pis) == p
    return pis

def evaluation(f):
    print(f.__name__,":", end="\t")
    maxv = -100
    minv = 100
    for p in range(2,1000):
        for times in range(5000):
            pis = get_pi_values(p)
            maxv = max(maxv, f(pis))
            minv = min(minv, f(pis))
    print("von", minv, "bis", maxv)


if __name__ == "__main__":
    evaluation(f=agreement_rate)
    evaluation(f=agreement_score)
    evaluation(f=max_consensus)

    evaluation(f=consensus)