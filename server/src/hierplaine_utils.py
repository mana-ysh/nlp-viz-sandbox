
from collections import defaultdict
import json

DUMMY_ROOT = "ROOT "
OFFSET = len(DUMMY_ROOT)



def convert2hierplain(result, base_key, dep_key):
    # FIXME: clean key order
    analyzed_result = result[base_key]
    input_text = result["original_text"]

    tree = {}
    chunks = [_convert_child(child) for child in analyzed_result["sequential"]]
    for chunk in chunks:
        chunk["nodeType"] = "chunk"
        for m in chunk["children"]:
            m["nodeType"] = "morph"
            m["link"] = "inner-morph"
            # NOTE: inner span information seems to cause UI problrem
            del m["spans"]

    deps = [(d["head_index"], d["modifier_index"], d["label"]) for d in result[dep_key]["sequential"]]
    parent2children, idx2depth = _cal_depth_in_tree(deps)
    idx2depth = {i: v for i, v in enumerate(idx2depth)}
    # add children (bottomup)
    for (idx, _) in sorted(idx2depth.items(), key=lambda x: x[1], reverse=True):
        if idx not in parent2children:  # leaf
            continue
        for c_idx in parent2children[idx]:
            chunks[c_idx]["link"] = "dep"
            chunks[idx]["children"].append(chunks[c_idx])
    
    root_idx = min(idx2depth.items(), key=lambda x: x[1])[0]
    root_chunk = chunks[root_idx]

    tree["text"] = input_text
    tree["root"] = root_chunk
    return tree


def _convert_child(child):
    """
    convert each child for hierplain usage

    TODO: append attributes and link information
    """
    assert "surface" in child
    assert "start" in child
    assert "end" in child

    _child = {}
    _child["word"] = child["surface"]
    _child["spans"] = [{"start": child["start"], "end": child["end"]}]
    if "children" in child:
        _grandchildren = [_convert_child(gc) for gc in child["children"]]
        _child["children"] = _grandchildren
    return _child


# FIXME: handle dep label
# FIXME: inefficient
def _cal_depth_in_tree(deps):
    n_node = len(deps) + 1
    parent2children = defaultdict(list)
    for (head_idx, mod_idx, _) in deps:
        parent2children[head_idx].append(mod_idx)
    parent2children = dict(parent2children)
    children = set([c for c_list in parent2children.values() for c in c_list])
    root_idx = list(set(list(range(n_node))).difference(children))
    assert len(root_idx) == 1
    root_idx = root_idx[0]

    # compute depth
    idx2depth = [-1 for _ in range(n_node)]
    idx2depth[root_idx] = 0
    for _ in range(n_node):
        for (head_idx, mod_idx, _) in deps:
            head_depth = idx2depth[head_idx]
            # update
            if head_depth > -1:
                idx2depth[mod_idx] = head_depth + 1
    
    assert all([depth > -1 for depth in idx2depth])
    return parent2children, idx2depth