import abc
import json
import re
from typing import Dict, TypeVar, Tuple, Type, Callable
from typing import Optional, List, Union, Any, Set

from pydgraph import DgraphClient

from grapl_analyzerlib.retry import retry


class Or(object):
    def __init__(self, *values: Union[str, int]):
        self.values = values

class Not(object):
    def __init__(self, value: Union[str, int]) -> None:
        self.value = value


class Cmp(object):
    def to_filter(self) -> str:
        pass


class Eq(Cmp):
    def __init__(self, predicate: str, value: Union[str, int, Not]) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, str):
            return 'eq({}, "{}")'.format(self.predicate, self.value)
        if isinstance(self.value, int):
            return "eq({}, {})".format(self.predicate, self.value)
        if isinstance(self.value, Not) and isinstance(self.value.value, str):
            return 'NOT eq({}, "{}")'.format(self.predicate, self.value.value)
        if isinstance(self.value, Not) and isinstance(self.value.value, int):
            return "NOT eq({}, {})".format(self.predicate, self.value.value)


class EndsWith(Cmp):
    def __init__(self, predicate: str, value: str) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, Not):
            value = self.value.value
            escaped_value = re.escape(value)
            return "NOT regexp({}, /.*{}/i)".format(self.predicate, escaped_value)
        else:
            escaped_value = re.escape(self.value)
            return "regexp({}, /.*{}/i)".format(self.predicate, escaped_value)


class Rex(Cmp):
    def __init__(self, predicate: str, value: Union[str, Not]) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, Not):
            value = self.value.value
            escaped_value = re.escape(value)
            return f"NOT regexp({self.predicate}, /{escaped_value}/)"
        else:
            escaped_value = re.escape(self.value)
            return f"regexp({self.predicate}, /{escaped_value}/)"


class Gt(Cmp):
    def __init__(self, predicate: str, value: Union[int, Not]) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, Not):
            return f"NOT gt({self.predicate}, {self.value})"
        else:
            return f"gt({self.predicate}, {self.value})"


class Lt(Cmp):
    def __init__(self, predicate: str, value: Union[int, Not]) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, Not):
            return f"NOT lt({self.predicate}, {self.value})"
        else:
            return f"lt({self.predicate}, {self.value})"


class Has(Cmp):
    def __init__(self, predicate: str) -> None:
        self.predicate = predicate

    def to_filter(self) -> str:
        return f"has({self.predicate})"


class Contains(Cmp):
    def __init__(self, predicate: str, value: Union[str, Not]) -> None:
        self.predicate = predicate
        self.value = value

    def to_filter(self) -> str:
        if isinstance(self.value, Not):
            value = self.value.value
            escaped_value = re.escape(value)
            return 'NOT alloftext({}, "{}")'.format(self.predicate, escaped_value)
        else:
            escaped_value = re.escape(self.value)
            return 'alloftext({}, "{}")'.format(self.predicate, escaped_value)


def get_var_block(
    node: Any, result_name: str, edge_name: str, binding_num: int, root: Any, already_converted: Set[Any]
) -> str:
    var_block = ""
    if node and node not in already_converted:
        var_block = node._get_var_block(binding_num, result_name, root, already_converted)
        if node == root:
            var_block = f"Binding{result_name}{binding_num} as {edge_name} {var_block}"
        else:
            var_block = f"{edge_name} {var_block}"

    return var_block


def _generate_filter(comparisons_list: List[List[Cmp]]) -> str:
    and_filters = []

    for comparisons in comparisons_list:
        if len(comparisons) > 1:
            comparisons = [c for c in comparisons if not isinstance(c, Has)]
        filters = [comparison.to_filter() for comparison in comparisons]
        filters = [f for f in filters if f]
        if not filters:
            continue
        and_filter = "(" + " AND ".join(filters) + ")"
        and_filters.append(and_filter)

    or_filters = " OR\n\t".join(and_filters)
    if not or_filters:
        return ""
    return "(\n\t{}\n)".format(or_filters)


