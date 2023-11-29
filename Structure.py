# classes: Station(istgah), Block(khotot), Demand(taghaza)

class Demand():
    
    def __init__(self, Index, Origin, Destination, Volume):
        self.index = Index
        self.origin = Origin
        self.destination = Destination
        self.volume = Volume        
        
class Station():
    # we have limits in here
    
    def __init__(self, Index, Block_Capacity, Vagon_Capacity):
        self.index = Index
        self.block_capacity = Block_Capacity
        self.vagon_capacity = Vagon_Capacity
        
class Block():
    
    def __init__(self, Index, Origin, Destination, Cost_Per_Unit):
        self.index = Index
        self.origin = Origin
        self.destination = Destination
        self.cost = Cost_Per_Unit
