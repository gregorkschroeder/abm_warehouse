import logging
import os
from itertools import chain

from vladiate import Vlad  # https://github.com/di/vladiate
from vladiate import logs
from vladiate.inputs import LocalFile
from vladiate.validators import UniqueValidator, SetValidator, FloatValidator, \
    RangeValidator, IntValidator, Ignore, RegexValidator

# initialize empty logfile
log_path = "../log_files/validator_log.txt"
try:
    os.remove(log_path)
except OSError as e:
    pass

# overwrite the vladiate package logger to write to an output file
logs.logger = logging.getLogger("vlad_logger")
logs.logger.setLevel(logging.INFO)
sh = logging.FileHandler(filename=log_path, mode="a")
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter("%(message)s"))
logs.logger.addHandler(sh)
logs.logger.propagate = False


# create vladiator class for airport_out.csv
class AirportTripsValidator(Vlad):
    """ Vladiate validator class for the airport model trips output
        comma-delimited file specifying the file schema.

    AirportTripsValidator(
        source=LocalFile("../test_files/output/airport_out.csv")
        ).validate()
    """
    validators = {
        "id": [
            IntValidator(),
            UniqueValidator()
            # ordered surrogate key
        ],
        "direction": [
            SetValidator(["0", "1"])
            # 0 - origin is airport MGRA
            # 1 - destination is airport MGRA
        ],
        "purpose": [
            SetValidator(["0", "1", "2", "3", "4"])
            # 0 - Resident Business
            # 1 - Resident Personal
            # 2 - Visitor Business
            # 3 - Visitor Personal
            # 4 - External
        ],
        "size": [
            SetValidator(["0", "1", "2", "3", "4", "5"])
            # party size 1-5+
        ],
        "income": [
            SetValidator(["0", "1", "2", "3", "4", "5", "6", "7"])
            # 0 - Less than 25k
            # 1 - 25k-50k
            # 2 - 50k-75k
            # 3 - 75k-100k
            # 4 - 100k-125k
            # 5 - 125k-150k
            # 6 - 150k-200k
            # 7 - 200k+
        ],
        "nights": [
            SetValidator([str(x) for x in range(0, 15)])
            # nights stayed 0-14+
        ],
        "departTime": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "originMGRA": [
            SetValidator([str(x) for x in chain(range(-99, -98), range(1, 23003))])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in chain(range(-99, -98), range(1, 23003))])
        ],
        "tripMode": [
            SetValidator([str(x) for x in chain(range(-99, -98), range(1, 26))])
            # -99 - Uknown
            # 1 - Drive Alone Free
            # 2 - Drive Alone Pay
            # 3 - Shared Ride 2 General Purpose
            # 4 - Shared Ride 2 HOV
            # 5 - Shared Ride 2 Pay
            # 6 - Shared Ride 3 General Purpose
            # 7 - Shared Ride 3 HOV
            # 8 - Shared Ride 3 Pay
            # 9 - Walk
            # 10 - Bike
            # 11 - Walk to Local
            # 12 - Walk to Express
            # 13 - Walk to BRT
            # 14 - Walk to Light Rail
            # 15 - Walk to Commuter Rail
            # 16 - Park Ride Local
            # 17 - Park Ride Express
            # 18 - Park Ride BRT
            # 19 - Park Ride Light Rail
            # 20 - Park Ride Commuter Rail
            # 21 - Kiss Ride Local
            # 22 - Kiss Ride Express
            # 23 - Kiss Ride BRT
            # 24 - Kiss Ride Light Rail
            # 25 - Kiss Ride Commuter Rail
        ],
        "arrivalMode": [
            SetValidator([str(x) for x in chain(range(-99, -98), range(1, 10))])
            # 1 - Parking lot terminal
            # 2 - Parking lot off-site San Diego Airport area
            # 3 - Parking lot off-site private
            # 4 - Pickup/Drop-off escort
            # 5 - Pickup/Drop-off curbside
            # 6 - Rental car
            # 7 - Taxi
            # 8 - Shuttle/Van/Courtesy Vehicle
            # 9 - Transit
        ],
        "boardingTAP": [
            IntValidator()
        ],
        "alightingTAP": [
            IntValidator()
        ]
    }


# create vladiator class for crossBorderTours.csv
class CrossBorderToursValidator(Vlad):
    """ Vladiate validator class for the cross border model tour output
        comma-delimited file specifying the file schema.

    CrossBorderToursValidator(
        source=LocalFile("../test_files/output/crossBorderTours.csv")
        ).validate()
    """
    validators = {
        "id": [
            IntValidator(),
            UniqueValidator()
            # ordered surrogate key
        ],
        "purpose": [
            SetValidator(["0", "1", "2", "3", "4", "5"])
            # 0 - Work
            # 1 - School
            # 2 - Shop
            # 3 - Cargo
            # 4 - Visit
            # 5 - Other
        ],
        "sentri": [
            SetValidator(["false", "true"])
        ],
        "poe": [
            SetValidator(["0", "1", "2"])
            # 0 - San Ysidro
            # 1 - Otay Mesa
            # 2 - Tecate
        ],
        "departTime": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "arriveTime": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "originMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "originTAZ": [ # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "destinationTAZ": [ # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "tourMode": [
            SetValidator(["1", "2", "3", "4"])
            # 1 - Drive Alone
            # 2 - Shared Ride 2
            # 3 - Shared Ride 3+
            # 4 - Walk
        ]
    }


