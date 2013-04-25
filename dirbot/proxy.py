#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def isPalindrome(n):
    s = str(n)
    return s == s[::-1]

def main():
    m1 = 1
    m2 = 10000000
    return [(i, i*i) for i in range(m1,m2) if isPalindrome(i) and isPalindrome(i*i)]

if __name__ == '__main__':
    import time
    
    st = time.time()
    print(main(), time.time() - st)