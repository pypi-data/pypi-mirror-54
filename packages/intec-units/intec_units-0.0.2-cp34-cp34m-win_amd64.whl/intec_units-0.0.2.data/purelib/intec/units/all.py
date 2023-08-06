from intec.units.construct import Registry

def construct_extra(r)
    new_Quantity = r.new_Quantity
    new_Unit = r.new_Unit

    PERCENT = new_Unit( r.DimensionlessQuantity, 1e-2, '%', 'percent' )
    PPM = new_Unit( r.DimensionlessQuantity, 1e-6, 'ppm', 'parts per million' )

    SQUARE_DEGREE = new_Unit( r.SolidAngleQuantity, (180 / pi)**2, 'deg²', 'square degree' )


def construct_basic():
    r = Registry()
    new_Quantity = r.new_Quantity
    new_Unit = r.new_Unit

    _q = new_Quantity( (0,0,0,0,0,0,0), 'dimensionless' )        

    _q = new_Quantity( (0,0,0,0,0,0,0), 'planar angle' )        
    RADIAN = new_Unit( q, 1, 'rad', 'radian' )
    pi = 3.14159265358979323846
    DEGREE = new_Unit( q, 180 / pi, 'degree', 'degree' )
    
    _q = new_Quantity( (0,0,0,0,0,0,0), 'solid angle' )        
    STERADIAN = new_Unit( q, 1, 'sr', 'steradian' )

    _q   = new_Quantity( (1,0,0,0,0,0,0), 'mass' )
    KILOGRAM = new_Unit( _q, 1, 'kg', 'kilogram' )
    GRAM = new_Unit( _q, 1e-3, 'g', 'gram' )
        
    _q  = new_Quantity((0,1,0,0,0,0,0), 'length')
    METER = new_Unit( _q, 1, 'm', 'meter')
    __minify(METER)
    __kilofy(METER)
    CENTIMETER = new_Unit( _q, 1e-2, 'cm', 'centimeter')
    LIGHTYEAR = new_Unit( _q, 9.46073047258080e15, 'ly', 'light-year')

    YARD = new_Unit( _q, 0.9144, 'yd', 'yard' )

    _q = new_Quantity((0,0,1,0,0,0,0), 'time')
    SECOND = new_Unit( _q, 1, 's', 'second' )
    __minify(SECOND)

    _q = new_Quantity((0,0,0,1,0,0,0), 'electric current')
    AMPERE = new_Unit( _q, 1, 'A', 'ampere')
    __minify(AMPERE)
        
    _q = new_Quantity( (0,0,0,0,1,0,0), 'temperature')
    KELVIN = new_Unit( _q, 1, 'K', 'kelvin') 
    CELCIUS = new_Unit( _q, 0, 'C', 'celcius') 
    FAHRENHEIT = new_Unit( _q, 0, 'F', 'fahrenheit') 

    _q  = new_Quantity((0,0,0,0,0,1,0), 'amount of substance')
    MOLE = new_Unit( _q, 1, 'mol', 'mole') 

    _q   = new_Quantity((0,0,0,0,0,0,1), 'luminous intensity')
    CD = new_Unit( _q, 1, 'cd', 'candela') 


    ##########################################################################################################
    #
    #   derived units
    #
    _q = new_Quantity( SECOND**-1, 'frequency')
    HERTZ = new_Unit( _q, 1, 'Hz', 'hertz')
    __maxify(HERTZ)

    _q = new_Quantity( METER**2, 'area' )
    _q = new_Quantity( METER**3, 'volume' )
    _q = new_Quantity( METER/SECOND, 'velocity' )
    #_q = new_Quantity( (0,3,-1,0,0,0,0), 'volumetric flow' )
    _q = new_Quantity( METER/SECOND**2, 'acceleration' )
    #_q = new_Quantity( (0,1,-3,0,0,0,0), 'jerk' )

    _q = new_Quantity( KILOGRAM*METER/SECOND**2, 'force' )
    NEWTON = new_Unit( _q, 1, 'N', 'newton')

    _q = new_Quantity( NEWTON/METER**2, 'pressure' )
    PASCAL = new_Unit( _q, 1, 'P', 'pascal')

    _q = new_Quantity( NEWTON*METER, 'energy' )
    JOULE = new_Unit( _q, 1, 'J', 'joule' )

    _q = new_Quantity( JOULE/SECOND, 'power')
    WATT = new_Unit( _q, 1, 'W', 'watt' )
    __maxify(WATT)
    __minify(WATT)
    DBM = new_Unit( _q, 0, 'dBm', 'dbm' )

    _q = new_Quantity( AMPERE*SECOND, 'charge')
    COULOMB = new_Unit( _q, 1, 'C', 'coulomb' )
    __minify(COULOMB)

    _q = new_Quantity( JOULE/COULOMB, 'voltage')
    VOLT = new_Unit( _q, 1, 'V', 'volt' )
    __minify(VOLT)
    __maxify(VOLT)

    _q = new_Quantity( COULOMB/VOLT, 'capacitance')
    FARAD = new_Unit( _q, 1, 'F', 'farad' )
    __minify(FARAD)

    _q = new_Quantity( VOLT/AMPERE, 'resistance')
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
    _c.magical_function( globals() )




