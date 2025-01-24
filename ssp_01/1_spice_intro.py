import spiceypy
import datetime
import math


spiceypy.furnsh('../_kernels/lsk/naif0012.tls')
spiceypy.furnsh('../_kernels/spk/de432s.bsp')

# get today's date
DATE_TODAY = datetime.datetime.today()

# convert the datetime to a string, replacing the time with midnight
DATE_TODAY = DATE_TODAY.strftime('%Y-%m-%dT00:00:00')

# convert the utc midnight string to the corresponding ET
ET_TODAY_MIDNIGHT = spiceypy.utc2et(DATE_TODAY)


# Can we compute now the position and velocity (so called state) of the Earth
# with respect to the Sun? We use the following function to determine the
# state vector and the so called light time (travel time of the light between
# the Sun and our home planet). Positions are always given in km, velocities
# in km/s and times in seconds

# targ : Object that shall be pointed at
# et : The ET of the computation
# ref : The reference frame. Here, it is ECLIPJ2000 (so Medium article)
# obs :  The observer respectively the center of our state vector computation
EARTH_STATE_WRT_SUN, EARTH_SUN_LT = spiceypy.spkgeo(targ=399,
                                                    et=ET_TODAY_MIDNIGHT,
                                                    ref='ECLIPJ2000',
                                                    obs=10)

# The (Euclidean) distance should be around 1 AU. Why "around"? Well the Earth
# revolves the Sun in a slightly non-perfect circle (elliptic orbit). First,
# we compute the distance in km.

EARTH_SUN_DISTANCE = math.sqrt(EARTH_STATE_WRT_SUN[0]**2.0
                               + EARTH_STATE_WRT_SUN[1]**2.0
                               + EARTH_STATE_WRT_SUN[2]**2.0)

# Convert the distance in astronomical units (1 AU)
# Instead of searching for the "most recent" value, we use the default value
# in SPICE. This way, we can easily compare our results with the results of
# others.
EARTH_SUN_DISTANCE_AU = spiceypy.convrt(EARTH_SUN_DISTANCE, 'km', 'AU')


# First, we compute the actual orbital speed of the Earth around the Sun
EARTH_ORB_SPEED_WRT_SUN = math.sqrt(EARTH_STATE_WRT_SUN[3]**2.0
                                    + EARTH_STATE_WRT_SUN[4]**2.0
                                    + EARTH_STATE_WRT_SUN[5]**2.0)


# Now let's compute the theoretical expectation. First, we load a pck file
# that contain miscellanoeus information, like the G*M values for different
# objects

# First, load the kernel
spiceypy.furnsh('../_kernels/pck/gm_de431.tpc')
_, GM_SUN = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)


# Now compute the orbital speed
def V_ORB_FUNC(gm, r):
    return math.sqrt(gm/r)


EARTH_ORB_SPEED_WRT_SUN_THEORY = V_ORB_FUNC(GM_SUN[0], EARTH_SUN_DISTANCE)


if __name__ == '__main__':
    print('State vector of the Earth w.r.t. the Sun for "today" (midnight):\n',
          EARTH_STATE_WRT_SUN)
    print(f"Earth Sun distance in km: {EARTH_SUN_DISTANCE}")
    print('Current distance between the Earth and the Sun in AU:',
          EARTH_SUN_DISTANCE_AU)
    # It's around 30 km/s
    print('Current orbital speed of the Earth around the Sun in km/s:',
          EARTH_ORB_SPEED_WRT_SUN)
    print('Theoretical orbital speed of the Earth around the Sun in km/s:',
          EARTH_ORB_SPEED_WRT_SUN_THEORY)