# create vladiator class for crossBorderTrips.csv
class CrossBorderTripsValidator(Vlad):
    """ Vladiate validator class for the cross border model trip output
        comma-delimited file specifying the file schema.

    CrossBorderTripsValidator(
        source=LocalFile("../test_files/output/crossBorderTrips.csv")
        ).validate()
    """
    validators = {
        "tourID": [
            IntValidator(),
            UniqueValidator(unique_with=["tripID"])
            # file ordered by ["tourID", "tripID"]
        ],
        "tripID": [
            IntValidator(),
            # file ordered by ["tourID", "tripID"]
        ],
        "originPurp": [
            SetValidator(["-1", "0", "1", "2", "3", "4", "5"])
            # -1 - Unknown
            # 0 - Work
            # 1 - School
            # 2 - Shop
            # 3 - Cargo
            # 4 - Visit
            # 5 - Other
        ],
        "destPurp": [
            SetValidator(["-1", "0", "1", "2", "3", "4", "5"])
            # -1 - Unknown
            # 0 - Work
            # 1 - School
            # 2 - Shop
            # 3 - Cargo
            # 4 - Visit
            # 5 - Other
        ],
        "originMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "originTAZ": [  # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "destinationTAZ": [  # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "inbound": [
            SetValidator(["false", "true"])
        ],
        "originIsTourDestination": [  # remove
            SetValidator(["false", "true"])
        ],
        "destinationIsTourDestination": [  # remove
            SetValidator(["false", "true"])
        ],
        "period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "tripMode": [
            SetValidator([str(x) for x in range(1, 16)])
            # 1 - Drive Alone Free
            # 2 - Drive Alone Pay
            # 3 - Shared Ride 2 General Purpose
            # 4 - Shared Ride 2 HOV
            # 5 - Shared Ride 2 Pay
            # 6 - Shared Ride 3 General Purpose
            # 7 - Shared Ride 3 HOV
            # 8 - Shared Ride 3 Pay
            # 9 - Walk
            # 10 - Bike
            # 11 - Walk to Local
            # 12 - Walk to Express
            # 13 - Walk to BRT
            # 14 - Walk to Light Rail
            # 15 - Walk to Commuter Rail
        ],
        "boardingTap": [
            IntValidator()
        ],
        "alightingTap": [
            IntValidator()
        ]
    }


# create vladiator class for internalExternalTrips.csv
class InternalExternalTripsValidator(Vlad):
    """ Vladiate validator class for the internal external trips output
        comma-delimited file specifying the file schema.

    InternalExternalTripsValidator(
        source=LocalFile("../test_files/output/internalExternalTrips.csv")
        ).validate()
    """
    validators = {
        # note there is no unique identifier in this file, no tripID
        "hhID": [
            IntValidator()
        ],
        "pnum": [  # remove either pnum or personID
            IntValidator()
        ],
        "personID": [  # remove either pnum or personID
            IntValidator()
        ],
        "tourID": [  # what does this map to?
            IntValidator()
        ],
        "originMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "originTAZ": [  # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "destinationTAZ": [  # remove
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "inbound": [
            SetValidator(["false", "true"])
        ],
        "originIsTourDestination": [  # remove
            SetValidator(["false", "true"])
        ],
        "destinationIsTourDestination": [  # remove
            SetValidator(["false", "true"])
        ],
        "period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "tripMode": [
            SetValidator([str(x) for x in range(1, 16)])
            # 1 - Drive Alone Free
            # 2 - Drive Alone Pay
            # 3 - Shared Ride 2 General Purpose
            # 4 - Shared Ride 2 HOV
            # 5 - Shared Ride 2 Pay
            # 6 - Shared Ride 3 General Purpose
            # 7 - Shared Ride 3 HOV
            # 8 - Shared Ride 3 Pay
            # 9 - Walk
            # 10 - Bike
            # 11 - Walk to Local
            # 12 - Walk to Express
            # 13 - Walk to BRT
            # 14 - Walk to Light Rail
            # 15 - Walk to Commuter Rail
        ],
        "boardingTap": [
            IntValidator()
        ],
        "alightingTap": [
            IntValidator()
        ]
    }


