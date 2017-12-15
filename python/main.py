from collections import namedtuple
from csvsplitter import split
import glob
import os
import validator

iteration = "3"
scenario_path = "../test_files/new_files/"

# create list of namedtuples containing
# the name of the file, the folder it is in within the scenario
# and the name of its Vladiate Vlad validator class
FileInfo = namedtuple("FileInfo", ["name", "folder", "validator_name"])

files = [FileInfo(name="airport_out", folder="output/", validator_name="AirportTripsValidator"),
         FileInfo(name="bikeMgraLogsum", folder="output/", validator_name="BikeMgraValidator"),
         FileInfo(name="commtrip", folder="report/", validator_name="CommercialVehicleTripsValidator"),
         FileInfo(name="crossBorderTours", folder="output/", validator_name="CrossBorderToursValidator"),
         FileInfo(name="crossBorderTrips", folder="output/", validator_name="CrossBorderTripsValidator"),
         FileInfo(name="eetrip", folder="report/", validator_name="ExternalExternalValidator"),
         FileInfo(name="eitrip", folder="report/", validator_name="ExternalInternalValidator"),
         FileInfo(name="householdData_" + iteration, folder="output/", validator_name="HouseholdDataValidator"),
         FileInfo(name="households", folder="input/", validator_name="HouseholdsValidator"),
         FileInfo(name="indivTourData_" + iteration, folder="output/", validator_name="IndividualToursValidator"),
         FileInfo(name="indivTripData_" + iteration, folder="output/", validator_name="IndividualTripsValidator"),
         FileInfo(name="internalExternalTrips", folder="output/", validator_name="InternalExternalTripsValidator"),
         FileInfo(name="jointTourData_" + iteration, folder="output/", validator_name="JointToursValidator"),
         FileInfo(name="jointTripData_" + iteration, folder="output/", validator_name="JointTripsValidator"),
         FileInfo(name="personData_" + iteration, folder="output/", validator_name="PersonDataValidator"),
         FileInfo(name="persons", folder="input/", validator_name="PersonsValidator"),
         FileInfo(name="tapskim", folder="report/", validator_name="TapSkimValidator"),
         FileInfo(name="tazskim", folder="report/", validator_name="TazSkimValidator"),
         FileInfo(name="visitorTours", folder="output/", validator_name="VisitorToursValidator"),
         FileInfo(name="visitorTrips", folder="output/", validator_name="VisitorTripsValidator"),
         FileInfo(name="walkMgraEquivMinutes", folder="output/", validator_name="WalkMgraEquivMinutesValidator"),
         FileInfo(name="walkMgraTapEquivMinutes", folder="output/", validator_name="WalkMgraTapEquivMinutesValidator"),
         FileInfo(name="wsLocResults_" + iteration, folder="output/", validator_name="WorkSchoolLocationValidator")]

# loop through list of namedtuples
for file_info in files:
    # get path to csv file
    file_path = scenario_path + file_info.folder + file_info.name + ".csv"

    # split file into multiple files if its size warrants
    split(filehandler=open(file_path, "r"), output_name_template=file_info.name + "_split_%s.csv",
          output_path=scenario_path + file_info.folder)

    # for all the created split files
    # eventually change this to a multi-threaded process
    for split_file in glob.glob(pathname=scenario_path + file_info.folder + file_info.name + "_split_*.csv"):
        # validate the file using the appropriate Vladiator Vlad class
        # need to add statement to fail if validator class does not pass
        # need to alter Vlad class to fail on first error but log that first error
        if file_info.name in ["commtrip", "tapskim", "tazskim"]:
            pass
        else:
            getattr(validator, file_info.validator_name)(source=validator.LocalFile(split_file)).validate()

        # bulk insert the file to the database

        # remove the created split file
        os.remove(split_file)

# execute sql transformations and final insert
