# coding: utf-8
import math


def log(base, x): #対数
    """対数"""
    return math.log(x, base)


def permutation(n,r): #順列
    """順列"""
    if n<0 or r<0:
        raise ValueError("negative numbers.")
    if n<r:
        raise ValueError("r is bigger than n.")
    return math.factorial(n) / (math.factorial(n-r))


def combination(n,r): #組合せ
    """組合せ"""
    if n<0 or r<0:
        raise ValueError("negative numbers.")
    if n<r:
        raise ValueError("r is bigger than n.")
    return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))


def product(iterable): #積
    """総乗"""
    ans = 1.0
    for num in iterable:
        ans *= num
    return ans


def prime_factorization(num, mode='flat'): #素因数分解
    """素因数分解した答を返す"""
    if num<1:
        raise ValueError("smaller than 1.")
    factors = []
    for i in range(2, int(math.sqrt(num))+1):
        while num % i == 0:
            factors.append(i)
            num //= i
        if num==1: break
    else:
        factors.append(num)
    if mode=='pow': #(因数,指数)の形を返す
        return [(i, factors.count(i)) for i in set(factors)]
    elif mode=='unique': #一意な値のみを返す
        return list(set(factors))
    else: #全ての数を返す
        return factors


def dimension_reduction(iterables, depth=1): #次元削減
    """多次元リストを次元削減をしたものを返す"""
    if depth==0:
        return iterables
    _iterables = []
    for iterable in iterables:
        _iterables += iterable
    return dimension_reduction(_iterables, depth-1)


def lcm(iterable): #最小公倍数
    """最小公倍数を返す"""
    _iterables = [prime_factorization(i) for i in iterable]
    uniques = set(dimension_reduction(_iterables))
    factors = [unique ** max([_iterable.count(unique)\
         for _iterable in _iterables]) for unique in uniques]
    return product(factors)


def gcd(iterable): #最大公約数
    """最大公約数を返す"""
    _iterables = [prime_factorization(i) for i in iterable]
    uniques = set(dimension_reduction(_iterables))
    factors = [unique ** min([_iterable.count(unique)\
         for _iterable in _iterables]) for unique in uniques]
    return product(factors)
