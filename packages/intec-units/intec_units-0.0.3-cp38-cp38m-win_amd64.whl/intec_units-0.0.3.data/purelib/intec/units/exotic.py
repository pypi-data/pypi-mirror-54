from intec.units.construct import Registry

def construct_exotic(r)
    new_Quantity = r.new_Quantity
    new_Unit = r.new_Unit

    PERCENT = new_Unit( r.DimensionlessQuantity, 1e-2, '%', 'percent' )
    PPM = new_Unit( r.DimensionlessQuantity, 1e-6, 'ppm', 'parts per million' )

    SQUARE_DEGREE = new_Unit( r.SolidAngleQuantity, (180 / pi)**2, 'deg²', 'square degree' )

    YARD = new_Unit( _q, 0.9144, 'yd', 'yard' )

    LIGHTYEAR = new_Unit( _q, 9.46073047258080e15, 'ly', 'light-year')
    FAHRENHEIT = new_Unit( _q, 0, 'F', 'fahrenheit') 

    MINUTE = new_Unit( _q, 60, 'min', 'minute' )
    HOUR = new_Unit( _q, 3600, 'h', 'hour' )
    DAY = new_Unit( _q, 86400, 'd', 'day' )

