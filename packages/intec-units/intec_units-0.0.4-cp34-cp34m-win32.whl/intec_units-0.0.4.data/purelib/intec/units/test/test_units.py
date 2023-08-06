# -*- coding: utf-8 -*-

import unittest
import math
                
class test_units(unittest.TestCase):

    def test_dimensionless(self):
        from intec.units.construct import Registry
        r = Registry()
        new_Quantity = r.new_Quantity
        new_Unit = r.new_Unit

        q = new_Quantity( (0,0,0,0,0,0,0), 'dimensionless' )    
        self.assertIsInstance(q, type)
        
        PERCENT = new_Unit( q, 1e-2, '%', 'percent' )
        PPM = new_Unit( q, 1e-6, 'ppm', 'parts per million' )

        q = 1*PERCENT+1*PPM
        self.assertEqual(q.m, 1.0001)
        self.assertEqual(q.u, PERCENT)
        
        q = 1*PERCENT*1*PPM
        self.assertIsInstance(q, float)
        self.assertEqual(q, 1e-8)
        
        q = PERCENT*PPM
        self.assertIsInstance(q, float)
        self.assertEqual(q, 1e-8)

        q = PERCENT*1*PPM
        self.assertIsInstance(q, float)
        self.assertEqual(q, 1e-8)

        q = 1*PERCENT*PPM
        self.assertIsInstance(q, float)
        self.assertEqual(q, 1e-8)
            
        q = new_Quantity( (0,0,0,0,0,0,0), 'planar angle' )        
        RADIAN = new_Unit( q, 1, 'rad', 'radian' )
        pi = 3.14159265358979323846
        DEGREE = new_Unit( q, pi / 180, 'degree', 'degree' )
        
        q = pi/2*RADIAN + 90*DEGREE
        self.assertEqual(q.m, pi)
        
        with self.assertRaises(TypeError):
            q = 1*PERCENT + 1*RADIAN
        with self.assertRaises(TypeError):
            q = 1*RADIAN + 1*PERCENT
        with self.assertRaises(TypeError):
            q = 1*PERCENT + 1*DEGREE
        
        q = new_Quantity( (0,0,0,0,0,0,0), 'solid angle' )        
        STERADIAN = new_Unit( q, 1, 'sr', 'steradian' )
        SQUARE_DEGREE = new_Unit( q, (180 / pi)**2, 'deg²', 'square degree' )
        a = 1*STERADIAN
        self.assertEqual( str(a), "1.000000 sr")
        a = 1*SQUARE_DEGREE
        self.assertEqual( str(a), "1.000000 deg²")
        
    
    def test_si(self):
        from intec.units.construct import Unit
        from intec.units.si import METER, KILOMETER, SECOND
        
        a = METER/SECOND
        self.assertEqual(type(a),Unit)
        a = KILOMETER/SECOND
        self.assertEqual(type(a),Unit)
        b = KILOMETER/SECOND
        self.assertEqual(a, b)
        self.assertIs(a, b)
        
        from intec.units.si import MILLISECOND, CENTIMETER
        
        c = METER/MILLISECOND
        self.assertEqual(a, c)
        self.assertIsNot(a, c)
        d = METER/SECOND
        self.assertTrue(d != c)
        self.assertTrue(d < c)
        self.assertTrue(d <= c)
        self.assertFalse(d == c)
        self.assertFalse(d > c)
        self.assertFalse(d >= c)

        a = 1 * KILOMETER ** 3
        self.assertTrue(a == 10 ** 9 * METER ** 3)

        a = 1 * METER
        self.assertEqual((a**2).unit.dims, (0, 2, 0, 0, 0, 0, 0))
        self.assertEqual((a**3).unit.dims, (0, 3, 0, 0, 0, 0, 0))
        self.assertEqual((a**-4).unit.dims, (0, -4, 0, 0, 0, 0, 0))
        self.assertEqual((a**-44).unit.dims, (0, -44, 0, 0, 0, 0, 0))

        from intec.units.si import KELVIN, AMPERE, VelocityQuantity, HERTZ, NEWTON, GRAM
        a = 1.234556789012 * a
        a = 12 * KELVIN**2
            
        
        1 * KILOMETER ** 127
        with self.assertRaises( OverflowError):
            1 * KILOMETER ** 128
        with self.assertRaises( OverflowError):
            (1 * KILOMETER ** 127) * KILOMETER
        1 * KILOMETER ** -127
        1 * KILOMETER ** -128
        with self.assertRaises( OverflowError):
            1 * KILOMETER ** -129
        with self.assertRaises( OverflowError):
            (1 * KILOMETER ** -128) / KILOMETER
        a = 1 * KILOMETER ** -120
        a**-1
        with self.assertRaises( OverflowError):
            a**2
        with self.assertRaises( OverflowError):
            a**-2
        
        self.assertTrue( (1*KILOMETER+1*METER).m == 1.001 )
        self.assertTrue( (1*KILOMETER+1*METER).unit is KILOMETER )
        self.assertTrue( (1*METER+1*KILOMETER).m == 1001 )
        self.assertTrue( (1*CENTIMETER+1*KILOMETER).unit == CENTIMETER )
        
        with self.assertRaisesRegex( TypeError, r"Cannot convert unit \[A\] to unit \[km\]"):
            1*KILOMETER+1*AMPERE
        
        q = 2*KILOMETER/SECOND
        self.assertTrue( type(q) is VelocityQuantity )
            
        q = 5*HERTZ    
        q2 = 1/q
        self.assertTrue( q2.unit.dims == SECOND.dims )
        
        with self.assertRaises(TypeError):
            NEWTON + METER    
        with self.assertRaises(TypeError):
            1 + METER
        with self.assertRaises(TypeError):
            METER + 1
        with self.assertRaises(TypeError):
            METER + 'a'
        #with self.assertRaises(TypeError):
        #    METER + np.zeros( (8,) )
        #with self.assertRaises(TypeError):
        #    np.zeros( (8,) ) + METER
        with self.assertRaises(TypeError):
            []*5*NEWTON
        with self.assertRaises(TypeError):
            5*NEWTON*[]
    
        self.assertTrue( (5*NEWTON).unit is NEWTON )
        self.assertTrue( 5*5*NEWTON == 25*NEWTON )
        self.assertTrue( 5*(5*NEWTON) == 25*NEWTON )
        self.assertTrue( 5*NEWTON*5 == 25*NEWTON )
        self.assertTrue( NEWTON*5*5 == 25*NEWTON )
            
        self.assertTrue( 5*(NEWTON*METER) > 4*NEWTON*METER ) 
        self.assertTrue( NEWTON*5*METER > 4*NEWTON*METER ) 
        self.assertTrue( NEWTON*METER*5 > 4*NEWTON*METER ) 
        self.assertTrue( KILOMETER*NEWTON*5 > 4*NEWTON*METER ) 
        
        from intec.units.si import ForceQuantity, CELCIUS, MICROMETER, MILLIMETER
        self.assertTrue( type( 5*GRAM*CENTIMETER/SECOND**2 ) is ForceQuantity )
        
        import intec.units.si as r
        ZoinkQuantity = r.new_Quantity( METER**10/SECOND**7, 'zoink' )
        self.assertTrue( type(7*METER**10/SECOND**7) is ZoinkQuantity )
        
        self.assertTrue( KILOMETER >= KILOMETER )
        self.assertTrue( KILOMETER > 1e5*MICROMETER )
        with self.assertRaisesRegex( TypeError, r"Cannot convert unit \[km\] to unit \[A\]"):
            KILOMETER < AMPERE
        
        t1 = 3*CELCIUS
        self.assertEqual(t1.to(KELVIN).magnitude, 276.15)
        t2 = 100*KELVIN
        self.assertTrue( t1 > t2 )
        self.assertTrue( t2 < t1 )
        self.assertTrue( t2.near(-173.15*CELCIUS) )
            
        q = r.Quantity(10, CENTIMETER)
        self.assertTrue( type(q) is r.LengthQuantity )
        #q = r.TemperatureQuantity(10, CENTIMETER)
        #self.assertTrue( type(q) is TemperatureQuantity
            
            
        PERCENT = r.new_Unit( r.DimensionlessQuantity, 1e-2, '%', 'percent' )
        PPM = r.new_Unit( r.DimensionlessQuantity, 1e-6, 'ppm', 'parts per million' )
        PERMIL = r.new_Unit( r.DimensionlessQuantity, 1e-3, "per mil", "per mil")
        pi = 3.14159265358979323846
        SQUARE_DEGREE = r.new_Unit( r.SolidAngleQuantity, (180 / pi)**2, 'deg²', 'square degree' )
        YARD = r.new_Unit( METER, 0.9144, 'yd', 'yard' )
        LIGHTYEAR = r.new_Unit( METER, 9.46073047258080e15, 'ly', 'light-year')
        MINUTE = r.new_Unit( SECOND, 60, 'min', 'minute' )
        HOUR = r.new_Unit( SECOND, 3600, 'h', 'hour' )
        DAY = r.new_Unit( SECOND, 86400, 'd', 'day' )
        POUND = r.new_Unit( r.KILOGRAM, 0.45359237, 'lb', 'pound' )
        
            
        q0 = 5*PERCENT
        q1 = 10*CENTIMETER
        q2 = 1.3*METER
        q3 = 3*AMPERE
        
        self.assertEqual(q0, 0.05)
        
        self.assertTrue( 1*PERMIL == 0.001 )
        self.assertTrue( q0 > 5*PERMIL )
        
        with self.assertRaisesRegex( TypeError, r"Cannot convert unit \[cm\] to unit \[A\]"):
            q1 > AMPERE
        with self.assertRaisesRegex( TypeError, r"Cannot convert unit \[cm\] to dimensionless number"):
            10 != q1
        with self.assertRaisesRegex( TypeError, r"Cannot convert unit \[cm\] to dimensionless number"):
            q1 < 10
        self.assertTrue( MILLIMETER < q2 )
        self.assertTrue( q1 > MILLIMETER )
        self.assertTrue( q1 <= q2 )
        with self.assertRaisesRegex(TypeError, "Cannot convert"):
            q1 != q3
        

        q = 10*CENTIMETER
        
        self.assertTrue( q > CENTIMETER )
        self.assertTrue( q >= CENTIMETER )
        self.assertTrue( q != CENTIMETER )
        self.assertTrue( q == 0.1*METER )
        self.assertTrue( q < KILOMETER )
        self.assertTrue( q <= KILOMETER )
        self.assertTrue( q > 9.99*CENTIMETER )
        self.assertTrue( q > 1*MILLIMETER )
        self.assertTrue( q >= 8*CENTIMETER )
        self.assertTrue( q >= 1*MILLIMETER )
        self.assertTrue( q < 2*LIGHTYEAR )
        self.assertTrue( q < 1*METER )
        self.assertTrue( q <= 2*LIGHTYEAR )
        self.assertTrue( q <= 1*METER )
        self.assertTrue( q == .10*METER )
        self.assertTrue( q == 10*CENTIMETER )
        self.assertTrue( q == 100*MILLIMETER )
        self.assertTrue( q >= 10*CENTIMETER )
        self.assertTrue( q >= 100*MILLIMETER )
        self.assertTrue( q <= 10*CENTIMETER )
        self.assertTrue( q <= 100*MILLIMETER )
        
        q = 2/KILOMETER
        #self.assertTrue( str(q) == "2. 1/km"
        q2 = q * MILLIMETER
        self.assertEqual( q2, 0.000002)
        
        from intec.units.si import KILOWATT, MILLIWATT, MILLIAMPERE, DBM, LengthQuantity, ATTOMETER, WATT, NANOMETER, TERAHERTZ
        
        self.assertTrue( type(KILOWATT/MILLIWATT) == float )
        self.assertTrue( KILOWATT/MILLIWATT == 1e6 )
        self.assertTrue( MILLIWATT/KILOWATT == 1e-6 )
        
        import sys
        rc = sys.getrefcount(MILLIWATT/KILOWATT)
        self.assertTrue( rc == sys.getrefcount(MILLIWATT/KILOWATT) )
        self.assertTrue( rc == sys.getrefcount(MILLIWATT/KILOWATT) )
        self.assertTrue( rc == sys.getrefcount(MILLIWATT/KILOWATT) )
        
        q = 2/PERCENT
        self.assertTrue( q == 200 )
        
        self.assertTrue( MILLIAMPERE/MILLIAMPERE == 1 )
        q = KILOMETER/2
        self.assertTrue( q.unit is KILOMETER )
        self.assertTrue( float(q.to(METER))==500 )
                
        with self.assertRaisesRegex( TypeError, r"Cannot multiply non-linear unit \[dBm\] with other unit"):
            DBM*METER
        with self.assertRaisesRegex( TypeError, r"Cannot multiply non-linear unit \[.C\] with other unit"):
            METER*CELCIUS
        
        q = 5*SECOND**-1
        # self.assertTrue( q.unit.qtype is r.FrequencyQuantity  ???
            
        q2 = q*20

        q2 = 2*MINUTE
        q3 = q*q2
        self.assertTrue( q3 == 600 )
        
        q = HERTZ*HOUR
        self.assertTrue( q == 3600 )
        self.assertTrue( q is HERTZ*HOUR )
        
        u = PERCENT*PERCENT
        self.assertTrue( u == 0.0001 )
        self.assertTrue( u == PERCENT*PERCENT )
        q = 5*PERCENT
        q *= 5
        self.assertTrue( q.unit is PERCENT )
        self.assertTrue( q.m == 25 )

            
        AU = r.new_Unit( METER, 149597870700, "AU", "astronomical unit" )
        self.assertTrue( AU.factor == 149597870700 )
        self.assertTrue( AU.qtype is LengthQuantity )
        q = (5*AU).to(KILOMETER)
        
        f = 1/math.tan( math.radians(1.0/3600) )    
        PARSEC = r.new_Unit( AU, f, "Pc", "parsec")
        self.assertTrue( (1*PARSEC).near( 3.26*LIGHTYEAR, .01 ) )
        self.assertTrue(not (1*PARSEC).near( 3.26*LIGHTYEAR, .001 ) )
        q = PARSEC.to(LIGHTYEAR)
        self.assertTrue(q.unit is LIGHTYEAR)
        self.assertTrue(int(q.m) == 3)
        
        self.assertTrue( METER.dims == (0,1,0,0,0,0,0) )
        u = METER**2
        self.assertTrue( u.dims == (0,2,0,0,0,0,0) )
        self.assertTrue( u is METER**2 )
        self.assertTrue( str(u) == "m^2" )
        u = u**2
        self.assertTrue( str(u) == "(m^2)^2" )
        self.assertTrue( u.dims == (0,4,0,0,0,0,0) )
        u = u**8
        self.assertTrue( u.dims == (0,32,0,0,0,0,0) )
        with self.assertRaisesRegex( OverflowError, "Dimension of unit 'meter': 256"):
            u = u**8
        u = METER*METER
        self.assertTrue( u.dims == (0,2,0,0,0,0,0) )
        
        self.assertTrue( ATTOMETER.name == 'attometer' )
        self.assertTrue( ATTOMETER.symbol == 'am' )
        self.assertTrue( ATTOMETER.factor == 1e-18 )

        q1 = 1008e+17*ATTOMETER
        self.assertTrue( q1.near( 100.8*METER ) )
        self.assertTrue( q1.to(METER).near( 100.8*METER ) )
        self.assertTrue( not (100.008*METER).near(100.007*METER) )
        
        q1 = 0*DBM
        q2 = q1.to(WATT)
        self.assertTrue( q2.m == 0.001 )
        self.assertTrue( q2.unit is WATT )
        q2 = q1.to(MILLIWATT)
        self.assertTrue( q2.m == 1 )

        q2 = 30*DBM
        q3 = q2.to(WATT)
        self.assertTrue( q3.m == 1 )
        q4 = q2 + q3
        
        SQUARE_YARD = YARD*YARD
        self.assertTrue( YARD*YARD is SQUARE_YARD )
        self.assertTrue( SQUARE_YARD.symbol == 'yd.yd' )
        self.assertTrue( SQUARE_YARD.qtype is r.AreaQuantity )
        
        q1 = 5 * SQUARE_YARD
        self.assertTrue( q1.unit is YARD*YARD )
        q1 = 5 * q1
        self.assertTrue( q1.unit is YARD*YARD )
        self.assertTrue( q1.m == 25 )
        
        self.assertTrue( q1.to(SQUARE_YARD) is q1 )
        self.assertTrue( q1.to(YARD*YARD) is q1 )
        with self.assertRaisesRegex(TypeError, "Cannot convert"):
            q1.to(POUND)
        q2 = q1.to(METER*METER)
        self.assertTrue( type(q2) is r.AreaQuantity )
        self.assertTrue( q2.m == 20.903184 )
            
        with self.assertRaisesRegex(TypeError, "must be Unit, not str"):
            q1 = r.Quantity(10.0, "kelvin")
        with self.assertRaisesRegex(TypeError, "function takes exactly 2 arguments"):
            q1 = r.Quantity(10.0, KELVIN, 1)        
        q1 = r.Quantity(5.0, KELVIN)
        self.assertTrue( q1.m == 5.0 )
        self.assertTrue( q1.unit is KELVIN )
        self.assertTrue( float(q1) == 5.0 )
        
        with self.assertRaisesRegex(AttributeError, "attribute 'm' of 'Quantity' objects is not writable"):
            q1.m = 3
        with self.assertRaisesRegex(AttributeError, "attribute 'unit' of 'Quantity' objects is not writable"):
            q1.unit = KELVIN
        
        q1 = -3*KELVIN
        self.assertTrue( q1.m == -3.0 )
        self.assertTrue( q1.unit is KELVIN )
        
        q1 = POUND*3
        self.assertTrue( q1.m == 3.0 )
        self.assertTrue( q1.unit is POUND )

        b = 5555555555566666666666665555555555555555555555555555555555555555555555555555555555555555
        q1 = b*KELVIN
        self.assertTrue( type(q1) == r.ThermodynamicTemperatureQuantity )
        self.assertTrue( q1.m == float(b) )
        self.assertTrue( q1.unit is KELVIN )
        
        q1 = POUND*.035
        self.assertTrue( type(q1) == r.MassQuantity )
        self.assertTrue( q1.m == .035 )
        self.assertTrue( q1.unit is POUND )   
        n1 = sys.getrefcount(POUND)
        q2 = q1 + 5*POUND
        self.assertTrue( -q2.m == -5.035 )
        self.assertTrue( q2.unit is POUND  )   
        self.assertTrue( sys.getrefcount(POUND) == n1+1 )
        del q2
        self.assertTrue( sys.getrefcount(POUND) == n1 )
        
        self.assertTrue( (5*5*KELVIN*5*5).m == 625 )
    
        with self.assertRaisesRegex( OverflowError, "int too large to convert to float"):    
            300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000*q1

            
        from intec.units.si import JOULE, KILOGRAM, PASCAL
        
        with self.assertRaises(TypeError):
            1/SECOND > 2*SECOND
        
        self.assertTrue( (1550*NANOMETER).to_frequency() > 193.41 * TERAHERTZ )
        self.assertTrue( (1550*NANOMETER).to_frequency() < 193.42 * TERAHERTZ )
        self.assertTrue( (1550*NANOMETER).to_frequency(HERTZ) > 193.41 * TERAHERTZ )
        
        self.assertTrue( 5*NEWTON*METER*KILOMETER*3 == 5*NEWTON*(METER*KILOMETER)*3 )
        self.assertTrue( (5*METER)*(5*METER) == 25 * METER**2 )
        self.assertTrue( METER*5 == 2.5*METER*2 )
        self.assertTrue( METER*(5*NEWTON) == JOULE*5 )
        self.assertTrue( 1*METER*5*NEWTON == 1*(METER*5*NEWTON) )
        self.assertTrue( 1*METER*(5*NEWTON) == 5*JOULE )
        
        with self.assertRaises(TypeError):
            1*METER == 1*JOULE    
        with self.assertRaises(TypeError):
            DBM*SECOND        
        with self.assertRaises(TypeError):
            (5*SECOND)*DBM    
        with self.assertRaises(TypeError):
            (5*DBM)*SECOND
        with self.assertRaises(TypeError):
            SECOND*(5*DBM)
        with self.assertRaises(TypeError):
            DBM*(5*SECOND)
        with self.assertRaises(TypeError):
            SECOND*DBM
        
        q1 = 5*KILOMETER 
        q2 = q1.to(METER)
        self.assertTrue( q1 == q2 )
        self.assertTrue( q2.unit == METER )
        self.assertTrue( q2.m == 5000 )
        #print( str((5*GRAM).to(KILOGRAM)) )
        #self.assertTrue( str((5*GRAM).to(KILOGRAM)) == '0.005 kg'
        self.assertTrue( (10*DBM).to(WATT) == 10*DBM )
        self.assertTrue( (10*DBM).to(DBM).m == 10 ) 
            
        from intec.units.si import PICOMETER            
        with self.assertRaises(TypeError):
            5 == 3*PICOMETER
        with self.assertRaises(TypeError):
            (10*WATT).to(DBM) == 10
        self.assertTrue( (0*CELCIUS).to(KELVIN).m == 273.15 )
        #self.assertTrue( str( (0*KELVIN).to(CELCIUS) ) ==  "-273.150 C"
        with self.assertRaisesRegex(TypeError, "Cannot convert"):
            (5*GRAM).to(NEWTON)

        self.assertTrue( 5*NEWTON + 7*NEWTON == 12*NEWTON )
        self.assertTrue( 1*KILOMETER + 1*METER > 1000 * METER )
        with self.assertRaisesRegex(TypeError, "Cannot convert"):
            1*METER + 1*NEWTON
            
        self.assertTrue( 1*JOULE + 1*NEWTON*METER == WATT*2*SECOND )    
        self.assertTrue( 1*METER/SECOND * HOUR == 3.6*KILOMETER )
        self.assertTrue( 1 == 1*WATT*SECOND / (1*NEWTON*METER) )
        self.assertTrue( 1/SECOND*HOUR == 3600 )
        q1 = 1*HERTZ
        q2 = 1/SECOND
        q3 = 1*SECOND**-1
        self.assertTrue( q1 + q2 == 2*HERTZ )
        self.assertTrue( q2 + q3 == 2*HERTZ )
        self.assertTrue( q3 + q1 == 2*HERTZ )
        with self.assertRaises(TypeError):
            NEWTON + NEWTON

        q = 100*WATT * 10*PERCENT
        self.assertTrue( q.m == 1000 )
        self.assertTrue( q.to(WATT).m == 10 )
        q = 100*WATT * (10*PERCENT)
        self.assertTrue( q.m == 1000 )
        
        self.assertTrue( 1*METER*(KILOGRAM/SECOND**2) == 1*NEWTON )
        
        self.assertTrue( (1*METER*KILOGRAM/(METER*PASCAL)).unit.symbol == 'm.kg/(m.P)' )
        self.assertTrue( 5*PERCENT*2 == 0.10 )
        str(5*PERCENT*(5*PERCENT))
        self.assertTrue( 1*WATT == 1000*MILLIWATT )
        self.assertTrue( 1*WATT > 500*MILLIWATT )
        self.assertTrue( not 1*WATT < 500*MILLIWATT )
        self.assertTrue( 5*METER*METER*5 == 250000*CENTIMETER**2 )
        self.assertTrue( (5*METER)**2 == (500*CENTIMETER)**2 )
        self.assertTrue( 23*CENTIMETER**2 == 23*(CENTIMETER**2) )
        '''
        self.assertTrue( repr(CENTIMETER**2) == 'x'
        type(5*CENTIMETER)
        print repr(5*CENTIMETER)
        print repr(5*CENTIMETER*CENTIMETER)
        print repr( LengthQuantity(5,CENTIMETER) )
        print repr(1*KILOMETER + 1*NANOMETER  )
        print CENTIMETER
        self.assertTrue( 4*KELVIN-6*KELVIN == -2*KELVIN
        '''



if __name__ == '__main__':
    unittest.main()
        
        