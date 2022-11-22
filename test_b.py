import random
from random import randint
import b
from b import *

from pprint import pprint

def test1():
    print("Test 1\n")

    json_str = '{"m": 3, "tree": {"k": [3], "v": ["value3"], "c": [ {"k": [1,2], "v": ["value1", "value2"], "c": [null, null, null] },{"k": [4,5], "v": ["value4", "value5"], "c": [null, null, null] } ] } }'
    tree = load_tree(json_str)
    m = tree.m
    print(tree)
    print("\n")

    print(query(tree, 5))
    dump = dump_tree(tree)
    print(dump)
    print("\n")
    
    insert(tree, tree.m, 0, "value0")
    print(tree)
    print("\n")

def test2():
    print("\nTest 2\n")
    
    tree = None
    m = 4

    insert_trace0 = [(50, "top"), (30, "top left"), (70, "top right"), (20, "top left left")]
    for i in insert_trace0:
        tree = insert(tree, m, i[0], i[1])
        print(tree)
        print("\n")

    insert_trace1 = [(40, "new1"), (10, "new2"), (15, "new3")]
    for i in insert_trace1:
        tree = insert(tree, m, i[0], i[1])
        print(tree)
        print("\n")
    
    tree = delete(tree, 10)
    print(tree)
    print("\n")

    tree = insert(tree, m, 80, "new4")
    print(tree)
    print("\n")

    tree = delete(tree, 50)
    print(tree)
    print("\n")

    tree = insert(tree, m, 5, "new5")
    print(tree)
    print("\n")

    tree = delete(tree, 30)
    print(tree)
    print("\n")

    tree = delete(tree, 40)
    print(tree)
    print("\n")

    insert_trace1 = [(100, "new6"), (200, "new7"), (300, "new8"), (400, "new9"), (1, "new10"), (2, "new11"), (75, "new12"), (74, "new13")]
    for i in insert_trace1:
        tree = insert(tree, m, i[0], i[1])
    print(tree)
    print("\n")

def test3():
    print("\nTest3\n")
    
    json_str = '{"m": 3, "tree": {"k": [3], "v": ["value3"], "c": [ {"k": [1,2], "v": ["value1", "value2"], "c": [null, null, null] },{"k": [4,5], "v": ["value4", "value5"], "c": [null, null, null] } ] } }'
    tree = load_tree(json_str)
    print(tree)
    print("\n")

    insert_trace0 = [(0, "value0"), (7, "value7"), (6, "value6")]
    for i in insert_trace0:
        tree = insert(tree, tree.m, i[0], i[1])
        print(tree)
        print("\n")

    delete_trace0 = [5, 6, 7]
    for i in delete_trace0:
        tree = delete(tree, i)
        print(tree)
        print("\n")    

def test_baby23tree1():
    fname = r"C:\Users\danie\OneDrive\Documents\University of Maryland\Fall 2022\CMSC420\Project 3\starter_code\input\small_2-3_mixed.trace"
    data = trace_from_file(fname)

    m_val = data["m"]
    i_path = data['init_path']
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None
    print(tree)
    print("\n")

    insert_trace0 = [(0, "value0"), (7, "value7"), (6, "value6")]
    for i in insert_trace0:
        tree = insert(tree, m_val, i[0], i[1])
        print(tree)
        print("\n")

def test_baby23tree2():
    fname = r"C:\Users\danie\OneDrive\Documents\University of Maryland\Fall 2022\CMSC420\Project 3\starter_code\input\small_2-3_mixed.trace"
    data = trace_from_file(fname)

    m_val = data["m"]
    i_path = data['init_path']
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None
    print(tree)
    print("\n")

    delete_trace0 = [4, 3]
    for i in delete_trace0:
        tree = delete(tree, i)
        print(tree)
        print("\n")

def test_baby23tree3():
    fname = r"C:\Users\danie\OneDrive\Documents\University of Maryland\Fall 2022\CMSC420\Project 3\starter_code\input\small_2-3_mixed.trace"
    data = trace_from_file(fname)

    m_val = data["m"]
    i_path = data['init_path']
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None
    print(tree)
    print("\n")

    insert_trace0 = [(8, "value8"), (0, "value0"), (9, "value9"), (7, "value7")]
    for i in insert_trace0:
        tree = insert(tree, m_val, i[0], i[1])
    print(tree)
    print("\n")

    tree = delete(tree, 0)
    tree = insert(tree, m_val, 6, "value6")
    tree = delete(tree, 8)
    print(tree)
    print("\n")

    keychain = query(tree, 0)
    value = keychain.pop()
    print((0, keychain, value))
    print("\n")

def test_mounttree1():
    print("\nTest5\n")

    fname = r"C:\Users\danie\OneDrive\Documents\University of Maryland\Fall 2022\CMSC420\Project 3\starter_code\input\mount_mixed.trace"
    data = trace_from_file(fname)

    m_val = data["m"]
    i_path = data['init_path']
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None
    print(tree)

    insert_trace0 = [(5, "value5"), (14, "value14"), (1, "value1"), (18, "value18")]
    for i in insert_trace0:
        tree = insert(tree, tree.m, i[0], i[1])
        print(tree)
        print("\n")

    insert_trace1 = [(100, "value100"), (110, "value110"), (120, "value120"), (130, "value130")]
    for i in insert_trace1:
        tree = insert(tree, tree.m, i[0], i[1])
        print(tree)
        print("\n")

    insert_trace2 = [(82, "value82"), (69, "value69"), (60, "value60")]
    for i in insert_trace2:
        tree = insert(tree, tree.m, i[0], i[1])
        print(tree)
        print("\n")

    tree = delete(tree, 40)
    tree = insert(tree, tree.m, 40, None)
    print(tree)
    print("\n")

def test_scratchtree1():
    tree = None
    m_val = 3
    queryresults = []

    insert_trace0 = [(65, 100065), (37, 100037), (39, 100039), (36, 100036), (14, 100014), (39, 100039)]
    for i in insert_trace0:
        tree = insert(tree, m_val, i[0], i[1])
        print(tree)
        print("\n")

    keychain1 = query(tree, 14)
    value1 = keychain1.pop()
    queryresults.append((14, keychain1, value1))

    keychain2 = query(tree, 39)
    value2 = keychain2.pop()
    queryresults.append((39, keychain2, value2))
    print(queryresults)

def test_baby23tree4():
    fname = r"C:\Users\danie\OneDrive\Documents\University of Maryland\Fall 2022\CMSC420\Project 3\starter_code\input\small_2-3_mixed.trace"
    data = trace_from_file(fname)
    queryresults = []

    m_val = data["m"]
    i_path = data['init_path']
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None
    print(tree)
    print("\n")

    tree = delete(tree, 4)

    k = 2
    keychain = query(tree, k)
    value = keychain.pop()
    queryresults.append((k, keychain, value))

    k = 4
    keychain = query(tree, k)
    value = keychain.pop()
    queryresults.append((k, keychain, value))

    tree = delete(tree, 3)
    tree = delete(tree, 2)
    tree = delete(tree, 1)
    tree = delete(tree, 2)
    print(tree)
    print("\n")
    print(queryresults)
    print("\n")

def main():
    #test1()
    #test2()
    #test3()
    #test_baby23tree1()
    #test_baby23tree2()
    #test_baby23tree3()
    #test_mounttree1()
    #test_scratchtree1()
    test_baby23tree4()

main()


