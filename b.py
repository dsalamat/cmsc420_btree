# I hate __future__ imports but this helps
# if you want to annotate that a class contains
# pointers to  instances of itself
from __future__ import annotations
from math import ceil, floor
from typing import Union, Tuple, List

# basic utilities
import json
import csv
import argparse

# feel free to import other stuff if you'd like. Of course the standard libraries 
# are available, but others may or may not be in the autograder.

###############################################################################
#### B-tree node class ########################################################
###############################################################################
"""This class is mostly unfilled to give you room to design it how you'd like
as it effects how you write the rest of your methods. A good place to start 
if you're unsure is the Java pseudo code definition from David Mount's notes"""
class BNode():
    def  __init__(self,
                  m : int,
                  keys : list,
                  values : list,
                  children : list,
                  ): 
        self.m = m
        self.keys = keys
        self.values = values
        self.children = children

    #__str__ method optional for grading, but required for visualizing
    def __str__(self):
        if self is None:
            return "None"
        else:
            curr = f"[m: {self.m}, keys: {self.keys}, values: {self.values} children:\n"
            for i in self.children:
                curr += str(i) + '\n'
            curr += ']'
            return curr



###############################################################################
#### I/O utils ################################################################
###############################################################################

""" This function needs to be completed to enable your main method to properly
    dump/load the trees to/from a json string representation. The recursive 
    function setup is based on the similarly named methods from previous 
    homework, so if the comments below aren't clear, take a look at those. 
    These are required during main execution but they also might be helpful in 
    parsing the autograder's test case dumps if you want to 
    use them for debugging """

def load_tree(json_str: str) -> BNode:
    """ Loads a tree of BNodes from a json string representation 
        using a driver-recursor pattern on an intermediate dict 
        representatation """

    m = None
    
    def _from_dict(dict_repr) -> BNode:

        if dict_repr == None or dict_repr == {}:
            return None
        return BNode(
            m,
            dict_repr["k"],
            dict_repr["v"],
            [_from_dict(i) for i in dict_repr["c"]]
        )
    
    try:
        # create the intermediate dict representation
        # and unpack the top keys
        dict_repr = json.loads(json_str)
        if "m" in dict_repr:
            m = dict_repr["m"]
        if "tree" in dict_repr:
            tree = dict_repr["tree"]
        else:
            tree = dict_repr
    except Exception as e:
        print(f"Exception encountered parsing the json string: {json_str}")
        raise e

    # call the recursor to turn the nested dict into a tree of BNodes
    root = _from_dict(tree)
    return root


def dump_tree(root: BNode) -> str:
    """ Dumps a tree of BNodes to a json string by using an intermediate dict
        representation, and driver-recursor pattern """
    
    def _to_dict(node) -> dict:
        if node is None:
            return {}
        return {
            "k" : node.keys,
            "v" : node.values,
            "c" : [_to_dict(i) for i in node.children]
        }
    
    # create the intermediate dict representation
    # and pack in the top keys
    if root == None:
        dict_repr = {}
    else:
        # call the recursor to turn the BNode tree into a nested dict
        dict_repr = _to_dict(root)
        dict_repr = {"m":root.m, "tree": dict_repr}

    return json.dumps(dict_repr, indent=4)


""" Do not modify these functions, as they define the trace schema by 
    implementing parsing for you, and returns a format that the main method 
    will expect. It includes assertions and error handling to help when a 
    tracefile is malformed - I hope this bootstraps your ability to write 
    extra traces yourself. You can read it through to help clarify the schema. """

