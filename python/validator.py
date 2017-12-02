import logging
import os
from itertools import chain
from vladiate import Vlad  # https://github.com/di/vladiate
from vladiate import logs
from vladiate.inputs import LocalFile
from vladiate.validators import UniqueValidator, SetValidator, FloatValidator, \
    RangeValidator, IntValidator, Ignore, RegexValidator, NotEmptyValidator

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


# create vladiator class for output/airport_out.csv
class AirportTripsValidator(Vlad):
    """ Vladiate validator class for the airport model trips output
        comma-delimited file specifying the file schema.

    AirportTripsValidator(source=LocalFile(
        "../test_files/new_files/output/airport_out.csv"
        )).validate()
    """
    validators = {
        # no changes from old file to new file
        # where is arriveTime? destination purpose?
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


# create vladiator class for output/bikeMgraLogsum.csv
class BikeMgraValidator(Vlad):
    """ Vladiate validator class for the bike mgra logsums output
        comma-delimited file specifying the file schema.

    BikeMgraValidator(source=LocalFile(
        "../test_files/new_files/output/bikeMgraLogsum.csv"
        )).validate()
    """
    validators = {
        # note the file is sorted on i, j
        # no changes from old file to new file
        # what is the assumed speed for bicycles in ABM model?
        "i": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "j": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "logsum": [
            FloatValidator()
        ],
        "time": [
            FloatValidator()
        ]
    }


# create vladiator class for report/commtrip.csv
class CommercialVehicleTripsValidator(Vlad):
    """ Vladiate validator class for the commercial vehicle model output
        comma-delimited file specifying the file schema.

    CommercialVehicleTripsValidator(source=LocalFile(
        "../test_files/new_files/report/commtrip.csv"
        )).validate()
    """
    validators = {
        # note the file is sorted on ORIG_TAZ, DEST_TAZ
        # no changes from old file to new file
        # mode is assumed can we write it out somehow?
        "ORIG_TAZ": [
            SetValidator([str(x) for x in range(13, 4997)])
        ],
        "DEST_TAZ": [
            SetValidator([str(x) for x in range(13, 4997)])
        ],
        "TOD": [
            SetValidator(["EA", "AM", "MD", "PM", "EV"])
            # ABM five time of day categories
        ],
        "TRIPS_COMMVEH": [
            FloatValidator()
        ]
    }


# create vladiator class for output/crossBorderTours.csv
class CrossBorderToursValidator(Vlad):
    """ Vladiate validator class for the cross border model tour output
        comma-delimited file specifying the file schema.

    CrossBorderToursValidator(source=LocalFile(
        "../test_files/new_files/output/crossBorderTours.csv"
        )).validate()
    """
    validators = {
        # removed originTAZ, destinationTAZ
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
        "tourMode": [
            SetValidator(["1", "2", "3", "4"])
            # 1 - Drive Alone
            # 2 - Shared Ride 2
            # 3 - Shared Ride 3+
            # 4 - Walk
        ]
    }


# create vladiator class for output/crossBorderTrips.csv
class CrossBorderTripsValidator(Vlad):
    """ Vladiate validator class for the cross border model trip output
        comma-delimited file specifying the file schema.

    CrossBorderTripsValidator(source=LocalFile(
        "../test_files/new_files/output/crossBorderTrips.csv"
        )).validate()
    """
    validators = {
        # removed originTAZ, destinationTAZ, originIsTourDestination,
        #    destinationIsTourDestination
        # where is arriveTime?
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
        "inbound": [
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


# create vladiator class for report/eetrip.csv
class ExternalExternalValidator(Vlad):
    """ Vladiate validator class for the External-External trips model output
        comma-delimited file specifying the file schema.

    ExternalExternalValidator(source=LocalFile(
        "../test_files/new_files/report/eetrip.csv"
        )).validate()
    """
    validators = {
        # note the file is sorted on ORIG_TAZ, DEST_TAZ
        # no changes from old file to new file
        # can we make TOD and mode a part of this?
        "ORIG_TAZ": [
            SetValidator([str(x) for x in range(1, 14)]),
            UniqueValidator(unique_with=["DEST_TAZ"])
        ],
        "DEST_TAZ": [
            SetValidator([str(x) for x in range(1, 14)])
        ],
        "TRIPS_EE": [
            FloatValidator()
        ]
    }


# create vladiator class for report/eitrip.csv
class ExternalInternalValidator(Vlad):
    """ Vladiate validator class for the External-Internal trips model output
        comma-delimited file specifying the file schema.

    ExternalInternalValidator(source=LocalFile(
        "../test_files/new_files/report/eitrip.csv"
        )).validate()
    """
    validators = {
        # note the file is sorted on ORIG_TAZ, DEST_TAZ
        # no changes from old file to new file
        "ORIG_TAZ": [
            SetValidator([str(x) for x in range(1, 4997)]),
            UniqueValidator(unique_with=["DEST_TAZ"])
        ],
        "DEST_TAZ": [
            SetValidator([str(x) for x in range(1, 4997)])
        ],
        "TOD": [
            SetValidator(["EA", "AM", "MD", "PM", "EV"])
            # ABM five time of day categories
        ],
        "PURPOSE": [
            SetValidator(["NONWORK", "WORK"])
        ],
        "TRIPS_DAN": [
            FloatValidator()
            # trips Drive Alone Free
        ],
        "TRIPS_S2N": [
            FloatValidator()
            # trips Shared Ride 2 General Purpose
            # check this is not HOV
        ],
        "TRIPS_S3N": [
            FloatValidator()
            # trips Shared Ride 3 General Purpose
            # check this is not HOV
        ],
        "TRIPS_DAT": [
            FloatValidator()
            # trips Drive Alone Pay
        ],
        "TRIPS_S2T": [
            FloatValidator()
            # trips Shared Ride 2 Pay
        ],
        "TRIPS_S3T": [
            FloatValidator()
            # trips Shared Ride 3 Pay
        ]
    }


# create vladiator class for output/householdData_<<iteration>>.csv
class HouseholdDataValidator(Vlad):
    """ Vladiate validator class for the household data output
        comma-delimited file specifying the file schema.

    HouseholdDataValidator(source=LocalFile(
        "../test_files/new_files/output/householdData_3.csv"
        )).validate()
    """
    validators = {
        # removed home_mgra, income, cdap_pattern, jtf_choice
        "hh_id": [
            IntValidator(),
            UniqueValidator()
            # file not sorted on hh_id
        ],
        "autos": [
            SetValidator(["0", "1", "2", "3", "4"])
            # 0 - 0 autos
            # 1 - 1 auto
            # 2 - 2 autos
            # 3 - 3 autos
            # 4 - 4+ autos
        ],
        "transponder": [
            SetValidator(["0", "1"])
            # transponder ownership
            # 0 - No
            # 1 - Yes
        ]
    }


# create vladiator class for input/households.csv
class HouseholdsValidator(Vlad):
    """ Vladiate validator class for the households data input
        comma-delimited file specifying the file schema.

    HouseholdsValidator(source=LocalFile(
        "../test_files/new_files/input/households.csv")
        ).validate()
    """
    validators = {
        # cannot remove what not interested in
        # not interested in taz, hinc, hworkers, veh
        "hhid": [
            IntValidator(),
            UniqueValidator()
            # ordered surrogate key
        ],
        "household_serial_no": [  # remove?
            NotEmptyValidator()
            # might want to use a regex validator?
        ],
        "taz": [
            SetValidator([str(x) for x in range(13, 4997)])
        ],
        "mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "hinccat1": [
            SetValidator(["1", "2", "3", "4", "5"])
            # 1 - Less than 30k
            # 2 - 30k-60k
            # 3 - 60k-100k
            # 4 - 100k-150k
            # 5 - 150k
        ],
        "hinc": [
            IntValidator()
            # continuous household income
        ],
        "hworkers": [
            IntValidator()
            # number of workers in household
        ],
        "veh": [
            IntValidator()
            # number of vehicles owned in household
            # this is NOT the same as vehicles owned in abm model
            # that is a separate field/estimation done in the model
        ],
        "persons": [
            IntValidator()
            # number of persons in household
        ],
        "hht": [
            SetValidator(["0", "1", "2", "3", "4", "5", "6", "7"])
            # 0 - not in universe (vacant or GQ)
            # 1 - family household: married couple
            # 2 - family household: male householder no wife present
            # 3 - family household: female householder no husband present
            # 4 - non-family household: male householder living alone
            # 5 - non-family household: male householder not living alone
            # 6 - non-family household: female householder living alone
            # 7 - non-family household: female householder not living alone
        ],
        "bldgsz": [
            SetValidator([str(x) for x in range(1, 11)])
            # 1 - mobile home or trailer
            # 2 - one-family house detached
            # 3 - one-family house attached
            # 4 - 2 apartments
            # 5 - 3-4 apartments
            # 6 - 5-9 apartments
            # 7 - 10-19 apartments
            # 8 - 20-49 apartments
            # 9 - 50 or more apartments
            # 10 - boat, rv, van, etc...
        ],
        "unittype": [
            SetValidator(["0", "1", "2"])
            # 0 - household
            # 1 - non-institutional group quarters
            # 2 - institutional group quarters
        ],
        "version": [
            IntValidator()
            # synthetic population version number
        ],
        "poverty": [
            FloatValidator()
            # ???
        ]
    }


# create vladiator class for output/indivTourData_<<iteration>>.csv
class IndividualToursValidator(Vlad):
    """ Vladiate validator class for the individual model tours output
            comma-delimited file specifying the file schema.

        IndividualToursValidator(source=LocalFile(
            "../test_files/new_files/output/indivTourData_3.csv"
            )).validate()
        """
    validators = {
        # note this file has no single ordered surrogate key,
        #     huge performance implications in the model
        # removed hh_id, person_num, person_type, tour_distance, atWork_freq,
        #     num_ob_stops, num_ib_stops, util_1-26, prob_1-26
        "person_id": [
            # there are a few different unique keys we can create due to
            # all the data duplication, this is the narrowest
            IntValidator(),
            UniqueValidator(unique_with=["tour_id", "tour_purpose"])
        ],
        "tour_id": [
            # should just be an ordered surrogate key
            # huge performance implications
            IntValidator()
        ],
        "tour_category": [
            SetValidator(["AT_WORK", "INDIVIDUAL_NON_MANDATORY",
                          "MANDATORY"])
        ],
        "tour_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Escort",
                          "Maintenance", "School", "Shop", "University",
                          "Visiting", "Work", "Work-Based"])
        ],
        "orig_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "dest_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "start_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "end_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "tour_mode": [
            SetValidator([str(x) for x in range(1, 27)])
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
        ]
    }


