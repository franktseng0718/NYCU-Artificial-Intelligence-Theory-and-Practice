import numpy as np

def F1(t):
    return 0.063*(t**3) - 5.284*(t**2) + 4.887*t + 412 + np.random.normal(0, 1)

def F2(t, A, B, C, D):
    return A*(t**B) + C*np.cos(D*t) + np.random.normal(0, 1, t.shape)

def gene2coef(gene):
    A = (np.sum(2**np.arange(10)*gene[0:10]) - 511) / 100   #-5.11 - 5.12
    B = (np.sum(2**np.arange(10)*gene[10:20]) - 511) / 100   #-511 - 512
    C = (np.sum(2**np.arange(10)*gene[20:30]) - 511)    #-5.11 - 5.12
    D = (np.sum(2**np.arange(10)*gene[30:40]) - 511) / 100   #-5.11 - 5.12
    return A, B, C, D

def plot_error1D(input, error):
    pass
def plot_error2D(input1, input2, error):
    pass
def solvelp():
    A = np.zeros((1000, 5))
    b = np.zeros((1000, 1))
    for t in range(0, 1000):
        b[t] = F1(t)
        A[t, 0] = t ** 4
        A[t, 1] = t ** 3
        A[t, 2] = t ** 2
        A[t, 3] = t
        A[t, 4] = 1

    x = np.linalg.lstsq(A, b)[0]

    print(x)

def gene_algo():

    T = np.random.random((1000, 1))*100
    b2 = F2(T, 0.6, 1.2, 100, 0.4)

    N = 10000
    G = 30
    survive_rate = 0.05
    mutation_rate = 0.001
    survive = round(N*survive_rate)
    mutation = round(N*40*mutation_rate)

    pop = np.random.randint(0, 2, (N, 40))
    fit = np.zeros((N, 1))

    for generation in range(G):
        # Fitness
        for i in range(N):
            A, B, C, D = gene2coef(pop[i, :])
            fit[i] = np.mean(abs(F2(T, A, B, C, D) - b2))
        
        #selection
        sortf = np.argsort(fit[:, 0])
        pop = pop[sortf, :]
        for i in range(survive, N):
            fid = np.random.randint(0, survive)
            mid = np.random.randint(0, survive)
            while(fid==mid):
                mid = np.random.randint(0, survive) # mother should different from father
            mask = np.random.randint(0, 2, [1, 40])
            son = pop[mid, :].copy()
            father = pop[fid, :]
            son[mask[0, :]==1] = father[mask[0, :]==1]   # crossover
            pop[i, :] = son
        
        # mutation
        for i in range(mutation):
            m = np.random.randint(survive, N)
            n = np.random.randint(0, 40)
            pop[m, n] = 1 - pop[m, n]

    # Fitness
    for i in range(N):
        A, B, C, D = gene2coef(pop[i, :])
        fit[i] = np.mean(abs(F2(T, A, B, C, D) - b2))
    sortf = np.argsort(fit[:, 0])
    pop = pop[sortf, :]

    A, B, C, D = gene2coef(pop[0, :])
    print(A, B, C, D)