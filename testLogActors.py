import pytest
from logActors import *
from threading import Thread
import subprocess as s
from subprocess import Popen
import os
import sys
from Queue import Queue, Empty

def pytest_namespace():
    return {'history_value' : 0, 'iterate' : 0}

@pytest.fixture(scope="module")
@pytest.fixture
def data():
    pytest.history_value = 0
    pytest.iterate = 0
     
@pytest.fixture(scope="module")
def proxy_and(request):
    log_and = Log_And.start()
    proxy = log_and.proxy()
    def fin():
        log_and.stop()
    request.addfinalizer(fin)
    return proxy

@pytest.fixture(scope="module")
def proxy_or(request):
    log_or = Log_Or.start()
    proxy = log_or.proxy()
    def fin():
        log_or.stop()
    request.addfinalizer(fin)
    return proxy

@pytest.fixture(scope="module")
def proxy_not(request):
    log_not = Log_Not.start()
    proxy = log_not.proxy()
    def fin():
        log_not.stop()
    request.addfinalizer(fin)
    return proxy

@pytest.fixture(scope="module")
def proxy_link(request):
    link = Link_Actor.start()
    proxy = link.proxy()
    def fin():
        link.stop()
    request.addfinalizer(fin)
    return proxy

def test_log_scheme(proxy_and, proxy_or, proxy_not, proxy_link, data):

    i = 3
    while (i):
        inp = raw_input()
        var = map(int, inp)
        y1_ideal = (not (var[0] and var[1])) or ((var[2] or var[3]) and (var[4] and var[5]))
        if (pytest.iterate):
            pytest.history_value = ((var[6] or var[7]) and pytest.history_value) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        else:
            pytest.history_value = (not (var[6] or var[7])) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        pytest.iterate += 1
        y1 = proxy_or.or_op(proxy_and.and_op(proxy_or.or_op(var[2], var[3]).get(), proxy_and.and_op(var[4], var[5]).get()).get(), proxy_not.not_op(proxy_and.and_op(var[0], var[1]).get()).get()).get()
        y2 = proxy_not.not_op(proxy_link.link(proxy_or.or_op(proxy_and.and_op(proxy_or.or_op(var[6], var[7]).get(), proxy_link.link().get()).get(), proxy_and.and_op(var[8], var[9]).get()).get()).get()).get()
        i -= 1    
        assert y1 == y1_ideal
        assert y2 == y2_ideal
         
def test_log_scheme_perl(proxy_and, proxy_or, proxy_not, data):
    ps = Popen(r'perl C:\Python27\komb.pl', stdin = s.PIPE, stdout = s.PIPE)
    i = 3
    ideal_list = []
    while (i):
        inp = raw_input()
        var = map(int, inp)
        ps.stdin.write(inp + '\n') 
        y1_ideal = (not (var[0] and var[1])) or ((var[2] or var[3]) and (var[4] and var[5]))
        if (pytest.iterate):
            pytest.history_value = ((var[6] or var[7]) and pytest.history_value) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        else:
            pytest.history_value = (not (var[6] or var[7])) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        pytest.iterate += 1
        i-=1
        ideal_list.append(int(y1_ideal))
        ideal_list.append(int(y2_ideal))

    ideal_list.reverse()
    for line in iter(ps.stdout.readline, b''):
        assert int(line[0]) == ideal_list.pop()
        assert int(line[1]) == ideal_list.pop()
      
def test_log_scheme_c(proxy_and, proxy_or, proxy_not, data):   
    ps = Popen(r'C:\Python27\org_comp_c.exe', stdin = s.PIPE, stdout = s.PIPE)
    i = 3
    ideal_list = []
    while (i):
        inp = raw_input()
        var = map(int, inp)
        ps.stdin.write(inp + '\n') 
        y1_ideal = (not (var[0] and var[1])) or ((var[2] or var[3]) and (var[4] and var[5]))
        if (pytest.iterate):
            pytest.history_value = ((var[6] or var[7]) and pytest.history_value) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        else:
            pytest.history_value = (not (var[6] or var[7])) or (var[8] and var[9])
            y2_ideal = not pytest.history_value
        pytest.iterate += 1
        i-=1
        ideal_list.append(int(y1_ideal))
        ideal_list.append(int(y2_ideal))

    ideal_list.reverse()
    for line in iter(ps.stdout.readline, b''):
        assert int(line[0]) == ideal_list.pop()
        assert int(line[1]) == ideal_list.pop()
    