# create vladiator class for output/indivTripData_<<iteration>>.csv
class IndividualTripsValidator(Vlad):
    """ Vladiate validator class for the individual model trips output
            comma-delimited file specifying the file schema.

        IndividualTripsValidator(source=LocalFile(
            "../test_files/new_files/output/indivTripData_3.csv"
            )).validate()
        """
    validators = {
        # note this file has no single ordered surrogate key,
        #     huge performance implications in the model
        # removed hh_id, person_num, tour_purpose, tour_mode
        # why no orig and dest period?
        "person_id": [
            # there are a few different unique keys we can create due to
            # all the data duplication, this is the narrowest
            IntValidator(),
            UniqueValidator(unique_with=["tour_id", "stop_id", "inbound", "tour_purpose"])
        ],
        "tour_id": [
            IntValidator()
        ],
        "stop_id": [
            IntValidator()
        ],
        "inbound": [
            SetValidator(["0", "1"])
        ],
        "orig_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Escort", "Home",
                          "Maintenance", "School", "Shop", "University",
                          "Visiting", "Work", "Work-Based", "work related"])
        ],
        "dest_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Escort", "Home",
                          "Maintenance", "School", "Shop", "University",
                          "Visiting", "Work", "Work-Based", "work related"])
        ],
        "orig_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "dest_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "parking_mgra": [
            SetValidator([str(x) for x in range(-1, 23003)])
        ],
        "stop_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "trip_mode": [
            SetValidator([str(x) for x in range(1, 27)])
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
        ],
        "trip_board_tap": [
            IntValidator()
        ],
        "trip_alight_tap": [
            IntValidator()
        ]
    }


