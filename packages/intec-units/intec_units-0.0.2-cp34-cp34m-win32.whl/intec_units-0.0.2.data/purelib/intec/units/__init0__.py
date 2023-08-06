from . import intecunits as __c
Unit = __c.Unit
Quantity = __c.Quantity

def __dims2int64(dims):
    L = 0
    for x in dims:
        if x < 0: x += 256
        L = (L<<8)+x
    return L
        
def __new_Quantity( dims_or_unit, name, inject, override_default):
    ''' Derive a specific Quantity class
        E.g. if the name is 'electric current', a class called ElectricCurrentQuantity will be derived from Quantity
    '''
    qclass_name = ''.join(name.title().split())+"Quantity"
    if qclass_name in globals():
        raise RuntimeError( "Class %s already exists!"%qclass_name )
    qclass = type( qclass_name , (Quantity,), {} )         
    if inject:
        globals()[qclass_name] = qclass
    if isinstance(dims_or_unit, Unit):
        dim64 = dims_or_unit.dim64
        dims_or_unit.qtype = qclass  
    else:
        dim64 = __dims2int64(dims_or_unit)
    __c.register_qtype(dim64, qclass, override_default)
    qclass.dim64 = dim64
    return qclass

def new_Quantity0( dims_or_unit, name, override_default = False ):
    return __new_Quantity( dims_or_unit, name, True, override_default)

def new_Quantity( dims_or_unit, name, override_default = False ):
    return __new_Quantity( dims_or_unit, name, False, override_default)
    
def new_Unit( quantity_or_unit, factor, symbol, name ):
    qu = quantity_or_unit
    if isinstance( qu, Unit):
        return __c.new_Unit( qu.dim64, qu.qtype, qu.factor*factor, symbol, name)
    else:
        return __c.new_Unit( qu.dim64, qu, factor, symbol, name)
    
    
##########################################################################################################
    
def __exafy(u):
    name = 'EXA' + u.name.upper()    
    globals()[name] = new_Unit( u, 1e18, 'E'+u.symbol, 'exa'+u.name )     
def __petafy(u):
    name = 'PETA' + u.name.upper()    
    globals()[name] = new_Unit( u, 1e15, 'P'+u.symbol, 'peta'+u.name )     
def __terafy(u):
    name = 'TERA' + u.name.upper()
    globals()[name] = new_Unit( u, 1e12, 'T'+u.symbol, 'tera'+u.name )     
def __gigafy(u):
    name = 'GIGA' + u.name.upper()
    globals()[name] = new_Unit( u, 1e9, 'G'+u.symbol, 'giga'+u.name )     
def __megafy(u):
    name = 'MEGA' + u.name.upper()
    globals()[name] = new_Unit( u, 1e6, 'M'+u.symbol, 'mega'+u.name )     
def __kilofy(u):
    name = 'KILO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e3, 'k'+u.symbol, 'kilo'+u.name )     
def __millify(u):
    name = 'MILLI' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-3, 'm'+u.symbol, 'milli'+u.name )     
def __microfy(u):
    name = 'MICRO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-6, 'u'+u.symbol, 'micro'+u.name )     
def __nanofy(u):
    name = 'NANO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-9, 'n'+u.symbol, 'nano'+u.name )     
def __picofy(u):
    name = 'PICO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-12, 'p'+u.symbol, 'pico'+u.name )     
def __femtofy(u):
    name = 'FEMTO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-15, 'f'+u.symbol, 'femto'+u.name )     
def __attofy(u):
    name = 'ATTO' + u.name.upper()
    globals()[name] = new_Unit( u, 1e-18, 'a'+u.symbol, 'atto'+u.name )     
    

def __minify(u):
    __millify(u)
    __microfy(u)
    __nanofy(u)
    __picofy(u)
    __femtofy(u)    
    __attofy(u)    

def __maxify(u):
    __exafy(u)
    __petafy(u)
    __terafy(u)
    __gigafy(u)
    __megafy(u)
    __kilofy(u)

##########################################################################################################

_q = new_Quantity0( (0,0,0,0,0,0,0), 'dimensionless' )
__ONE = new_Unit( _q, 1, '1', '1' )
PERCENT = new_Unit( _q, 1e-2, '%', 'percent' )
PPM = new_Unit( _q, 1e-6, 'ppm', 'parts per million' )
DEGREE = new_Unit( _q, 360, 'degree', 'degree' )
pi = 3.14159265358979323846
RADIAN = new_Unit( _q, 2*pi, 'rad', 'radian' )
STERADIAN = new_Unit( _q, 4*pi, 'sr', 'steradian' )
del pi

