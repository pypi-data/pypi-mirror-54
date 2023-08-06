from . import intecunits as _c
Unit = _c.Unit
Quantity = _c.Quantity

def __dims2int64(dims):
    L = 0
    for x in dims:
        if x < 0: x += 256
        L = (L<<8)+x
    return L
    
def new_Quantity( dims_or_unit, name, qclass_name = None ):
    ''' Derive a specific Quantity class
        E.g. if the name is 'electric current', a class called ElectricCurrentQuantity will be derived from Quantity
    '''
    qclass_name = qclass_name or ''.join(name.title().split())+"Quantity"
    qclass = type( qclass_name , (Quantity,), {} )         
    if isinstance(dims_or_unit, Unit):
        dim64 = dims_or_unit.dim64
        if dims_or_unit.qtype is Quantity:
            dims_or_unit.qtype = qclass
    else:
        dim64 = __dims2int64(dims_or_unit)
    qclass.dim64 = dim64
    qclass.name = name
    return qclass
    
class Registry(int):
    def __new__(cls):   
        pointer_to_registry_object = _c.new_registry()  
        i = super(Registry, cls).__new__(cls, pointer_to_registry_object)
        i.quantity_types = []
        i.units = []
        return i
    def __del__(self):
        _c.delete_registry(self)
    def new_Quantity(self, dims_or_unit, name, qclass_name = None):
        qclass = new_Quantity( dims_or_unit, name, qclass_name)
        setattr(self, qclass.__name__, qclass)
        self.quantity_types.append(qclass.__name__)
        override_default = False
        _c.register_qtype(self, qclass.dim64, qclass, override_default)
        return qclass        
    def new_Unit( self, quantity_or_unit, factor, symbol, name ):
        qu = quantity_or_unit
        if isinstance( qu, Unit):
            u = _c.new_Unit( self, qu.dim64, qu.qtype, qu.factor*factor, symbol, name)
        else:
            u = _c.new_Unit( self, qu.dim64, qu, factor, symbol, name)
        self.units.append(name)
        #self.units.append(name.upper())        
        setattr(self, name, u)
        #setattr(self, name.upper(), u)
        return u
    def new_Prefix( self, u, factor, symbol, name ):
        return self.new_Unit(u, factor, symbol + u.symbol, name + u.name)
    def __getattr__(self, n):
        f = self.prefixes.get(n[:4], None)
        if f:
            return f(self, getattr(self, n[4:]))
        f = self.prefixes.get(n[:5], None)
        if f:
            return f(self, getattr(self, n[5:]))
        f = self.prefixes.get(n[:3], None)
        if f:
            return f(self, getattr(self, n[3:]))
        raise AttributeError
    prefixes = {
        'yotta' : lambda self, u : self.new_Prefix( u, 1e24, 'Y', 'yotta'),
        'zetta' : lambda self, u : self.new_Prefix( u, 1e21, 'Z', 'zetta'),
        'exa'   : lambda self, u : self.new_Prefix( u, 1e18, 'E', 'exa'),
        'peta'  : lambda self, u : self.new_Prefix( u, 1e15, 'P', 'peta'),
        'tera'  : lambda self, u : self.new_Prefix( u, 1e12, 'T', 'tera'),
        'giga'  : lambda self, u : self.new_Prefix( u, 1e09, 'G', 'giga'),
        'mega'  : lambda self, u : self.new_Prefix( u, 1e06, 'M', 'mega'),
        'kilo'  : lambda self, u : self.new_Prefix( u, 1e03, 'k', 'kilo'),
        'hecto' : lambda self, u : self.new_Prefix( u, 1e02, 'h', 'hecto'),
        'deka'  : lambda self, u : self.new_Prefix( u, 1e01, 'da', 'deka'),
        'deci'  : lambda self, u : self.new_Prefix( u, 1e-01, 'd', 'deci'),
        'centi' : lambda self, u : self.new_Prefix( u, 1e-02, 'c', 'centi'),
        'milli' : lambda self, u : self.new_Prefix( u, 1e-03, 'm', 'milli'),
        'micro' : lambda self, u : self.new_Prefix( u, 1e-06, 'µ', 'micro'),
        'nano'  : lambda self, u : self.new_Prefix( u, 1e-09, 'n', 'nano'),
        'pico'  : lambda self, u : self.new_Prefix( u, 1e-12, 'p', 'pico'),
        'femto' : lambda self, u : self.new_Prefix( u, 1e-15, 'f', 'femto'),
        'atto'  : lambda self, u : self.new_Prefix( u, 1e-18, 'a', 'atto'),
        'zepto' : lambda self, u : self.new_Prefix( u, 1e-21, 'z', 'zepto'),
        'yocto' : lambda self, u : self.new_Prefix( u, 1e-24, 'y', 'yocto'),                     
    }
    def uppercase_units(self):
        unit_names = list(self.units)
        for name in unit_names:
            self.units.append(name.upper())        
            setattr(self, name.upper(), getattr(self, name))
        
for k, v in list(Registry.prefixes.items()): 
    Registry.prefixes[k.upper()] = v