# create vladiator class for visitorTours.csv
class VisitorToursValidator(Vlad):
    """ Vladiate validator class for the visitor model tours output
        comma-delimited file specifying the file schema.

    VisitorToursValidator(
        source=LocalFile("../test_files/output/visitorTours.csv")
        ).validate()
    """
    validators = {
        "id": [
            IntValidator(),
            UniqueValidator()
            # ordered surrogate key
        ],
        "segment": [
            SetValidator(["0", "1"])
            # 0 - Business
            # 1 - Personal
        ],
        "purpose": [
            SetValidator(["0", "1", "2"])
            # 0 - Work
            # 1 - Recreation
            # 2 - Dining
        ],
        "autoAvailable": [
            SetValidator(["0", "1"])
            # 0 - No
            # 1 - Yes
        ],
        "partySize": [
            SetValidator([str(x) for x in range(1, 11)])
            # party size 1-10+
        ],
        "income": [
            SetValidator(["0", "1", "2", "3", "4"])
            # 0 - Less than 30k
            # 1 - 30k-60k
            # 2 - 60k-100k
            # 3 - 100k-150k
            # 4 - 150k
        ],
        "departTime": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "arriveTime": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "originMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "tourMode": [
            SetValidator([str(x) for x in range(1, 28)])
            # 1 - Drive Alone Free
            # 2 - Drive Alone Pay
            # 3 - Shared Ride 2 General Purpose
            # 4 - Shared Ride 2 HOV
            # 5 - Shared Ride 2 Pay
            # 6 - Shared Ride 3 General Purpose
            # 7 - Shared Ride 3 HOV
            # 8 - Shared Ride 3 Pay
            # 9 - Walk
            # 10 - Bike
            # 11 - Walk to Local
            # 12 - Walk to Express
            # 13 - Walk to BRT
            # 14 - Walk to Light Rail
            # 15 - Walk to Commuter Rail
            # 16 - Park Ride Local
            # 17 - Park Ride Express
            # 18 - Park Ride BRT
            # 19 - Park Ride Light Rail
            # 20 - Park Ride Commuter Rail
            # 21 - Kiss Ride Local
            # 22 - Kiss Ride Express
            # 23 - Kiss Ride BRT
            # 24 - Kiss Ride Light Rail
            # 25 - Kiss Ride Commuter Rail
            # 26 - School Bus
            # 27 - Taxi
        ],
        "outboundStops": [  # remove
            IntValidator()
        ],
        "inboundStops": [  # remove
            IntValidator()
        ]
    }


# create vladiator class for visitorTrips.csv
class VisitorTripsValidator(Vlad):
    """Vladiate validator class for the visitor model trips output
        comma-delimited file specifying the file schema.

    VisitorTripsValidator(
        source=LocalFile("test_files/visitorTrips.csv")
        ).validate()
    """
    validators = {
        "tourID": [  # note the file is sorted by tourID, tripID
            IntValidator(),
            UniqueValidator(unique_with=["tripID"])
        ],
        "tripID": [
            IntValidator()
        ],
        "originPurp": [
            SetValidator(["-1", "0", "1", "2"])
            # -1 - Unknown
            # 0 - Work
            # 1 - Recreation
            # 2 - Dining
        ],
        "destPurp": [
            SetValidator(["-1", "0", "1", "2"])
            # -1 - Unknown
            # 0 - Work
            # 1 - Recreation
            # 2 - Dining
        ],
        "originMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "destinationMGRA": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "inbound": [
            SetValidator(["false", "true"])
        ],
        "originIsTourDestination": [
            SetValidator(["false", "true"])
        ],
        "destinationIsTourDestination": [
            SetValidator(["false", "true"])
        ],
        "period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "tripMode": [
            SetValidator([str(x) for x in range(1, 28)])
            # 1 - Drive Alone Free
            # 2 - Drive Alone Pay
            # 3 - Shared Ride 2 General Purpose
            # 4 - Shared Ride 2 HOV
            # 5 - Shared Ride 2 Pay
            # 6 - Shared Ride 3 General Purpose
            # 7 - Shared Ride 3 HOV
            # 8 - Shared Ride 3 Pay
            # 9 - Walk
            # 10 - Bike
            # 11 - Walk to Local
            # 12 - Walk to Express
            # 13 - Walk to BRT
            # 14 - Walk to Light Rail
            # 15 - Walk to Commuter Rail
            # 16 - Park Ride Local
            # 17 - Park Ride Express
            # 18 - Park Ride BRT
            # 19 - Park Ride Light Rail
            # 20 - Park Ride Commuter Rail
            # 21 - Kiss Ride Local
            # 22 - Kiss Ride Express
            # 23 - Kiss Ride BRT
            # 24 - Kiss Ride Light Rail
            # 25 - Kiss Ride Commuter Rail
            # 26 - School Bus
            # 27 - Taxi
        ],
        "boardingTap": [
            IntValidator()
        ],
        "alightingTap": [
            IntValidator()
        ]
    }