# create vladiator class for output/internalExternalTrips.csv
class InternalExternalTripsValidator(Vlad):
    """ Vladiate validator class for the internal external trips output
        comma-delimited file specifying the file schema.

    InternalExternalTripsValidator(source=LocalFile(
        "../test_files/new_files/output/internalExternalTrips.csv"
        )).validate()
    """
    validators = {
        # note there is no unique identifier in this file, no tripID
        # where is arriveTime? no purposes?
        # removed hhID, pnum, originTAZ, destinationTAZ,
        #     originIsTourDestination, destinationIsTourDestination,
        "personID": [
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
        "inbound": [
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


# create vladiator class for output/jointTourData_<<iteration>>.csv
class JointToursValidator(Vlad):
    """ Vladiate validator class for the joint model tours output
            comma-delimited file specifying the file schema.

        JointToursValidator(source=LocalFile(
            "../test_files/new_files/output/jointTourData_3.csv"
            )).validate()
        """
    validators = {
        # note this file has no single ordered surrogate key,
        #     huge performance implications in the model
        # removed tour_composition, tour_distance
        #     num_ob_stops, num_ib_stops, util_1-26, prob_1-26
        "hh_id": [
            IntValidator(),
            UniqueValidator(unique_with=["tour_id"])
        ],
        "tour_id": [
            # should just be an ordered surrogate key
            IntValidator()
        ],
        "tour_category": [
            SetValidator(["JOINT_NON_MANDATORY"])
        ],
        "tour_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Shop", "Visiting"])
        ],
        "tour_participants": [
            NotEmptyValidator()
            # space separated pnum of persons on the tour
            # if replaced by person_id could drop hh_id
        ],
        "orig_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "dest_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "start_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "end_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "tour_mode": [
            SetValidator([str(x) for x in range(1, 27)])
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
        ]
    }


