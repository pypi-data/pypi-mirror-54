import intec.units.si as r

new_Quantity = r.new_Quantity
new_Unit = r.new_Unit

PERCENT = new_Unit( r.DimensionlessQuantity, 1e-2, '%', 'percent' )
PPM = new_Unit( r.DimensionlessQuantity, 1e-6, 'ppm', 'parts per million' )

#SQUARE_DEGREE = new_Unit( r.SolidAngleQuantity, (180 / pi)**2, 'deg²', 'square degree' )

YARD = new_Unit( r.meter, 0.9144, 'yd', 'yard' )

LIGHTYEAR = new_Unit( r.meter, 9.46073047258080e15, 'ly', 'light-year')

MINUTE = new_Unit( r.second, 60, 'min', 'minute' )
HOUR = new_Unit( r.second, 3600, 'h', 'hour' )
DAY = new_Unit( r.second, 86400, 'd', 'day' )