def trace_from_file(fname: str) -> dict:
    """ Load the specified tracefile and then parse it line by line according 
        to the schema convention. Returns a dict with each of the components
        required by the driver. """

    def parse_tup(tup):
        assert len(tup) > 0, "Trace file must not contain any extra empty lines except for the final line"
        assert len(tup) != 1, (f"Only one line in trace file should have a single value,",
                               f" it should be first (already parsed here), and should be the integer m, got unexpected line {tup}") 
        if tup[0]   == "ins"  : return {"op":tup[0], "k":int(tup[1]), "v":tup[2]}
        elif tup[0] == "del"  : return {"op":tup[0], "k":int(tup[1])}
        elif tup[0] == "load" : return {"op":tup[0], "path": tup[1]}
        elif tup[0] == "dump" : return {"op":tup[0], "path": tup[1]}
        elif tup[0] == "qry" : return {"op":tup[0], "k": int(tup[1])}
        elif tup[0] == "qry_path" : return {"op":tup[0], "path": tup[1]}
        else:
            raise ValueError

    with open(fname, "r") as f:
        reader = csv.reader(f)
        try:
            lines = [l for l in reader]
            m = int(lines[0][0])
            full_trace = [parse_tup(line) for line in lines[1:]]
        except Exception as e:
            print(f"Error while parsing trace file...")
            raise e
        
        load_paths = [(idx, tup["path"]) for idx,tup in enumerate(full_trace) if tup["op"]=="load"]
        assert (len(load_paths) in [0,1]), "If trace includes a load command there must be only one."

        if len(load_paths) == 1:
            idx, path = load_paths[0]
            assert idx == 0, "If trace includes a load command it should be the first op, second line of file"
            init_path = path
        else:
            init_path = None

        dump_paths = [tup["path"] for tup in full_trace if tup["op"]=="dump"]
        assert len(dump_paths) > 0, "Trace file must contain at least one dump command."
        
        mixed_trace = [tup for tup in full_trace if tup["op"]!="load"]
        assert len(mixed_trace) >= 1, "Number of variable ops (ins,del,dump) in trace must be >= 1"

        query_cmds = [tup for tup in full_trace if tup["op"]=="qry"]
        if len(query_cmds) > 0:
            assert mixed_trace[-2]["op"] == "dump", "If trace contains qry cmds, second to last should be a dump"
            assert mixed_trace[-1]["op"] == "qry_path", "If trace contains qry cmds, last line should be a qry_path"
            query_path = mixed_trace[-1]["path"]
            mixed_trace = mixed_trace[:-1]
        else:
            query_path = None
            assert mixed_trace[-1]["op"] == "dump", "If trace has no qry cmds, last line should be a dump"

    return dict(mixed_trace=mixed_trace, m=m, init_path=init_path, query_path=query_path)


""" These are NOT required during main execution but they are useful
    in parsing the autograder's test case dumps if you want to 
    use them for debugging """

