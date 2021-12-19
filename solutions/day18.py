from math import ceil, floor

class Node:
    def __init__(self, parent):
        self.parent = parent

class LeafNode:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

def build_tree(el, parent=None):
    a, b = el

    p = Node(parent)

    if isinstance(a, int): # reached a leaf!
        n_a = LeafNode(p, a)
    else:
        n_a = build_tree(a, p)
    
    if isinstance(b, int): # reached a leaf!
        n_b = LeafNode(p, b)
    else:
        n_b = build_tree(b, p)
    
    p.left = n_a
    p.right = n_b

    return p

def find_depth_4(t, curr_depth=0):
    if curr_depth == 4 and isinstance(t, Node):
        return t
    if isinstance(t, LeafNode):
        return None
    
    return find_depth_4(t.left, curr_depth+1) or find_depth_4(t.right, curr_depth+1)

def find_gte_10(t):
    if isinstance(t, LeafNode):
        if t.value >= 10:
            return t
        return None
    
    return find_gte_10(t.left) or find_gte_10(t.right)

def get_before(root, target, prev_seen, l2r=True):
    if root == target:
        if not prev_seen:
            return (None, True)
        return (prev_seen[-1], True)

    if l2r:
        if isinstance(root.left, LeafNode):
            prev_seen.append(root.left)
        else:
            ret = get_before(root.left, target, prev_seen, l2r)
            if ret:
                return ret
    
    if isinstance(root.right, LeafNode):
        prev_seen.append(root.right)
    else:
        ret = get_before(root.right, target, prev_seen, l2r)
        if ret:
            return ret

    if not l2r:
        if isinstance(root.left, LeafNode):
            prev_seen.append(root.left)
        else:
            ret = get_before(root.left, target, prev_seen, l2r)
            if ret:
                return ret


def reduce_tree(t):
    while True:
        d4 = find_depth_4(t)
        if d4:
            before, _ = get_before(t, d4, [], True)
            after, _ = get_before(t, d4, [], False)

            if before:
                before.value += d4.left.value
            
            if after:
                after.value += d4.right.value
            
            zero = LeafNode(d4.parent, 0)
            if d4.parent.left == d4:
                d4.parent.left = zero
            else:
                d4.parent.right = zero
            
            continue

        g10 = find_gte_10(t)
        if g10:
            np = Node(g10.parent)

            l = LeafNode(np, floor(g10.value/2))
            r = LeafNode(np, ceil(g10.value/2))

            np.left = l
            np.right = r

            if g10.parent.left == g10:
                g10.parent.left = np
            else:
                g10.parent.right = np

            continue
        break

def magnitude(el):
    if isinstance(el, LeafNode):
        return el.value
    
    return 3 * magnitude(el.left) + 2 * magnitude(el.right)

def snail_sum(a, b):
    p = Node(None)
    p.left = a
    a.parent = p
    p.right = b
    b.parent = p

    reduce_tree(p)

    return p

if __name__ == "__main__":

    with open("day18.input") as f:
        l = [ eval(x) for x in f.readlines() ] # 🤮
    
    res = build_tree(l[0])
    for i in range(1, len(l)):
        res = snail_sum(res, build_tree(l[i]))
    
    print(magnitude(res))

    mm = 0
    for i in range(len(l)):
        for j in range(len(l)):
            if i == j:
                continue

            a = build_tree(l[i])
            b = build_tree(l[j])
            mm = max(magnitude(snail_sum(a,b)), mm)
    print(mm)
