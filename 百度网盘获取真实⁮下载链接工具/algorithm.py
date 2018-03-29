#!/usr/bin/python3
# coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

import datetime
import os
import re
from pyquery import PyQuery as pq
import pymysql.cursors
import requests

def sign2(j, r):
    a = [];
    p = [];
    o = "";
    v = len(j)
    for q in range(0, 256):
        z = q % v;
        js = j[z:z + 1];
        jc = ord(js[0]);
        a.append(jc);
        p.append(q);
        
    for q in range(0, 256):
        if q == 0:
            u = 0

        u = (u + p[q] + a[q]) % 256;
        t = p[q];
        p[q] = p[u];
        p[u] = t;
    i = 0
    while i < len(r):
        if i == 0:
            u, q = 0, 0
        i = (i + 1) % 256;
        u = (u + p[i]) % 256;
        t = p[i];
        p[i] = p[u];
        p[u] = t;
        k = p[(p[i] + p[u]) % 256];
        kr = ord(r[q]) ^ k;
        o += chr(kr)
        q += 1
    return o;


def base64_baidu(sign_old):
    C = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    length = len(sign_old);
    # print(length);
    A = 0;
    B = "";
    while (A < length):
        F = ord(sign_old[A]) & 255;
        A += 1
        if (A == length):
            B += C[F >> 2];
            B += C[(F & 3) << 4];
            B += "==";
            break;
        D = ord(sign_old[A]);
        A += 1
        if (A == length):
            B += C[F >> 2];
            B += C[((F & 3) << 4) | ((D & 240) >> 4)];
            B += C[(D & 15) << 2];
            B += "=";
            break;
        E = ord(sign_old[A]);
        A += 1
        B += C[F >> 2]
        # print('---', str((F & 3)), str(0 << 4))
        B += C[((F & 3) << 4) | ((D & 240) >> 4)];
        B += C[((D & 15) << 2) | ((E & 192) >> 6)];
        B += C[E & 63];
    return B;
    pass
