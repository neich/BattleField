import random
import math
import bisect
import csv
import timeit


class Parameter:
    def __init__(self, name, min, max, delta):
        self.name = name
        self.min = min
        self.max = max
        self.delta = delta

    def round(self, value):
        d = value - self.min
        n = int(round(d / self.delta))
        return self.min + n * self.delta


class PSet:
    def __init__(self):
        self.parameters = {}

    def __iter__(self):
        return iter(self.parameters)

    def add_parameter(self, param):
        self.parameters[param.name] = param


class PState:
    def __init__(self):
        self.parameters = {}
        self.values = []

    def __iter__(self):
        return iter(self.parameters)

    def __hash__(self):
        return hash(','.join([str(v) for v in self.values]))

    def __str__(self):
        return ','.join([str((name, value[1])) for name, value in self.parameters.iteritems()])

    def add_parameter(self, param, value):
        self.parameters[param.name] = (param, param.round(value))
        self.__compute_values__()

    def set_value(self, pname, value):
        param, v = self.parameters[pname]
        self.parameters[pname] = (param, param.round(value))
        self.__compute_values__()

    def get_value(self, pname):
        return self.parameters[pname][1]

    def __compute_values__(self):
        pnames = list(self.parameters)
        pnames.sort()
        self.values = [self.parameters[pname][1] for pname in pnames]

    def clone(self):
        ps = PState()
        for pname in self:
            param, value = self.parameters[pname]
            ps.add_parameter(param, value)
        return ps

    def new_delta(self, pname, n):
        param, value = self.parameters[pname]
        new_value = param.round(value + n * param.delta)
        if new_value > param.max or new_value < param.min:
            return None
        new_pstate = self.clone()
        new_pstate.set_value(pname, new_value)
        return new_pstate

    def distance(self, pstate):
        d = 0
        for pname in self:
            p0 = self.parameters[pname][1]
            p1 = pstate.get_value(pname)
            d += (p1-p0)*(p1-p0)

        return math.sqrt(d)


class PInterval:
    def __init__(self):
        self.parameters = {}

    def __iter__(self):
        return iter(self.parameters)

    def add_parameter(self, param, min_p=None, max_p=None):
        self.parameters[param.name] = (param, min_p if min_p else param.min, max_p if max_p else param.max)

    def set_interval(self, pname, min_p, max_p):
        self.parameters[pname][1] = min_p
        self.parameters[pname][2] = max_p

    def get_min_max(self, pname):
        return self.parameters[pname][1], self.parameters[pname][2]

    def get_parameter(self, pname):
        return self.parameters[pname][0]

    def get(self, pname):
        return self.parameters[pname]

    def get_size(self, pname):
        p = self.parameters[pname]
        return (p[2] - p[1]) / p[0].delta

    def set_min_max(self, pname, min_p, max_p):
        p = self.parameters[pname]
        self.parameters[pname] = (p[0], min_p, max_p)

    def clone(self):
        pi = PInterval()
        for pname in self.parameters:
            p = self.parameters[pname]
            pi.add_parameter(p[0], p[1], p[2])
        return pi


class ONode:
    index = 0

    def __init__(self, pinterval):
        self.index = ONode.index
        ONode.index += 1
        self.interval = pinterval
        self.last_eval = None
        vol = 1
        for pname in pinterval:
            vol *= pinterval.get_size(pname)
        self.volume = vol
        self.center = self.compute_center()

    def get_index(self):
        return self.index

    def get_interval(self):
        return self.interval

    def get_max_size(self):
        max_size = 0
        max_pname = None
        for pname in self.interval:
            size = self.interval.get_size(pname)
            if size > max_size:
                max_size = size
                max_pname = pname

        return max_size, max_pname

    def get_center(self):
        return self.center

    def compute_center(self):
        pstate = PState()
        for pname in self.interval:
            p = self.interval.get(pname)
            pstate.add_parameter(p[0], p[1] + (p[2] - p[1]) / 2.0)

        return pstate

    def get_volume(self):
        return self.volume

    def get_last_eval(self):
        return self.last_eval

    def set_last_eval(self, eval):
        self.last_eval = eval

    def subdivide(self, pname):
        min_interval = self.get_interval().clone()
        max_interval = self.get_interval().clone()

        param, min_p, max_p = self.get_interval().get(pname)
        mid_p = param.round(min_p + (max_p - min_p) / 2.0)
        min_interval.set_min_max(pname, min_p, mid_p)
        max_interval.set_min_max(pname, mid_p, max_p)

        return ONode(min_interval), ONode(max_interval)


