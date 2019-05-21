"""
This will create a pivot table showing demographics of participants served
"""

import numpy as np
import pandas as pd
import sys

class PtDemoPivot:
    def __init__(self, df):
        """
        Initialize the class making a local copy of the dataframe, then calling
        the process method which will return the result.

        :param df: A pandas dataframe containing demographics data and a
        staff member's name.  At this time the only report that should use this
        class will be using the All Services report as its base.  Should other
        reports be used this class will need to be modified to both identify the
        dataframe's base report and treat the data accordingly.
        """
        self.df = df
        self.pivot = None
        self.race_dict = {
           "Black or African American (HUD)": "Black or African American",
            "American Indian or Alaska Native (HUD)": "American Indian or Alaska Native",
            "American Indian or Alaska Native (HUD) - DOES NOT MAP": "American Indian or Alaska Native",
            "White (HUD)": "White",
            "Client refused (HUD)": "No Race Information Entered",
            "Native Hawaiian or Other Pacific Islander (HUD)": "Native Hawaiian or Other Pacific Islander",
            "Client doesn't know (HUD)": "No Race Information Entered",
            "Other Multi-Racial": "No Race Information Entered",
            "Asian (HUD)": "Asian",
            "Other (NON-HUD)": "No Race Information Entered",
            "Data not collected (HUD)": "No Race Information Entered",
            "Black or African American (HUD) - DOES NOT MAP": "Black or African American",
            "blank": "No Race Information Entered",
            "american indian or alaska native (hud)-does not map": "American Indian or Alaska Native"
        }
        self.eth_dict = {
            "Non-Hispanic/Non-Latino (HUD)": "Non-Hispanic/Non-Latino",
            "Client refused (HUD)": "No Ethnicity Information Entered",
            "Client doesn't know (HUD)": "No Ethnicity Information Entered",
            "Hispanic/Latino (HUD)": "Hispanic/Latino",
            "Data not collected (HUD)": "No Ethnicity Information Entered",
            "blank": "No Ethnicity Information Entered"
        }

    def __check_df_type(self):
        """
        This checks attempts to identify the base report given to the df param
        """

        try:
            if "Service User Creating" in self.df.columns.tolist():
                __services_pivot()
            elif "Entry Exit User Creating" in self.df.columns.tolist():
                pass
            elif "Placement Case Manager(3075)" in self.df.columns.tolist():
                pass
            else:
                raise Exception(
                    "MissingStaffMember: No staff member column present"
                )
        except:
            raise Exception("UnexpectedError: {}".format(sys.exc_info()))

    def __services_pivot(self, services_df):
        """
        Create a pivot table showing demographics of pts served by staff member.

        This method is specifically for instances where the dataframe provided
        to the df param is from an All Services style base report.  df derived
        from other base reports will be processed using other methods.

        :param services_df: this is a pandas dataframe that is derived from an
        all services style ART report or similar collection of services data.
        """
        local_df = self.df.copy()

        # make
        local_df["Race"] = [self.race_dict[race] for race in local_df["Race(895)"]]
        local_df["Secondary Race"] = [self.race_dict[race] for race in local_df["Race-Additional(1213)"]]
        local_df["Ethnicity"] = [self.eth_dict[eth] for eth in local_df["Ethnicity (Hispanic/Latino)(896)"]]

        # create pivot tables for the race, gender, and ethnicity columns
        primary_pivot = pd.pivot_table(
            local_df,
            index="Service User Creating",
            columns="Race",
            values="Client Uid",
            aggfunc=len
        )
        secondary_pivot = pd.pivot_table(
            local_df,
            index="Service User Creating",
            columns="Secondary Race",
            values="Client Uid",
            aggfunc=len
        )
        tertiary_pivot = pd.pivot_table(
            local_df,
            index="Service User Creating",
            columns="Ethnicity",
            values="Client Uid",
            aggfunc=len
        )
        gender_pivot = pd.pivot_table(
            local_df,
            index="Service User Creating",
            columns="Gender",
            values="Client Uid",
            aggfunc=len
        )

        # set the value of the self.pivot variable to be the sum of the various
        # demographics pivot tables
        self.pivot = primary_pivot.add(
            secondary_pivot.add(
                tertiary_pivot.add(
                    gender_pivot,
                    fill_value=0
                ),
                fill_value=0
            ),
            fill_value=0
        )

    def __entries_pivot(self, services_df):
        """
        Create a pivot table showing demographics of pts entered by staff member.

        This method is specifically for instances where the dataframe provided
        to the df param is from an All Services style base report.  df derived
        from other base reports will be processed using other methods.

        :param services_df: this is a pandas dataframe that is derived from an
        all services style ART report or similar collection of services data.
        """
        local_df = self.df.copy()

        # make
        local_df["Race"] = [self.race_dict[race] for race in local_df["Race(895)"]]
        local_df["Secondary Race"] = [self.race_dict[race] for race in local_df["Race-Additional(1213)"]]
        local_df["Ethnicity"] = [self.eth_dict[eth] for eth in local_df["Ethnicity (Hispanic/Latino)(896)"]]