def flatten_nodes(root: Any) -> List[Any]:
    node_list = [root]
    already_visited = set()
    to_visit = [root]

    while True:
        if not to_visit:
            break

        next_node = to_visit.pop()

        if next_node in already_visited:
            continue

        neighbors = next_node.get_neighbors()

        for neighbor in neighbors:
            if isinstance(neighbor, list):
                node_list.extend(neighbor)
                to_visit.extend(neighbor)
            else:
                node_list.append(neighbor)
                to_visit.append(neighbor)

        already_visited.add(next_node)

    # Maintaining order is a convenience
    return list(dict.fromkeys(node_list))


def __build_expansion(node: Union[Any, Any], already_visited: Set[Any]) -> str:
    if node in already_visited:
        return ""
    already_visited.add(node)

    edges = node.get_edges()

    expanded_edges = []

    for edge_tuple in edges:
        edge, neighbor = edge_tuple[0], edge_tuple[1]
        if neighbor in already_visited:
            continue
        already_visited.add(neighbor)
        neighbor_props = neighbor.get_property_names()
        expanded_edge = f"""
                
                    {edge} {{
                        uid,
                        {",".join(neighbor_props)},
                        {__build_expansion(neighbor, already_visited)}
                    }}  
                
            """
        expanded_edges.append(expanded_edge)
    if not expanded_edges:
        return ""
    return ",".join([x for x in expanded_edges if x])


def _build_expansion_root(node: Union[Any, Any]) -> str:
    props = node.get_property_names()
    edges = node.get_edges()

    expanded_edges = []

    already_visited = {node}

    for edge_tuple in edges:
        edge, neighbor = edge_tuple[0], edge_tuple[1]

        neighbor_props = neighbor.get_property_names()
        expanded_edge = f"""
                {edge} {{
                    uid,
                    {",".join([x for x in neighbor_props if x])},
                     
                    {__build_expansion(neighbor, already_visited)}
                
                }}
            """
        expanded_edges.append(expanded_edge)

    return f"""
            {",".join(props)},
            {", ".join([x for x in expanded_edges if x])}
    """


def _build_query(
    node: Any,
    var_blocks: List[str],
    bindings: List[str],
    count: bool = False,
    first: Optional[int] = None,
    result_name='res'
) -> str:
    joined_vars = "\n".join(var_blocks)
    if not count:
        expansion = _build_expansion_root(node)
    else:
        expansion = "count(uid) as c"

    if not first:
        first = ""
    else:
        first = f", first: {first}"

    query = f"""
            {{
            {joined_vars}
            
            {result_name}(func: uid({", ".join(bindings)}) {first}) {{
                uid,
                {expansion}
            }}
           
           }}
        """
    return query


def _get_queries(
    node_query: Any, node_key: str, count: bool = False, first: Optional[int] = None,
    result_name='res',
):
    if not first:
        first = 1

    all_nodes = flatten_nodes(node_query)
    bindings = []
    var_blocks = []

    for i, node in enumerate(all_nodes):
        bindings.append(f"Binding{result_name}{i}")
        var_blocks.append(
            node._get_var_block_root(i, result_name, root=node_query, node_key=node_key)
        )

    return _build_query(node_query, var_blocks, bindings, count, first=first, result_name=result_name)


def _str_cmps(
    predicate: str,
    eq: Optional[Union[str, List[str], Not, List[Not]]] = None,
    contains: Optional[Union[str, List[str], Not, List[Not]]] = None,
    ends_with: Optional[Union[str, List[str], Not, List[Not]]] = None,
):
    cmps = []

    inner_eq = eq
    if isinstance(eq, Not):
        inner_eq = eq.value
    if isinstance(inner_eq, str):
        cmps.append([Eq(predicate, eq)])
    elif isinstance(inner_eq, list):
        _eq = [Eq(predicate, e) for e in eq]
        cmps.append(_eq)

    inner_contains = contains
    if isinstance(contains, Not):
        inner_contains = contains.value

    if isinstance(inner_contains, str):
        cmps.append([Contains(predicate, contains)])
    elif isinstance(inner_contains, list):
        _contains = [Contains(predicate, e) for e in contains]
        cmps.append(_contains)

    inner_ends_with = ends_with
    if isinstance(ends_with, Not):
        inner_ends_with = ends_with.value

    if isinstance(inner_ends_with, str):
        cmps.append([EndsWith(predicate, ends_with)])
    elif isinstance(inner_ends_with, list):
        _ends_with = [EndsWith(predicate, e) for e in ends_with]
        cmps.append(_ends_with)

    if not (eq or contains or ends_with):
        cmps.append([Has(predicate)])

    return cmps