class NodeEvaluation:
    current_index = 0

    def __init__(self, pstate, f, extra):
        self.pstate = pstate
        self.f = f
        self.extra = extra
        self.current_minimum = 1e100
        self.index = NodeEvaluation.current_index
        NodeEvaluation.current_index += 1

    def __lt__(self, other):
        return self.f < other.f


class Optimizer:

    def __init__(self, start_interval, function, extra_data, initial_subdivison_d, n_iterations, keep_best=50):
        self.nc_subdivisions_pre = 0
        self.nc_subdivisions = 0
        self.extra_data = extra_data
        self.initial_subdivison_d = initial_subdivison_d
        self.n_iterations = n_iterations
        self.keep_best = keep_best
        self.best_nodes = []
        self.start_interval = start_interval
        self.function = function
        self.node_index = 0
        self.nodes = []
        self.nodes_computed = {}
        self.nodes_explored = {}
        self.minimum = NodeEvaluation(None, 1e100, None)

    def eval_func(self, pstate):
        print("Evaluating node at {}".format(pstate))
        if pstate in self.nodes_computed:
            result = self.nodes_computed[pstate]
        else:
            f, extra_data = self.function(pstate, self.extra_data)
            nc = NodeEvaluation(pstate, f, extra_data)
            self.nodes_computed[pstate] = nc
            result = nc  # We are minimizing, so no changes
            bisect.insort(self.best_nodes, nc)

            if len(self.best_nodes) > self.keep_best:
                self.best_nodes.pop()

            if result.f < self.minimum.f:
                print("NEW MINIMUM: {}, {}".format(result.f, result.pstate))
                self.minimum = result

            nc.current_minimum = self.minimum.f

        return result

    def init_search(self):
        self.initial_subdivision(self.initial_subdivison_d)
        self.initialize_nodes()

    def initial_subdivision(self, min_dist):
        pending = [ONode(self.start_interval)]
        while True:
            if len(pending) == 0:
                break

            nn = pending.pop()

            d, name = nn.get_max_size()

            if d < min_dist:
                self.nodes.append(nn)
            else:
                n_min, n_max = nn.subdivide(name)
                pending.extend((n_min, n_max))

    def step(self):
        self.compute_cdf()
        self.process_node()

    def compute_cdf(self):
        pass

    def process_node(self):
        t0 = random.random()
        explore = self.nc_subdivisions - self.nc_subdivisions_pre > 10
        lowcdf = t0 < 0.5

        if explore:
            dist = 4

            print(" ### EXPLORING NODE WITH DISTANCE {} ###".format(dist))

            self.nc_subdivisions_pre = self.nc_subdivisions

            good = False
            elem_to_explore = None
            min_f = 1e100
            for pstate_nc in self.nodes_computed:
                eval_nc = self.nodes_computed[pstate_nc]
                f = eval_nc.f
                if pstate_nc not in self.nodes_explored and f < 1000:
                    good = True
                    for ne in self.nodes_explored:
                        if pstate_nc.distance(ne) < dist:
                            good = False
                            break

                if not good:
                    continue

                if f < min_f:
                    min_f = f
                    elem_to_explore = eval_nc

            if elem_to_explore is not None:
                print("Exploring node with F = {}".format(elem_to_explore.f))
                self.explore(elem_to_explore)
                print(" ### END EXPLORING NODE ###")
                self.nodes_explored[elem_to_explore.pstate] = True

        elif not lowcdf:
            selected = self.nodes[0]
            print(" --- SUBVIVIDE BIGGEST NODE ---")
            max_vol = 0.0
            for node in self.nodes:
                v = node.get_volume()
                if v > max_vol:
                    max_vol = v
                    selected = node

            cs = len(self.nodes_computed)
            self.subdivide_node(selected, True)
            self.nc_subdivisions += len(self.nodes_computed) - cs
        else:
            print(" --- SUBDIVIDE BEST NODE --- ")
            min_f = 1e100
            selected = None
            for node in self.nodes:
                f = node.get_last_eval().f
                if f < min_f:
                    min_f = f
                    selected = node

            cs = len(self.nodes_computed)
            self.subdivide_node(selected, True)
            self.nc_subdivisions += len(self.nodes_computed) - cs

    def initialize_nodes(self):
        for node in self.nodes:
            self.init_state(node)

    def subdivide_node(self, node, erase):
        print("Subdividing node: {} with F = {}".format(node.get_index(), node.get_last_eval().f))

        if node.get_max_size()[0] < 4:
            self.nodes.remove(node)
            return False

        d, name = node.get_max_size()

        if erase:
            self.nodes.remove(node)

        self.nodes.extend(node.subdivide(name))

        self.init_state(self.nodes[-1])
        self.init_state(self.nodes[-2])

        return True

    def init_state(self, node):
        n_eval = self.eval_func(node.get_center())
        node.set_last_eval(n_eval)

    def explore(self, eval):

        class EvalElem:
            def __init__(self, pstate, f, depth):
                self.pstate = pstate
                self.f = f
                self.explored = False
                self.depth = depth

            def __lt__(self, other):
                return self.f < other.d

        min_f = eval.f

        explore_nodes = [EvalElem(eval.pstate, eval.f, 0)]
        nodes_traversed = {}
        while len(explore_nodes) > 0:
            explore_nodes.sort()
            current = explore_nodes.pop()

            if current.depth > 5:
                continue

            if current.pstate in nodes_traversed:
                continue

            nodes_traversed[current.pstate] = True

            print("--- EXPLORING NODE AT DEPTH {} with function value {}".format(current.depth, current.f))

            pstates_to_explore = []
            for pname, (param, value) in current.pstate.parameters.iteritems():
                ps_delta_pos = current.pstate.new_delta(pname, 1)
                ps_delta_neg = current.pstate.new_delta(pname, -1)

                pstates_to_explore += [ps_delta_pos] if ps_delta_pos is not None else []
                pstates_to_explore += [ps_delta_neg] if ps_delta_neg is not None else []

            new_nodes = []
            for pstate in pstates_to_explore:
                if pstate not in nodes_traversed:
                    eval = self.eval_func(pstate)
                    nodes_traversed[pstate] = True
                    if eval.f < current.f:
                        new_nodes.append(EvalElem(pstate, eval.f, current.depth + 1))
                    if eval.f < min_f:
                        print("New local minimum: {} over {}".format(eval.f, min_f))
                        min_f = eval.f

            explore_nodes = explore_nodes + new_nodes

    def run(self):
        start_time = timeit.default_timer()
        self.init_search()
        for i in xrange(self.n_iterations):
            print('STEP {} OF {}'.format(i, self.n_iterations))
            self.step()

        elapsed = timeit.default_timer() - start_time
        print('ELAPSD TIME: {}'.format(elapsed))

        nodes = [(k, v) for k, v in self.nodes_computed.items()]
        nodes.sort(key=lambda node: node[1].index)
        with open('search.csv', 'wb') as csvfile:
            node_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            node_writer.writerow(['Index', 'FromX', 'FromY', 'Distance', 'Minimum'])
            for pstate, node in nodes:
                if node.f < 10000:
                    node_writer.writerow([node.index, pstate.get_value('TARGET_Y'), pstate.get_value('TARGET_X'), node.f, node.current_minimum])
            csvfile.close()

        return self.minimum.f, self.minimum.pstate, self.minimum.extra