# create validator class for hwy_tcad.csv
class HwyTcadValidator(Vlad):
    """Vladiate validator class for the transcad highway network output
        comma-delimited file specifying the file schema.

    HwyTcadValidator(source=LocalFile("test_files/hwy_tcad.csv")).validate()
    """
    validators = {
        "ID": [  # duplicate of hwycov-id:1?
            IntValidator(),
            UniqueValidator()
        ],
        "Length": [
            FloatValidator()
        ],
        "Dir": [
            SetValidator(["0", "1"])
        ],
        "hwycov-id:1": [  # duplicate of ID?
            IntValidator(),
            UniqueValidator()
        ],
        "ID:1": [  # ??
            IntValidator()
        ],
        "Length:1": [
            FloatValidator()
        ],
        "QID": [
            SetValidator(["0"])
        ],
        "CCSTYLE": [
            SetValidator([str(x) for x in range(1, 11)])
        ],
        "UVOL": [
            SetValidator(["0"])
        ],
        "AVOL": [
            SetValidator(["0"])
        ],
        "TMP1": [
            SetValidator(["0", "1"])
        ],
        "TMP2": [
            SetValidator(["0"])
        ],
        "PLOT": [
            SetValidator(["0", "1"])
        ],
        "SPHERE": [ # understand better and make set validator?
            IntValidator(),
            RangeValidator(0, 1999)
        ],
        "RTNO": [
            IntValidator()
        ],
        "LKNO": [
            IntValidator()
        ],
        "NM": [  # has empty records
            Ignore()
        ],
        "FXNM": [  # has empty records
            Ignore()
        ],
        "TXNM": [  # has empty records
            Ignore()
        ],
        "AN": [
            IntValidator()
        ],
        "BN": [
            IntValidator()
        ],
        "COJUR": [  # understand better and make set validator?
            IntValidator(),
            RangeValidator(0, 20)
        ],
        "COSTAT": [
            IntValidator()
        ],
        "COLOC": [
            SetValidator(["0", "1"])
        ],
        "RLOOP": [
            IntValidator()
        ],
        "ADTLK": [
            IntValidator()
        ],
        "ADTVL": [
            IntValidator()
        ],
        "PKPCT": [
            IntValidator()
        ],
        "TRPCT": [
            IntValidator()
        ],
        "SECNO": [
            IntValidator()
        ],
        "DIR:1": [
            SetValidator(["1", "2", "3", "4"])
        ],
        "FFC": [
            SetValidator(["0", "1", "2", "3", "4", "5", "6", "9", "99"])
        ],
        "CLASS": [
            IntValidator()
        ],
        "ASPD": [
            IntValidator()
        ],
        "IYR": [
            SetValidator([str(x) for x in range(1990, 2101)])
        ],
        "IPROJ": [
            IntValidator()
        ],
        "IJUR": [
            SetValidator(["1", "2", "3", "4", "5", "6"])
        ],
        "IFC": [
            SetValidator([str(x) for x in range(1, 11)])
        ],
        "IHOV": [
            SetValidator(["1", "2", "4"])
        ],
        "ITRUCK": [
            SetValidator(["1", "3", "4", "7"])
        ],
        "ISPD": [
            IntValidator()
        ],
        "ITSPD": [
            IntValidator()
        ],
        "IWAY": [
            SetValidator(["1", "2"])
        ],
        "IMED": [
            SetValidator(["1", "2", "3"])
        ],
        "COST": [
            FloatValidator()
        ],
        "ITOLLO": [
            IntValidator()
        ],
        "ITOLLA": [
            IntValidator()
        ],
        "ITOLLP": [
            IntValidator()
        ],
        "ABLNO": [
            SetValidator([str(x) for x in range(1, 10)])
        ],
        "ABLNA": [
            SetValidator([str(x) for x in range(1, 10)])
        ],
        "ABLNP": [
            SetValidator([str(x) for x in range(1, 10)])
        ],
        "ABAU": [
            SetValidator(["0", "1", "2"])
        ],
        "ABPCT": [
            IntValidator(),
            RangeValidator(0, 100)
        ],
        "ABPHF": [
            IntValidator()
        ],
        "ABCNT": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "ABTL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "ABRL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "ABLL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "ABTLB": [
            IntValidator()
        ],
        "ABRLB": [
            IntValidator()
        ],
        "ABLLB": [
            IntValidator()
        ],
        "ABGC": [
            IntValidator()
        ],
        "ABPLC": [
            IntValidator()
        ],
        "ABCPO": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCPA": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCPP": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCXO": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCXA": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCXP": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCHO": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABCHA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABCHP": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABTMO": [
            FloatValidator()
        ],
        "ABTMA": [
            FloatValidator()
        ],
        "ABTMP": [
            FloatValidator()
        ],
        "ABTXO": [
            RangeValidator(0, 1)
        ],
        "ABTXA": [
            RangeValidator(0, 1)
        ],
        "ABTXP": [
            RangeValidator(0, 1)
        ],
        "ABCST": [
            FloatValidator()
        ],
        "ABVLA": [
            SetValidator(["0"])
        ],
        "ABVLP": [
            SetValidator(["0"])
        ],
        "ABLOS": [
            SetValidator(["0"])
        ],
        "BALNO": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BALNA": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BALNP": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BAAU": [
            SetValidator(["0", "1", "2"])
        ],
        "BAPCT": [
            IntValidator(),
            RangeValidator(0, 100)
        ],
        "BAPHF": [
            IntValidator()
        ],
        "BACNT": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BATL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BARL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BALL": [
            SetValidator([str(x) for x in range(0, 10)])
        ],
        "BATLB": [
            IntValidator()
        ],
        "BARLB": [
            IntValidator()
        ],
        "BALLB": [
            IntValidator()
        ],
        "BAGC": [
            IntValidator()
        ],
        "BAPLC": [
            IntValidator()
        ],
        "BACPO": [  # 999999 missing?
            FloatValidator()
        ],
        "BACPA": [  # 999999 missing?
            FloatValidator()
        ],
        "BACPP": [  # 999999 missing?
            FloatValidator()
        ],
        "BACXO": [  # 999999 missing?
            FloatValidator()
        ],
        "BACXA": [  # 999999 missing?
            FloatValidator()
        ],
        "BACXP": [  # 999999 missing?
            FloatValidator()
        ],
        "BACHO": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BACHA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BACHP": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BATMO": [
            FloatValidator()
        ],
        "BATMA": [
            FloatValidator()
        ],
        "BATMP": [
            FloatValidator()
        ],
        "BATXO": [
            RangeValidator(0, 1)
        ],
        "BATXA": [
            RangeValidator(0, 1)
        ],
        "BATXP": [
            RangeValidator(0, 1)
        ],
        "BACST": [
            FloatValidator()
        ],
        "BAVLA": [
            SetValidator(["0"])
        ],
        "BAVLP": [
            SetValidator(["0"])
        ],
        "BALOS": [
            SetValidator(["0"])
        ],
        "relifac": [
            RangeValidator(0, 1)
        ],
        "ITOLL2_EA": [
            IntValidator()
        ],
        "ITOLL2_AM": [
            IntValidator()
        ],
        "ITOLL2_MD": [
            IntValidator()
        ],
        "ITOLL2_PM": [
            IntValidator()
        ],
        "ITOLL2_EV": [
            IntValidator()
        ],
        "ITOLL3_EA": [
            FloatValidator()
        ],
        "ITOLL3_AM": [
            FloatValidator()
        ],
        "ITOLL3_MD": [
            FloatValidator()
        ],
        "ITOLL3_PM": [
            FloatValidator()
        ],
        "ITOLL3_EV": [
            FloatValidator()
        ],
        "ITOLL4_EA": [
            FloatValidator()
        ],
        "ITOLL4_AM": [
            FloatValidator()
        ],
        "ITOLL4_MD": [
            FloatValidator()
        ],
        "ITOLL4_PM": [
            FloatValidator()
        ],
        "ITOLL4_EV": [
            FloatValidator()
        ],
        "ITOLL5_EA": [
            FloatValidator()
        ],
        "ITOLL5_AM": [
            FloatValidator()
        ],
        "ITOLL5_MD": [
            FloatValidator()
        ],
        "ITOLL5_PM": [
            FloatValidator()
        ],
        "ITOLL5_EV": [
            FloatValidator()
        ],
        "ITOLL_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ITOLL_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ITOLL_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ITOLL_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ITOLL_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABCP_EA": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCP_AM": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCP_MD": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCP_PM": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCP_EV": [  # 999999 missing?
            FloatValidator()
        ],
        "BACP_EA": [  # 999999 missing?
            FloatValidator()
        ],
        "BACP_AM": [  # 999999 missing?
            FloatValidator()
        ],
        "BACP_MD": [  # 999999 missing?
            FloatValidator()
        ],
        "BACP_PM": [  # 999999 missing?
            FloatValidator()
        ],
        "BACP_EV": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCX_EA": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCX_AM": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCX_MD": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCX_PM": [  # 999999 missing?
            FloatValidator()
        ],
        "ABCX_EV": [  # 999999 missing?
            FloatValidator()
        ],
        "BACX_EA": [  # 999999 missing?
            FloatValidator()
        ],
        "BACX_AM": [  # 999999 missing?
            FloatValidator()
        ],
        "BACX_MD": [  # 999999 missing?
            FloatValidator()
        ],
        "BACX_PM": [  # 999999 missing?
            FloatValidator()
        ],
        "BACX_EV": [  # 999999 missing?
            FloatValidator()
        ],
        "ABTM_EA": [  # 999 missing?
            FloatValidator()
        ],
        "ABTM_AM": [  # 999 missing?
            FloatValidator()
        ],
        "ABTM_MD": [  # 999 missing?
            FloatValidator()
        ],
        "ABTM_PM": [  # 999 missing?
            FloatValidator()
        ],
        "ABTM_EV": [  # 999 missing?
            FloatValidator()
        ],
        "BATM_EA": [  # 999 missing?
            FloatValidator()
        ],
        "BATM_AM": [  # 999 missing?
            FloatValidator()
        ],
        "BATM_MD": [  # 999 missing?
            FloatValidator()
        ],
        "BATM_PM": [  # 999 missing?
            FloatValidator()
        ],
        "BATM_EV": [  # 999 missing?
            FloatValidator()
        ],
        "ABTX_EA": [
            RangeValidator(0, 1)
        ],
        "ABTX_AM": [
            RangeValidator(0, 1)
        ],
        "ABTX_MD": [
            RangeValidator(0, 1)
        ],
        "ABTX_PM": [
            RangeValidator(0, 1)
        ],
        "ABTX_EV": [
            RangeValidator(0, 1)
        ],
        "BATX_EA": [
            RangeValidator(0, 1)
        ],
        "BATX_AM": [
            RangeValidator(0, 1)
        ],
        "BATX_MD": [
            RangeValidator(0, 1)
        ],
        "BATX_PM": [
            RangeValidator(0, 1)
        ],
        "BATX_EV": [
            RangeValidator(0, 1)
        ],
        "ABLN_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABLN_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABLN_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABLN_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABLN_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BALN_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BALN_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BALN_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BALN_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BALN_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ABSCST_EA": [
            FloatValidator()
        ],
        "ABSCST_AM": [
            FloatValidator()
        ],
        "ABSCST_MD": [
            FloatValidator()
        ],
        "ABSCST_PM": [
            FloatValidator()
        ],
        "ABSCST_EV": [
            FloatValidator()
        ],
        "BASCST_EA": [
            FloatValidator(empty_ok=True)
        ],
        "BASCST_AM": [
            FloatValidator(empty_ok=True)
        ],
        "BASCST_MD": [
            FloatValidator(empty_ok=True)
        ],
        "BASCST_PM": [
            FloatValidator(empty_ok=True)
        ],
        "BASCST_EV": [
            FloatValidator(empty_ok=True)
        ],
        "ABH2CST_EA": [
            FloatValidator()
        ],
        "ABH2CST_AM": [
            FloatValidator()
        ],
        "ABH2CST_MD": [
            FloatValidator()
        ],
        "ABH2CST_PM": [
            FloatValidator()
        ],
        "ABH2CST_EV": [
            FloatValidator()
        ],
        "BAH2CST_EA": [
            FloatValidator(empty_ok=True)
        ],
        "BAH2CST_AM": [
            FloatValidator(empty_ok=True)
        ],
        "BAH2CST_MD": [
            FloatValidator(empty_ok=True)
        ],
        "BAH2CST_PM": [
            FloatValidator(empty_ok=True)
        ],
        "BAH2CST_EV": [
            FloatValidator(empty_ok=True)
        ],
        "ABH3CST_EA": [
            FloatValidator()
        ],
        "ABH3CST_AM": [
            FloatValidator()
        ],
        "ABH3CST_MD": [
            FloatValidator()
        ],
        "ABH3CST_PM": [
            FloatValidator()
        ],
        "ABH3CST_EV": [
            FloatValidator()
        ],
        "BAH3CST_EA": [
            FloatValidator(empty_ok=True)
        ],
        "BAH3CST_AM": [
            FloatValidator(empty_ok=True)
        ],
        "BAH3CST_MD": [
            FloatValidator(empty_ok=True)
        ],
        "BAH3CST_PM": [
            FloatValidator(empty_ok=True)
        ],
        "BAH3CST_EV": [
            FloatValidator(empty_ok=True)
        ],
        "ABSTM_EA": [
            FloatValidator()
        ],
        "ABSTM_AM": [
            FloatValidator()
        ],
        "ABSTM_MD": [
            FloatValidator()
        ],
        "ABSTM_PM": [
            FloatValidator()
        ],
        "ABSTM_EV": [
            FloatValidator()
        ],
        "BASTM_EA": [
            FloatValidator(empty_ok=True)
        ],
        "BASTM_AM": [
            FloatValidator(empty_ok=True)
        ],
        "BASTM_MD": [
            FloatValidator(empty_ok=True)
        ],
        "BASTM_PM": [
            FloatValidator(empty_ok=True)
        ],
        "BASTM_EV": [
            FloatValidator(empty_ok=True)
        ],
        "ABHTM_EA": [
            FloatValidator()
        ],
        "ABHTM_AM": [
            FloatValidator()
        ],
        "ABHTM_MD": [
            FloatValidator()
        ],
        "ABHTM_PM": [
            FloatValidator()
        ],
        "ABHTM_EV": [
            FloatValidator()
        ],
        "BAHTM_EA": [
            FloatValidator(empty_ok=True)
        ],
        "BAHTM_AM": [
            FloatValidator(empty_ok=True)
        ],
        "BAHTM_MD": [
            FloatValidator(empty_ok=True)
        ],
        "BAHTM_PM": [
            FloatValidator(empty_ok=True)
        ],
        "BAHTM_EV": [
            FloatValidator(empty_ok=True)
        ],
        "ABPRELOAD_EA": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "BAPRELOAD_EA": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "ABPRELOAD_AM": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "BAPRELOAD_AM": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "ABPRELOAD_MD": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "BAPRELOAD_MD": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "ABPRELOAD_PM": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "BAPRELOAD_PM": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "ABPRELOAD_EV": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "BAPRELOAD_EV": [  # why any decimals? only .25, .5, .75
            FloatValidator()
        ],
        "AB_GCRatio": [
            RangeValidator(0, 1, empty_ok=True)
        ],
        "BA_GCRatio": [
            RangeValidator(0, 1, empty_ok=True)
        ],
        "AB_Cycle": [
            FloatValidator(empty_ok=True)
        ],
        "BA_Cycle": [
            FloatValidator(empty_ok=True)
        ],
        "AB_PF": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator(empty_ok=True)
        ],
        "BA_PF": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator(empty_ok=True)
        ],
        "ALPHA1": [
            FloatValidator()
        ],
        "BETA1": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2": [
            FloatValidator()
        ],
        "BETA2": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "AB_GCRatio_EA": [
            RangeValidator(0, 1)
        ],
        "BA_GCRatio_EA": [
            RangeValidator(0, 1)
        ],
        "AB_Cycle_EA": [
            FloatValidator()
        ],
        "BA_Cycle_EA": [
            FloatValidator()
        ],
        "AB_PF_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BA_PF_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA1_EA": [
            FloatValidator()
        ],
        "BETA1_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2_EA": [
            FloatValidator()
        ],
        "BETA2_EA": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "AB_GCRatio_AM": [
            RangeValidator(0, 1)
        ],
        "BA_GCRatio_AM": [
            RangeValidator(0, 1)
        ],
        "AB_Cycle_AM": [
            FloatValidator()
        ],
        "BA_Cycle_AM": [
            FloatValidator()
        ],
        "AB_PF_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BA_PF_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA1_AM": [
            FloatValidator()
        ],
        "BETA1_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2_AM": [
            FloatValidator()
        ],
        "BETA2_AM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "AB_GCRatio_MD": [
            RangeValidator(0, 1)
        ],
        "BA_GCRatio_MD": [
            RangeValidator(0, 1)
        ],
        "AB_Cycle_MD": [
            FloatValidator()
        ],
        "BA_Cycle_MD": [
            FloatValidator()
        ],
        "AB_PF_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BA_PF_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA1_MD": [
            FloatValidator()
        ],
        "BETA1_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2_MD": [
            FloatValidator()
        ],
        "BETA2_MD": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "AB_GCRatio_PM": [
            RangeValidator(0, 1)
        ],
        "BA_GCRatio_PM": [
            RangeValidator(0, 1)
        ],
        "AB_Cycle_PM": [
            FloatValidator()
        ],
        "BA_Cycle_PM": [
            FloatValidator()
        ],
        "AB_PF_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BA_PF_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA1_PM": [
            FloatValidator()
        ],
        "BETA1_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2_PM": [
            FloatValidator()
        ],
        "BETA2_PM": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "AB_GCRatio_EV": [
            RangeValidator(0, 1)
        ],
        "BA_GCRatio_EV": [
            RangeValidator(0, 1)
        ],
        "AB_Cycle_EV": [
            FloatValidator()
        ],
        "BA_Cycle_EV": [
            FloatValidator()
        ],
        "AB_PF_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "BA_PF_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA1_EV": [
            FloatValidator()
        ],
        "BETA1_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ],
        "ALPHA2_EV": [
            FloatValidator()
        ],
        "BETA2_EV": [  # integers with all 0 decimals...why? should just be integers
            FloatValidator()
        ]
    }