def _int_cmps(
    predicate: str,
    eq: Optional[Union[int, List, Not, List[Not]]] = None,
    gt: Optional[Union[int, List, Not, List[Not]]] = None,
    lt: Optional[Union[int, List, Not, List[Not]]] = None,
) -> List[List[Cmp]]:
    cmps = []

    inner_eq = eq
    if isinstance(eq, Not):
        inner_eq = eq.value

    if isinstance(inner_eq, int):
        cmps.append([Eq(predicate, eq)])
    elif isinstance(inner_eq, list):
        _eq = [Eq("last_seen_timestamp", e) for e in eq]
        cmps.append(_eq)

    inner_gt = gt
    if isinstance(gt, Not):
        inner_gt = gt.value

    if isinstance(inner_gt, int):
        cmps.append([Gt(predicate, gt)])
    elif isinstance(inner_gt, list):
        _gt = [Gt("last_seen_timestamp", e) for e in gt]
        cmps.append(_gt)

    inner_lt = lt
    if isinstance(lt, Not):
        inner_lt = lt.value

    if isinstance(inner_lt, int):
        cmps.append([Lt(predicate, lt)])
    elif isinstance(inner_lt, list):
        _lt = [Lt(predicate, e) for e in lt]
        cmps.append(_lt)

    if not (eq or gt or lt):
        cmps.append([Has(predicate)])

    return cmps


PropertyFilter = List[List[Cmp]]
StrCmp = Union[str, List[str], Not, List[Not]]
IntCmp = Union[int, List[int], Not, List[Not]]

EdgeFilter = Optional[Any]

V = TypeVar("V", bound="Viewable")