# create vladiator class for output/jointTripData_<<iteration>>.csv
class JointTripsValidator(Vlad):
    """ Vladiate validator class for the joint model trips output
            comma-delimited file specifying the file schema.

        JointTripsValidator(source=LocalFile(
            "../test_files/new_files/output/jointTripData_3.csv"
            )).validate()
        """
    validators = {
        # note this file has no single ordered surrogate key,
        #     huge performance implications in the model
        # removed tour_purpose, num_participants, tour_mode
        # why no orig and dest period?
        "hh_id": [
            IntValidator(),
            UniqueValidator(unique_with=["tour_id", "stop_id", "inbound"])
        ],
        "tour_id": [
            IntValidator()
        ],
        "stop_id": [
            IntValidator()
        ],
        "inbound": [
            SetValidator(["0", "1"])
        ],
        "orig_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Escort", "Home",
                          "Maintenance", "Shop", "Visiting"])
        ],
        "dest_purpose": [
            SetValidator(["Discretionary", "Eating Out", "Escort", "Home",
                          "Maintenance", "Shop", "Visiting"])
        ],
        "orig_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "dest_mgra": [
            SetValidator([str(x) for x in range(1, 23003)])
        ],
        "parking_mgra": [
            SetValidator([str(x) for x in range(-1, 23003)])
        ],
        "stop_period": [
            SetValidator([str(x) for x in range(1, 41)])
            # 1 - Before 5am
            # 2-39 every half hour time slots
            # 40 - After 12am
        ],
        "trip_mode": [
            SetValidator([str(x) for x in range(1, 27)])
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
        ],
        "trip_board_tap": [
            IntValidator()
        ],
        "trip_alight_tap": [
            IntValidator()
        ]
    }