_q   = new_Quantity0( (1,0,0,0,0,0,0), 'mass' )
KILOGRAM = new_Unit( _q, 1, 'kg', 'kilogram' )
GRAM = new_Unit( _q, 1e-3, 'g', 'gram' )
__minify(GRAM)
POUND = new_Unit( _q, 0.450, 'lb', 'pound' )
    
_q  = new_Quantity0((0,1,0,0,0,0,0), 'length')
METER = new_Unit( _q, 1, 'm', 'meter')
__minify(METER)
__kilofy(METER)
CENTIMETER = new_Unit( _q, 1e-2, 'cm', 'centimeter')
LIGHTYEAR = new_Unit( _q, 9.46073047258080e15, 'ly', 'light-year')

YARD = new_Unit( _q, 0.9144, 'yd', 'yard' )

_q = new_Quantity0((0,0,1,0,0,0,0), 'time')
SECOND = new_Unit( _q, 1, 's', 'second' )
__minify(SECOND)
MINUTE = new_Unit( _q, 60, 'min', 'minute' )
HOUR = new_Unit( _q, 3600, 'h', 'hour' )
DAY = new_Unit( _q, 86400, 'd', 'day' )

_q = new_Quantity0((0,0,0,1,0,0,0), 'electric current')
AMPERE = new_Unit( _q, 1, 'A', 'ampere')
__minify(AMPERE)
    
_q = new_Quantity0( (0,0,0,0,1,0,0), 'temperature')
KELVIN = new_Unit( _q, 1, 'K', 'kelvin') 
CELCIUS = new_Unit( _q, 0, 'C', 'celcius') 
FAHRENHEIT = new_Unit( _q, 0, 'F', 'fahrenheit') 

_q  = new_Quantity0((0,0,0,0,0,1,0), 'amount of substance')
MOLE = new_Unit( _q, 1, 'mol', 'mole') 

_q   = new_Quantity0((0,0,0,0,0,0,1), 'luminous intensity')
CD = new_Unit( _q, 1, 'cd', 'candela') 


##########################################################################################################
#
#   derived units
#
_q = new_Quantity0( SECOND**-1, 'frequency')
HERTZ = new_Unit( _q, 1, 'Hz', 'hertz')
__maxify(HERTZ)

_q = new_Quantity0( METER**2, 'area' )
_q = new_Quantity0( METER**3, 'volume' )
_q = new_Quantity0( METER/SECOND, 'velocity' )
#_q = new_Quantity0( (0,3,-1,0,0,0,0), 'volumetric flow' )
_q = new_Quantity0( METER/SECOND**2, 'acceleration' )
#_q = new_Quantity0( (0,1,-3,0,0,0,0), 'jerk' )

_q = new_Quantity0( KILOGRAM*METER/SECOND**2, 'force' )
NEWTON = new_Unit( _q, 1, 'N', 'newton')

_q = new_Quantity0( NEWTON/METER**2, 'pressure' )
PASCAL = new_Unit( _q, 1, 'P', 'pascal')

_q = new_Quantity0( NEWTON*METER, 'energy' )
JOULE = new_Unit( _q, 1, 'J', 'joule' )

_q = new_Quantity0( JOULE/SECOND, 'power')
WATT = new_Unit( _q, 1, 'W', 'watt' )
__maxify(WATT)
__minify(WATT)
DBM = new_Unit( _q, 0, 'dBm', 'dbm' )

_q = new_Quantity0( AMPERE*SECOND, 'charge')
COULOMB = new_Unit( _q, 1, 'C', 'coulomb' )
__minify(COULOMB)

_q = new_Quantity0( JOULE/COULOMB, 'voltage')
VOLT = new_Unit( _q, 1, 'V', 'volt' )
__minify(VOLT)
__maxify(VOLT)

_q = new_Quantity0( COULOMB/VOLT, 'capacitance')
FARAD = new_Unit( _q, 1, 'F', 'farad' )
__minify(FARAD)

_q = new_Quantity0( VOLT/AMPERE, 'resistance')
OHM = new_Unit( _q, 1, 'Ohm', 'ohm' )


''' convenience function to convert length to a frequency
    if this length is an electromagnetic wavelength
    (although the framework has no way of checking this!)    
'''
def __to_frequency(self, unit = TERAHERTZ):
    c = 299792458.0
    wl = self.tof(METER)
    f = c/wl * HERTZ
    return f.to(unit)
LengthQuantity.to_frequency = __to_frequency


# "magically" fill in the C conversion functions of the non-linear units
__c.magical_function( globals() )




