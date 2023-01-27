from IPython.display import display, Markdown, HTML, IFrame
from graphviz import Digraph

class RiverCrossGraph() :
    
    def __init__(self, width=500, height=500) :
        self.nodes = []
        self.edges = []
        self.width = width
        self.height = height

    def _render_graph(self) :
        self.g.render(cleanup = True)
        del self.g
        return display(IFrame('rivercross.png', width = self.width, height = self.height))
        # display(Markdown("<img src='rivercross.pdf'>"))
        
    def render_node(self, env, state, render = True) :
        _node = env._render(state)
        if not(_node in self.nodes) : self.nodes.append(_node) 
        
        self.g = Digraph('G', filename='rivercross', graph_attr = {'rankdir' : 'LR'})
        self.g.format = 'png'
        
        self.g.node(_node, color = 'green')
        if render : self._render_graph()

    def render_edge(self, env, state, next_state, action, done, win = 0, render = True) :
        _sta = env._render(state)
        _nxt = env._render(next_state)
        _act = self._render_action(action)
        _edge = (_sta, _nxt, _act)
        if not(_edge in self.edges) : self.edges.append(_edge)
        if not(_nxt in self.nodes) : self.nodes.append(_nxt) 
        
        self.g = Digraph('G', filename='rivercross', graph_attr = {'rankdir' : 'LR'})      
        self.g.format = 'png'

        for _node in self.nodes :
            _style = ''
            _color = 'black'
            if _node == _nxt :
                _color = 'green'
                if done: 
                    _style = 'filled'
                    if not win : _color = 'red'
            self.g.node(_node, color = _color, style = _style)    

        for _src, _tgt, _label in self.edges :
            self.g.edge(_src, _tgt, label = _label)

        if render : self._render_graph()
        
    def _render_action(self, action) :
        p2char = ['C', 'G', 'W', 'F']
        d2char =[ 'R', 'L' ]
        return "" + p2char[action["passenger"]] + d2char[action["direction"]]
    