def trace_to_file(m: int, init_path: str, trace: list, query_path: str, out_path: str) -> None:
    """ Take the components of a trace and write them in order to a file. """

    with open(out_path, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([m])
        if init_path: 
            writer.writerow(["load", init_path])
        writer.writerows([d.values() for d in trace])
        if query_path: 
            writer.writerow(["qry_path", query_path])


def query_values_to_file(keychains_values: List[dict], query_path: str) -> None:
    """ Take the keychains and values corresponding the results of executing
        the queries in a trace (in dict format like the autograder spits out) 
        and writes them to a file. Similar to what the main method does at the end. """
        
    with open(f"{query_path}", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows([[k]+keychain+[value] for k,keychain,value in [d.values() for d in keychains_values]])


###############################################################################
#### Operator methods #########################################################
###############################################################################
""" These are up to you! Feel free to implement whatever helper methods and 
    lambdas/macros are useful in organizing your code. Even signatures are 
    ommitted as these are all based on the choices you make. """

def left_rot(pkey, pval, node1: BNode, node2: BNode) -> list:
    #Key and value in overfull node
    nkey = node1.keys.pop(0)
    nval = node1.values.pop(0)

    #Rotation
    node2.keys.append(pkey)
    node2.values.append(pval)
    node2.children.append(node1.children.pop(0))

    return [nkey, nval, node1, node2]

def right_rot(pkey, pval, node1: BNode, node2: BNode) -> list:
    #Key and value in overfull node
    nkey = node1.keys.pop()
    nval = node1.values.pop()

    #Rotation
    node2.keys.insert(0, pkey)
    node2.values.insert(0, pval)
    node2.children.insert(0, node1.children.pop())

    return [nkey, nval, node1, node2]

def split(root: BNode) -> list:
    #If None
    if root is None:
        raise ValueError("Can't run Split on None")
    
    #Index on which to divide up
    slice = floor((len(root.keys)-1)/2)
    
    #Median key/value
    mkey = root.keys[slice]
    mval = root.values[slice]
    
    #Split into two children
    lkeys = root.keys[0:slice]
    lvals = root.values[0:slice]
    lchilds = root.children[0:(slice+1)]
    rkeys = root.keys[(slice+1):]
    rvals = root.values[(slice+1):]
    rchilds = root.children[(slice+1):]

    #Create two new children
    child1 = BNode(root.m, lkeys, lvals, lchilds)
    child2 = BNode(root.m, rkeys, rvals, rchilds)
        
    return [mkey, mval, child1, child2]

def merge(pkey, pval, snode: BNode, bnode: BNode) -> BNode:
    #Append parent key and value to problem node
    snode.keys.append(pkey)
    snode.values.append(pval)

    #Collapse second node into first
    snode.keys.extend(bnode.keys)
    snode.values.extend(bnode.values)
    snode.children.extend(bnode.children)
    
    return snode

def rebalance_ins(root: BNode, i: int) -> BNode:
    curr = root.children[i]
    upbound = root.m-1
    
    #Raises error if leaf node
    if curr is None:
        raise ValueError("Cannot call rebalance_ins on leaf node")
    
    #Child has more than m-1 keys aka Post-Insertion
    if len(curr.keys) > upbound:

        #Push overfull over to left
        if i != 0:
            if root.children[i-1] is not None:
                if len(root.children[i-1].keys) < upbound:
                    result = left_rot(root.keys[i-1], root.values[i-1], root.children[i], root.children[i-1])
                    root.keys[i-1] = result[0]
                    root.values[i-1] = result[1]
                    root.children[i] = result[2]
                    root.children[i-1] = result[3]
                    return root
        #Push overfull over to right
        if i != len(root.children)-1:
            if root.children[i+1] is not None:
                if len(root.children[i+1].keys) < upbound:
                    result = right_rot(root.keys[i], root.values[i], root.children[i], root.children[i+1])
                    root.keys[i] = result[0]
                    root.values[i] = result[1]
                    root.children[i] = result[2]
                    root.children[i+1] = result[3]
                    return root
        
        #Split due to no other options
        result = split(root.children[i])
        root.keys.insert(i, result[0])
        root.values.insert(i, result[1])
        root.children[i] = result[3]
        root.children.insert(i, result[2])
        if root.children[-1] is None:
            root.children.pop()
    return root
    
def rebalance_del(root: BNode, i: int) -> BNode:
    #If None
    if root.children[i] is None: 
        return root

    #Variables    
    curr = root.children[i]
    lowbound = ceil(root.m/2) - 1

    #Child has less than ceil(m/2) keys aka Post-Deletion
    if len(curr.keys) < lowbound:
        #Left adjacent sibling gives node
        if i != 0:
            if root.children[i-1] is not None:
                if len(root.children[i-1].keys) > lowbound and i != 0:
                    result = right_rot(root.keys[i-1], root.values[i-1], root.children[i-1], root.children[i])
                    root.keys[i-1] = result[0]
                    root.values[i-1] = result[1]
                    root.children[i-1] = result[2]
                    root.children[i] = result[3]
                    return root
        #Right adjacent sibling gives node
        if i != len(root.children)-1:
            if root.children[i+1] is not None:
                if len(root.children[i+1].keys) > lowbound and i != len(curr.keys)-1:
                    result = left_rot(root.keys[i], root.values[i], root.children[i+1], root.children[i])
                    root.keys[i] = result[0]
                    root.values[i] = result[1]
                    root.children[i+1] = result[2]
                    root.children[i] = result[3]
                    return root
        #Merge with adjacent left sibling
        if i != 0:
            result = merge(root.keys[i-1], root.values[i-1], root.children[i-1], root.children[i])
            root.keys.pop(i-1)
            root.values.pop(i-1)
            if len(root.keys) == 0:
                return result
            else:
                root.children[i-1] = result
                root.children.pop(i)
        #Merge with adjacent right sibling
        else:
            result = merge(root.keys[i], root.values[i], root.children[i], root.children[i+1])
            root.keys.pop(i)
            root.values.pop(i)
            if len(root.keys) == 0:
                return result
            else:
                root.children[i] = result
                root.children.pop(i+1)
    return root


def insert(root: BNode, m: int, key, value, top = True):
    #If None
    if root is None:
        return BNode(m, [key], [value], [None, None])
    
    i = 0
    #Find where to insert
    while i < len(root.keys):
        curr = root.keys[i]
        if key == curr:
            root.values[i] = value
            return root
        elif key < curr:
            break
        i += 1
    
    #Insertion and Rebalancing
    if root.children[i] is None:
        root.keys.insert(i, key)
        root.values.insert(i, value)
        root.children.append(None)
    else:
        root.children[i] = insert(root.children[i], m, key, value, False)
        root = rebalance_ins(root, i)

    #Return
    if top is True:
        if len(root.keys) == root.m:
            result = split(root)
            root = BNode(m, [result[0]], [result[1]], [result[2], result[3]])
    return root


def getinordersucc(root: BNode) -> list:
    if root.children[0] is not None:
        result = getinordersucc(root.children[0])
        root.children[0] = result[0]
        return (rebalance_del(root, 0), result[1], result[2])
    else:
        rkey = root.keys.pop(0)
        rval = root.values.pop(0)
        root.children.pop(0)
        return [root, rkey, rval]


def delete(root: BNode, key, top = True):
    if root is None:
        return None
    else:
        i = 0
        #Find key to delete
        while i < len(root.keys):
            curr = root.keys[i]
            if key == curr:
                if root.children[i+1] is not None:
                    result = getinordersucc(root.children[i+1])
                    root.children[i+1] = result[0]
                    root.keys[i] = result[1]
                    root.values[i] = result[2]
                    return rebalance_del(root, i+1)
                else:
                    root.keys.pop(i)
                    root.values.pop(i)
                    root.children.pop()
                    if top is True and len(root.keys) == 0:
                        return None
                    else:
                        return root
            elif key < curr:
                break
            i += 1
        root.children[i] = delete(root.children[i], key, False)
        return rebalance_del(root, i)


def query(root: BNode, key) -> list:
    #If node None
    if root is None:
        return [None]
    
    #Find child to go to
    i = 0
    while i < len(root.keys):
        curr = root.keys[i]
        result = [curr]
        if key == curr:
            return [curr, root.values[i]]
        elif key < curr:
            break
        i += 1
    
    #Go down to child
    result.extend(query(root.children[i], key))
    return result


###############################################################################
#### Main driver method #######################################################
###############################################################################
""" This is the main method of your program and it takes in a tracefile, 
    parses it, and iterates over the operations, performing them. Only the 
    marked parts *must* be modified based on how you implement your operators
    however, other parts can be changed as long as the overall program 
    takes in the -tf/--tracefile argument and processes the trace correctly! """

def main(args):
    print(args)

    data  = trace_from_file(f"{args.tracefile}")
    
    m_val = data["m"]
    new_trace = data["mixed_trace"]
    i_path = data['init_path']
    query_path = data["query_path"]
    
    if i_path:
        with open(f"{i_path}", "r") as infile:
            tree = load_tree(infile.read())
        if tree: assert tree.m == m_val, "Should never have a mismatch between trace m value and init tree m value."
    else:
        tree = None

    query_results = []

    for cmd in new_trace:
        
        if cmd["op"] == "ins": #Insert
            k, v = cmd["k"], cmd["v"]
            tree = insert(tree, m_val, k, v)

        elif cmd["op"] == "del": #Delete
            k = cmd["k"]
            tree = delete(tree, k, True)

        elif cmd["op"] == "qry": #Query
            k = cmd["k"]
            keychain = query(tree, k)
            value = keychain.pop()

            query_results.append((k, keychain, value))

        elif cmd["op"] == "dump":
            path = f"{cmd['path']}"
            with open(path, "w") as outfile:
                outfile.write(dump_tree(tree))
        else:
            raise ValueError(f"Unknown op code in tracefile command: {cmd}")

    if query_path:
        with open(f"{query_path}", "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerows([[k]+keychain+[value] for k,keychain,value in query_results])
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-tf", 
                        "--tracefile", 
                        required=True)
    
    # you may add other optional args if you'd like, but the grader will only call 
    # the program with the single tracefile argument

    args = parser.parse_args()
    main(args)