class Viewable(abc.ABC):
    def __init__(self, dgraph_client: DgraphClient, node_key: str, uid: str):
        self.dgraph_client = dgraph_client
        self.node_key = node_key
        self.uid = uid

    @staticmethod
    @abc.abstractmethod
    def get_property_types() -> List[Tuple[str, Callable[[Any], Union[str, int]]]]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_edge_types() -> List[Tuple[str, Union[List[Type[V]], Type[V]]]]:
        pass

    @abc.abstractmethod
    def get_property_tuples(self) -> List[Tuple[str, Any]]:
        pass

    @abc.abstractmethod
    def get_edge_tuples(self) -> List[Tuple[str, Any]]:
        pass

    def get_property(
        self, prop_name: str, prop_type: Callable[[Any], Union[str, int]]
    ) -> Optional[Union[str, int]]:
        query = f"""
            {{
                q0(func: uid("{self.uid}")) {{
                    uid,
                    {prop_name}
                }}
            
            }}
        """
        res = json.loads(self.dgraph_client.txn(read_only=True).query(query).json)

        raw_prop = res["q0"]
        if not raw_prop:
            return None

        prop = prop_type(raw_prop[0][prop_name])

        return prop

    @retry(delay=0.05)
    def get_properties(
        self, prop_name: str, prop_type: Callable[[Any], Union[str, int]]
    ) -> List[str]:
        query = f"""
            {{
                q0(func: uid("{self.uid}")) {{
                    uid,
                    {prop_name}
                }}
            
            }}
        """
        res = json.loads(self.dgraph_client.txn(read_only=True).query(query).json)

        raw_props = res["q0"]

        if not raw_props:
            return []

        props = [prop_type(p[prop_name]) for p in raw_props]

        return props

    @retry(delay=0.05)
    def get_edge(self, edge_name: str, edge_type: V) -> Optional[V]:
        query = f"""
            {{
                q0(func: uid("{self.uid}")) {{
                    uid,
                    {edge_name} {{
                        uid,
                        node_type,
                        node_key,
                    }}
                }}
            
            }}
        """
        res = json.loads(self.dgraph_client.txn(read_only=True).query(query).json)

        raw_edge = res["q0"]
        if not raw_edge:
            return None

        edge = edge_type.from_dict(self.dgraph_client, raw_edge[0][edge_name])
        return edge

    @retry(delay=0.05)
    def get_edges(self, edge_name: str, edge_type: Type[V]) -> List[V]:
        query = f"""
            {{
                q0(func: uid("{self.uid}")) {{
                    uid,
                    {edge_name} {{
                        uid,
                        node_type,
                        node_key,
                    }}
                }}
            
            }}
        """
        res = json.loads(self.dgraph_client.txn(read_only=True).query(query).json)

        raw_edges = res["q0"]

        if not raw_edges:
            return []

        raw_edges = raw_edges[0][edge_name]
        edges = [edge_type.from_dict(self.dgraph_client, f) for f in raw_edges]

        return edges

    @classmethod
    def from_dict(cls: Type[V], dgraph_client: DgraphClient, d: Dict[str, Any]) -> V:
        properties = {}
        if d.get("node_type"):
            properties["node_type"] = d["node_type"]

        for prop, into in cls.get_property_types():
            val = d.get(prop)
            if val:
                val = into(val)
                properties[prop] = val

        edges = {}
        for edge_tuple in cls.get_edge_types():
            edge_name, ty = edge_tuple[0], edge_tuple[1]
            raw_edge = d.get(edge_name, None)

            if not raw_edge:
                continue

            if isinstance(ty, List):
                ty = ty[0]

                if d.get(edge_name, None):
                    _edges = [ty.from_dict(dgraph_client, f) for f in d[edge_name]]
                    if len(edge_tuple) == 3:
                        edges[edge_tuple[2]] = _edges
                    else:
                        edges[edge_name] = _edges

            else:
                edge = ty.from_dict(dgraph_client, raw_edge[0])
                if len(edge_tuple) == 3:
                    edges[edge_tuple[2]] = edge
                else:
                    edges[edge_name] = edge

        cleaned_edges = {}
        for edge_name, edge in edges.items():
            if edge_name[0] == "~":
                edge_name = edge_name[1:]
            cleaned_edges[edge_name] = edge

        return cls(
            dgraph_client=dgraph_client,
            node_key=d["node_key"],
            uid=d["uid"],
            **properties,
            **cleaned_edges,
        )


Q = TypeVar("Q", bound="Queryable")