# create vladiator class for output/personData_<<iteration>>.csv
class PersonDataValidator(Vlad):
    """ Vladiate validator class for the abm person data output
            comma-delimited file specifying the file schema.

        PersonDataValidator(source=LocalFile(
            "../test_files/new_files/output/personData_3.csv"
            )).validate()
        """
    validators = {
        # removed imf_choice, inmf_choice, ie_choice
        "hh_id": [
            IntValidator()
        ],
        "person_id": [
            IntValidator(),
            UniqueValidator()
        ],
        "person_num": [
            IntValidator()
            # could remove if joint trips participants used person_id
            # why does this exist?
        ],
        "age": [
            IntValidator()
        ],
        "gender": [
            SetValidator(["f", "m"])
        ],
        "type": [
            SetValidator(["Child too young for school", "Full-time worker",
                          "Non-worker", "Part-time worker", "Retired",
                          "Student of driving age",
                          "Student of non-driving age", "University student"])
        ],
        "value_of_time": [
            Ignore()  # TBD
        ],
        "activity_pattern": [
            SetValidator(["H", "M", "N"])
        ],
        "fp_choice": [
            SetValidator([-1, 1, 2, 3])
        ],
        "reimb_pct": [
            RangeValidator(-1, 1)
        ]
    }


# create vladiator class for input/persons.csv
class PersonsValidator(Vlad):
    """ Vladiate validator class for the input person data
            comma-delimited file specifying the file schema.

        PersonDataValidator(source=LocalFile(
            "../test_files/new_files/input/persons.csv"
            )).validate()
        """
    validators = {
        # do not remove anything although not interested in everything
        # only interested in hhid, perid,household_serial_no, military, rac1p
        #     hisp, version
        "hhid": [
            IntValidator()
        ],
        "perid": [
            IntValidator(),
            UniqueValidator()
            # ordered surrogate key
        ],
        "household_serial_no": [  # remove?
            NotEmptyValidator()
            # might want to use a regex validator?
        ],
        "pnum": [
            IntValidator()
            # person number within household
            # necessary?
        ],
        "age": [
            IntValidator()
        ],
        "sex": [
            SetValidator([])
        ],
        "miltary": [
            SetValidator([])
        ],
        "pemploy": [
            SetValidator([])
        ],
        "pstudent": [
            SetValidator([])
        ],
        "ptype": [
            SetValidator([])
        ],
        "educ": [
            SetValidator([])
        ],
        "grade": [
            SetValidator([])
        ],
        "occen5": [
            SetValidator([])
        ],
        "occsoc5": [
            SetValidator([])
        ],
        "indcen": [
            SetValidator([])
        ],
        "weeks": [
            IntValidator()
        ],
        "hours": [
            IntValidator()
        ],
        "rac1p": [
            SetValidator([])
        ],
        "hisp": [
            SetValidator([])
        ],
        "version": [
            IntValidator()
            # synthetic population version number
        ]
    }


# create vladiator class for report/tapskim.csv
class TapSkimValidator(Vlad):
    """ Vladiate validator class for the tap skims output
            comma-delimited file specifying the file schema.

        TapSkimValidator(source=LocalFile(
            "../test_files/new_files/report/tapskim.csv"
            )).validate()
        """
    validators = {
        # note the file is sorted on ORIG_TAP, DEST_TAP
        # requires additional modes and number of transfers
        "ORIG_TAP": [
            IntValidator(),
            UniqueValidator(unique_with=["DEST_TAP"])
        ],
        "DEST_TAP": [
            IntValidator()
        ],
        "TOD": [
            SetValidator(["EA", "AM", "MD", "PM", "EV"])
            # ABM five time of day categories
        ],
        "TIME_INIT_WAIT_PREMIUM_TRANSIT": [
            FloatValidator()
            # initial wait time
            # units?
            # need to decide on significant digits
            # what is premimum transit?
        ],
        "TIME_IVT_TIME_PREMIUM_TRANSIT": [
            FloatValidator()
            # in vehicle time
            # units?
            # need to decide on significant digits
            # what is premimum transit?
        ],
        "TIME_WALK_TIME_PREMIUM_TRANSIT": [
            FloatValidator()
            # what is this?
            # units?
            # need to decide on significant digits
            # what is premimum transit?
        ],
        "TIME_TRANSFER_TIME_PREMIUM_TRANSIT": [
            FloatValidator()
            # transfer time
            # units?
            # need to decide on significant digits
            # what is premimum transit?
        ],
        "FARE_PREMIUM_TRANSIT": [
            FloatValidator()
            # cost in dollars ($XX.XX)
            # what is premimum transit?
        ]
    }


