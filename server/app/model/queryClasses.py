from enum import Enum


class Color(Enum):
    black = 'black'
    grey = 'grey'
    white = 'white'
    yellow_brown = 'yellow_brown'
    red_brown = 'red_brown'
    yellow = 'yellow'
    olivegreen = 'olivegreen'
    blue = 'blue'
    orange = 'orange'


# TODO: think of appropriate size measure
class Size(Enum):
    random_size = 'random_size'
    # TODO: drei Größen erstellen


# reference: https://identify.whatbird.com/mwg/20/0/1/10/vals.aspx#Values
class Shape(Enum):
    sparrow_like = 'sparrow_like'
    water_bird_like = 'water_bird_like'
    duck_like = 'duck_like'
    chicken_like = 'chicken_like'
    hawk_like = 'hawk_like'
    owl_like = 'owl_like'
    long_legged_like = 'long_legged_like'
    woodpecker_like = 'woodpecker_like'
    pigeon_like = 'pigeon_like'

# class Region():
#     '''
#     Represents a Birds breeding region

#     short -- region short (like \'NA\')

#     name -- region name (like \'North America\')
#     '''
#     short = None
#     name = None

#     def __init__(self, short: str, name: str):
#         self.short = short
#         self.name = name

#     def __new__(cls, short: str, name: str):
#         cls.short = short
#         cls.name = name
#         return cls

#     def __repr__(self):
#         return self.name


class Breeding(Enum):
    # def __new__(cls, short: str, name: str):
    #     region = str.__new__(cls, [short])
    #     region.short = short
    #     region.name = name
    #     return region

    na = 'NA'
    ma = 'MA'
    sa = 'SA'
    la = 'LA'
    af = 'AF'
    eu = 'EU'
    orr = 'OR'
    au = 'AU'
    ao = 'AO'
    po = 'PO'
    io = 'IO'
    tro = 'TrO'
    to = 'TO'
    no = 'NO'
    so = 'SO'
    an = 'AN'
    soc = 'So. Cone'

    # na = ('NA', 'North America')
    # ma = ('MA', 'Middle America')
    # sa = ('SA', 'South America')
    # la = ('LA', 'Latin America')
    # af = ('AF', 'Africa')
    # eu = ('EU', 'Eurasia')
    # orr = ('OR', 'Oriental Region')
    # au = ('AU', 'Australasia')
    # ao = ('AO', 'Atlantic Ocean')
    # po = ('PO', 'Pacific Ocean')
    # io = ('IO', 'Indian Ocean')
    # tro = ('TrO', 'Tropical Ocean')
    # to = ('TO', 'Temperate Ocean')
    # no = ('NO', 'Northern Ocean')
    # so = ('SO', 'Southern Ocean')
    # an = ('AN', 'Antarctica')
    # soc =('So. Cone', 'Southern Cone')