class Queryable(abc.ABC):
    def __init__(self, view_type: Type[V]) -> None:
        self._node_key = Has("node_key")  # type: Cmp
        self._uid = None  # type: Optional[Cmp]
        self.view_type = view_type

    @abc.abstractmethod
    def get_unique_predicate(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_node_type_name(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_properties(self) -> List[Tuple[str, PropertyFilter]]:
        pass

    @abc.abstractmethod
    def get_forward_edges(self) -> List[Tuple[str, Any]]:
        pass

    @abc.abstractmethod
    def get_reverse_edges(self) -> List[Tuple[str, Any, str]]:
        pass

    def get_node_key_filter(self) -> PropertyFilter:
        return [[self._node_key]]

    def get_uid_filter(self) -> PropertyFilter:
        if not self._uid:
            return []
        return [[self._uid]]

    def with_node_key(self: Q, node_key: str) -> Q:
        self._node_key = Eq("node_key", node_key)
        return self

    def with_uid(self: Q, eq: Union[str, Not]) -> Q:
        self._uid = Eq("uid", eq)
        return self

    def get_property_names(self) -> List[str]:
        return [p[0] for p in self.get_properties() if p and p[1]]

    def get_edges(self) -> List[Tuple[str, Any]]:
        all_edges = []
        all_edges.extend(self.get_forward_edges())
        all_edges.extend(self.get_reverse_edges())
        return [e for e in all_edges if e and e[1]]

    def get_neighbors(self) -> List[Q]:
        return [e[1] for e in self.get_edges() if e and e[1]]

    @retry(delay=0.05)
    def query(
        self,
        dgraph_client: DgraphClient,
        contains_node_key: Optional[str] = None,
        first: Optional[int] = 1000,
    ) -> List[V]:
        if contains_node_key:
            query_str = _get_queries(self, node_key=contains_node_key, first=1)
        else:
            query_str = self.to_query(first=first)

        raw_views = json.loads(dgraph_client.txn(read_only=True).query(query_str).json)[
            "res"
        ]

        if not raw_views:
            return []

        return [
            self.view_type.from_dict(dgraph_client, raw_view) for raw_view in raw_views
        ]

    def query_first(
        self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional[V]:
        res = self.query(dgraph_client, contains_node_key, first=1)
        if res:
            return res[0]
        else:
            return None

    @retry(delay=0.05)
    def get_count(
        self,
        dgraph_client: DgraphClient,
        max: Optional[int] = None,
        contains_node_key: Optional[str] = None,
    ) -> int:
        if contains_node_key:
            query_str = _get_queries(self, node_key=contains_node_key, count=True)
        else:
            query_str = self.to_query(count=True, first=max or 1000)

        raw_count = json.loads(dgraph_client.txn(read_only=True).query(query_str).json)[
            "res"
        ]

        if not raw_count:
            return 0
        else:
            return raw_count[0].get("count", 0)

    def to_query(self, count: bool = False, first: Optional[int] = None) -> str:
        var_block = self._get_var_block_root(0, 'res', root=self)

        return _build_query(self, [var_block], ["Bindingres0"], count=count, first=first)

    def _filters(self) -> str:
        inner_filters = []

        for prop in self.get_properties():
            if not prop[1]:
                continue
            f = _generate_filter(prop[1])
            if f:
                inner_filters.append(f)

        if not inner_filters:
            return ""

        return f"@filter({'AND'.join(inner_filters)})"

    def _get_var_block(
        self, result_name: str, binding_num: int, root: Any, already_converted: Set[Any]
    ) -> str:
        if self in already_converted:
            return ""
        already_converted.add(self)

        filters = self._filters()

        edge_var_blocks = []

        for edge_tuple in self.get_edges():
            edge_name, edge = edge_tuple[0], edge_tuple[1]
            var_block = get_var_block(
                edge, result_name, edge_name, binding_num, root, already_converted
            )
            edge_var_blocks.append(var_block)

        edge_var_blocks = "\n".join(edge_var_blocks)

        block = f"""
            {filters} {{
                uid,
                {edge_var_blocks}
            }}
            """

        return block

    def _get_var_block_root(
        self, binding_num: int, result_name: str, root: Any, node_key: Optional[str] = None
    ):
        already_converted = {self}
        root_var = ""
        if self == root:
            root_var = f"Binding{result_name}{binding_num} as "

        filters = self._filters()

        edge_var_blocks = []

        for edge_tuple in self.get_edges():
            edge_name, edge = edge_tuple[0], edge_tuple[1]
            var_block = get_var_block(
                edge, result_name, edge_name, binding_num, root, already_converted
            )
            edge_var_blocks.append(var_block)

        type_name = self.get_node_type_name()

        if self._node_key and isinstance(self._node_key, Eq):
            func_filter = self._node_key.to_filter()
        elif node_key:
            func_filter = f'eq(node_key, "{node_key}")'
        elif type_name:
            func_filter = f'eq(node_type, "{self.get_node_type_name()}")'
        elif self.get_unique_predicate():
            func_filter = f"has({self.get_unique_predicate()})"
        else:
            # worst case, we have to search every node :(
            func_filter = "has(node_key)"

        edge_var_blocks = "\n".join(edge_var_blocks)

        block = f"""
            {root_var} var(func: {func_filter}) @cascade {filters} {{
                uid,
                {edge_var_blocks}
            }}
            """

        return block