# create vladiator class for output/visitorTours.csv
class VisitorToursValidator(Vlad):
    """ Vladiate validator class for the visitor model tours output
        comma-delimited file specifying the file schema.

    VisitorToursValidator(source=LocalFile(
        "../test_files/new_files/output/visitorTours.csv"
        )).validate()
    """
    validators = {
        # removed outboundStops, inboundStops
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
        ]
    }


# create vladiator class for output/visitorTrips.csv
class VisitorTripsValidator(Vlad):
    """Vladiate validator class for the visitor model trips output
        comma-delimited file specifying the file schema.

    VisitorTripsValidator(source=LocalFile(
        "../test_files/new_files/output/visitorTrips.csv"
        )).validate()
    """
    validators = {
        # removed originIsTourDestination, destinationIsTourDestination
        # where is arriveTime?
        # note the column headers are misspelled in the file, destinationMGRAu and inbond
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


# create vladiator class for output/walkMgraEquivMinutes.csv
class WalkMgraEquivMinutesValidator(Vlad):
    """Vladiate validator class for the MGRA-based walk time from MGRA-MGRA
        in minutes comma-delimited file specifying the file schema.

    WalkMgraEquivMinutesValidator(source=LocalFile(
        "../test_files/new_files/output/walkMgraEquivMinutes.csv"
        )).validate()
    """
    validators = {
        # note perceived is spelled wrong in the header, percieved
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


# create vladiator class for output/walkMgraTapEquivMinutes.csv
class WalkMgraTapEquivMinutesValidator(Vlad):
    """Vladiate validator class for the MGRA-based walk time from MGRA-TAP
        in minutes comma-delimited file specifying the file schema.

    WalkMgraTapEquivMinutesValidator(source=LocalFile(
        "../test_files/new_files/walkMgraTapEquivMinutes.csv"
        )).validate()
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


# create vladiator class for output/wsLocResults_<<iteration>>.csv
class WorkSchoolLocationValidator(Vlad):
    """Vladiate validator class for the work-school location choice model
        output comma-delimited file specifying the file schema.

    WorkSchoolLocationValidator(source=LocalFile(
        "../test_files/new_files/output/wsLocResults_3.csv"
        )).validate()
    """
    validators = {
        # removed HHID, HomeMGRA, Income, PersonNum, PersonType, PersonAge
        #    WorkLocationDistance, WorkLocationLogsum, SchoolLocationDistance
        #    SchoolLocationLogsum
        "PersonID": [
            IntValidator(),
            UniqueValidator()
        ],
        "EmploymentCategory": [
            SetValidator(["1", "2", "3", "4"])
            # 1 - Working Full Time worker
            # 2 - Working Part Time workers, university student workers
            #     and driving age student workers
            # 3 - Non-working university students, non-workers
            #     and driving age student workers
            # 4 - Non-working pre-driving and preschool students
        ],
        "StudentCategory": [
            SetValidator(["1", "2", "3"])
            # 1 - Preschool and K-12
            # 2 - University/College
            # 3 - Workers/Non-workers/Preschool
        ],
        "WorkSegment": [
            SetValidator([str(x) for x in chain(range(-1, 6), range(99998, 99999))])
            # work district, definition?
            # 99999 - non-workers
        ],
        "SchoolSegment": [
            SetValidator([str(x) for x in chain(range(-1, 57), range(88887, 88888))])
            # school district, definition?
            # 88888 - non-school students
        ],
        "WorkLocation": [
            SetValidator([str(x) for x in range(0, 23003)])
            # includes 0 as missing
        ],
        "SchoolLocation": [
            SetValidator([str(x) for x in range(0, 23003)])
            # includes 0 as missing
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
        "SPHERE": [  # understand better and make set validator?
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