# create vladiator class for highway load file schema
class HwyLoadValidator(Vlad):
    """Vladiate validator class for the highway load output
        comma-delimited files specifying the file schema.

    HwyLoadValidator(source=LocalFile("test_files/hwyload_AM.csv")).validate()
    """
    def __init__(self, *args, **kwargs):
        self.validators = {
            "ID1": [  # note the file is sorted by ID1, looks like an ordered surrogate key
                IntValidator(),
                UniqueValidator()
            ],
            "AB_Flow_PCE": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_PCE": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Time": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Time": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_VOC": [
                RegexValidator(pattern="([0-9]{1,2}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_VOC": [
                RegexValidator(pattern="([0-9]{1,2}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_V_Dist_T": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_V_Dist_T": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_VHT": [
                RegexValidator(pattern="([0-9]{1,5}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_VHT": [
                RegexValidator(pattern="([0-9]{1,5}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Speed": [
                RegexValidator(pattern="([0-9]{1,3}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Speed": [
                RegexValidator(pattern="([0-9]{1,3}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_VDF": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_VDF": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_MSA_Flow": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_MSA_Flow": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_MSA_Time": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_MSA_Time": [
                RegexValidator(pattern="([0-9]{1,4}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SOV_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SOV_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SOV_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SOV_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR2_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR2_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR2_HOV": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR2_HOV": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR2_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR2_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR3_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR3_GP": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR3_HOV": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR3_HOV": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_SR3_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_SR3_PAY": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_lhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_lhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_mhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_mhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_hhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_hhdn": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_lhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_lhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_mhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_mhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow_hhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow_hhdt": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ],
            "AB_Flow": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}"),
                FloatValidator()
            ],
            "BA_Flow": [
                RegexValidator(pattern="([0-9]{1,6}){1}(\.[0-9]{1,6}){0,1}", empty_ok=True),
                FloatValidator(empty_ok=True)
            ]
        }
        super(HwyLoadValidator, self).__init__(*args, **kwargs)


# create vladiator class for ctm trips file schema
class CVMTripValidator(Vlad):
    """Vladiate validator class for the Commercial Vehicle Model trip output
    comma-delimited files specifying the file schema.

    CVMTripValidator(source=LocalFile("test_files/Trip_TH_OL.csv")).validate()
    """
    def __init__(self, *args, **kwargs):
        self.validators = {
            "Model": [
                SetValidator(["3"])
            ],
            "SerialNo": [
                UniqueValidator(unique_with=["Trip"])
            ],
            "Person": [
                SetValidator(["1"])
            ],
            "Trip": [
                # RangeValidator(1, 10)
                IntValidator()
            ],
            "Tour": [
                SetValidator(["1"])
            ],
            "HomeZone": [
                SetValidator([str(x) for x in range(13, 4998)])
            ],
            "ActorType": [
                SetValidator(["FA", "GO", "IN", "RE", "SV", "TH", "WH"])
            ],
            "OPurp": [
                SetValidator(["Est", "Gds", "Oth", "Srv"])
            ],
            "DPurp": [
                SetValidator(["Est", "Gds", "Oth", "Srv"])
            ],
            "I": [
                SetValidator([str(x) for x in range(13, 4998)])
            ],
            "J": [
                SetValidator([str(x) for x in range(13, 4998)])
            ],
            "Time": [
                SetValidator(["CVM_EA:LT", "CVM_EA:LNT", "CVM_EA:IT",
                              "CVM_EA:INT", "CVM_EA:MT", "CVM_EA:MNT",
                              "CVM_EA:HT", "CVM_EA:HNT",
                              "CVM_AM:LT", "CVM_AM:LNT", "CVM_AM:IT",
                              "CVM_AM:INT", "CVM_AM:MT", "CVM_AM:MNT",
                              "CVM_AM:HT", "CVM_AM:HNT",
                              "CVM_MD:LT", "CVM_MD:LNT", "CVM_MD:IT",
                              "CVM_MD:INT", "CVM_MD:MT", "CVM_MD:MNT",
                              "CVM_MD:HT", "CVM_MD:HNT",
                              "CVM_PM:LT", "CVM_PM:LNT", "CVM_PM:IT",
                              "CVM_PM:INT", "CVM_PM:MT", "CVM_PM:MNT",
                              "CVM_PM:HT", "CVM_PM:HNT",
                              "CVM_EV:LT", "CVM_EV:LNT", "CVM_EV:IT",
                              "CVM_EV:INT", "CVM_EV:MT", "CVM_EV:MNT",
                              "CVM_EV:HT", "CVM_EV:HNT"])
                ],
            "Mode": [
                SetValidator(["L", "I", "M", "H"])
            ],
            "StartTime": [
                FloatValidator()
            ],
            "EndTime": [
                FloatValidator()
            ],
            "StopDuration": [
                FloatValidator()
            ],
            "TourType": [
                SetValidator(["G", "O", "S"])
            ],
            "OriginalTimePeriod": [
                SetValidator(["OE", "AM", "MD", "PM", "OL"])
            ],
            "TripMode": [
                SetValidator(["T", "NT"])
            ],
            "TollAvailable": [
                SetValidator(["false", "true"])
            ]
        }
        super(CVMTripValidator, self).__init__(*args, **kwargs)


# create vladiator class for walkMgraEquivMinutes.csv
class WalkMgraEquivMinutesValidator(Vlad):
    """Vladiate validator class for the MGRA-based walk time from MGRA-MGRA
        in minutes comma-delimited file specifying the file schema.

    WalkMgraEquivMinutesValidator(source=LocalFile("test_files/walkMgraEquivMinutes.csv")).validate()
    """
    validators = {
        "i": [  # note the file is sorted by (i, j)
            SetValidator([str(x) for x in range(1, 23003)]),
            UniqueValidator(unique_with=["j"])
        ],
        "j": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "percieved": [  # note this is misspelled, why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "actual": [  # why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "gain": [
            # very few records (<.1%) have a decimal value and all are .5, just keep it in feet make integer
            FloatValidator()
        ]
    }


# create vladiator class for walkMgraTapEquivMinutes.csv
class WalkMgraTapEquivMinutesValidator(Vlad):
    """Vladiate validator class for the MGRA-based walk time from MGRA-TAP
        in minutes comma-delimited file specifying the file schema.

    WalkMgraTapEquivMinutesValidator(source=LocalFile("test_files/walkMgraTapEquivMinutes.csv")).validate()
    """
    validators = {
        "mgra": [  # note the file is sorted by (mgra, tap)
            SetValidator([str(x) for x in range(1, 23003)]),
            UniqueValidator(unique_with=["tap"])
        ],
        "tap": [
            IntValidator()
        ],
        "boardingPerceived": [  # why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "boardingActual": [  # why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "alightingPerceived": [  # why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "alightingActual": [  # why 3 digits? that's .006 seconds
            FloatValidator()
        ],
        "boardingGain": [
            IntValidator()
        ],
        "alightingGain": [
            IntValidator()
        ]
    }

