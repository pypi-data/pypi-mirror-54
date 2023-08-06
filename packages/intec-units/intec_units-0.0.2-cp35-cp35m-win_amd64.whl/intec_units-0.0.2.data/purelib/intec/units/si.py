from . import intecunits as _c
from intec.units.construct import Registry

def si_base(r):
    new_Quantity = r.new_Quantity
    new_Unit = r.new_Unit

    ##########################################################################################################
    #
    #   SI base units
    #
    _q = new_Quantity( (0,0,0,0,0,0,0), 'dimensionless' )        

    _q   = new_Quantity( (1,0,0,0,0,0,0), 'mass' )
    new_Unit( _q, 1, 'kg', 'kilogram' )
        
    _q  = new_Quantity((0,1,0,0,0,0,0), 'length')
    new_Unit( _q, 1, 'm', 'meter')

    _q = new_Quantity((0,0,1,0,0,0,0), 'time')
    new_Unit( _q, 1, 's', 'second' )

    _q = new_Quantity((0,0,0,1,0,0,0), 'electric current')
    new_Unit( _q, 1, 'A', 'ampere')
        
    _q = new_Quantity( (0,0,0,0,1,0,0), 'thermodynamic temperature')
    new_Unit( _q, 1, 'K', 'kelvin') 

    _q  = new_Quantity((0,0,0,0,0,1,0), 'amount of substance')
    new_Unit( _q, 1, 'mol', 'mole') 

    _q   = new_Quantity((0,0,0,0,0,0,1), 'luminous intensity')
    new_Unit( _q, 1, 'cd', 'candela') 
    

def si_derived(r):
    new_Quantity = r.new_Quantity
    new_Unit = r.new_Unit
    
    ##########################################################################################################
    #
    #   derived units
    #    
    _q = new_Quantity( (0,0,0,0,0,0,0), 'plane angle' )        
    new_Unit( _q, 1, 'rad', 'radian' )
    
    _q = new_Quantity( (0,0,0,0,0,0,0), 'solid angle' )        
    new_Unit( _q, 1, 'sr', 'steradian' )
    
    _q = new_Quantity( r.second**-1, 'frequency')
    new_Unit( _q, 1, 'Hz', 'hertz')

    _q = new_Quantity( r.meter**2, 'area' )
    
    _q = new_Quantity( r.meter**3, 'volume' )
    
    _q = new_Quantity( r.meter/r.second, 'velocity' )
    
    _q = new_Quantity( r.meter/r.second**2, 'acceleration' )
    
    _q = new_Quantity( r.meter/r.second**3, 'jerk' )
    
    _q = new_Quantity( r.kilogram*r.meter/r.second**2, 'force' )
    new_Unit( _q, 1, 'N', 'newton')

    _q = new_Quantity( r.newton/r.meter**2, 'pressure' )
    new_Unit( _q, 1, 'P', 'pascal')

    _q = new_Quantity( r.newton*r.meter, 'energy' )
    new_Unit( _q, 1, 'J', 'joule' )

    _q = new_Quantity( r.joule/r.second, 'power')
    new_Unit( _q, 1, 'W', 'watt' )

    _q = new_Quantity( r.ampere*r.second, 'charge')
    new_Unit( _q, 1, 'C', 'coulomb' )

    _q = new_Quantity( r.joule/r.coulomb, 'voltage')
    new_Unit( _q, 1, 'V', 'volt' )

    _q = new_Quantity( r.coulomb/r.volt, 'capacitance')
    new_Unit( _q, 1, 'F', 'farad' )

    _q = new_Quantity( r.volt/r.ampere, 'electric resistance')
    new_Unit( _q, 1, 'Ω', 'ohm' )

    _q = new_Quantity( r.ampere/r.volt, 'electric conductance')
    new_Unit( _q, 1, 'S', 'siemens' )

    _q = new_Quantity( r.volt*r.second, 'magnetic flux')
    new_Unit( _q, 1, 'Wb', 'weber' )

    _q = new_Quantity( r.weber/r.meter**2, 'magnetic flux density')
    new_Unit( _q, 1, 'T', 'tesla' )

    _q = new_Quantity( r.weber/r.ampere, 'inductance')
    new_Unit( _q, 1, 'H', 'henry' )
    
    _q = new_Quantity( r.candela*r.steradian, 'luminous flux')
    new_Unit( _q, 1, 'lm', 'lumen' )

    _q = new_Quantity( r.lumen/r.meter**2, 'illuminance')
    new_Unit( _q, 1, 'lx', 'lux' )

    _q = new_Quantity( r.second**-1, 'activity')
    new_Unit( _q, 1, 'Bq', 'becquerel' )

    _q = new_Quantity( r.joule/r.kilogram, 'absorbed dose')
    new_Unit( _q, 1, 'Gy', 'gray' )

    _q = new_Quantity( r.joule/r.kilogram, 'dose equivalent')
    new_Unit( _q, 1, 'Sv', 'sievert' )


    pi = 3.14159265358979323846
    new_Unit( r.radian, pi/180, 'degree', 'degree' )

    new_Unit( r.kilogram, 1e-3, 'g', 'gram' )
    new_Unit( r.meter, 1e-2, 'cm', 'centimeter')
    
    new_Unit( r.watt, 0, 'dBm', 'dBm' )
    new_Unit( r.kelvin, 0, '°C', 'Celcius') 

    # "magically" fill in the C conversion functions of the non-linear units
    _c.magical_function( r.__dict__ )
    
    ''' convenience function to convert length to a frequency
        if this length is an electromagnetic wavelength
        (although the framework has no way of checking this!)    
    '''
    def __to_frequency(self, unit = r.terahertz):
        c = 299792458.0
        wl = self.tof(r.METER)
        f = c/wl * r.HERTZ
        return f.to(unit)
    r.LengthQuantity.to_frequency = __to_frequency





r = Registry()
r.__name__ = __name__
r.__file__ = __file__
si_base(r)
si_derived(r)
r.uppercase_units()
r.Quantity = _c.Quantity

import sys
sys.modules[__name__] = r



