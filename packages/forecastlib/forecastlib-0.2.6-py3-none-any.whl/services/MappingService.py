# Intro camaign distance num zrusit
# new_splah prehazet - OK
#intro campaigndistamce dat na max+1
#campaign distance gap na 0 kde je to zaporny - OK
# prihodit poradi kampane v roce
#layout-density_num_m zabit - OK




import itertools
import json

import pandas as pd
import numpy as np

from forecastlib.libs.MappingHelper import MappingHelper
from scipy.interpolate import CubicSpline
import datetime

import logging

logger = logging.getLogger('MappingService')


intents_dict = {
    None: 0,
    "Complimentary Product": 1,
    "Star Product": 2,
    "Units Generator": 3,
    "Anchor": 4,
    "Excitement Creator": 5,
}




class MappingService(object):
    def __init__(self, mapping_json, history: pd.DataFrame, intents: pd.DataFrame):

        self.cols = {
            'PROD_ID': "number",
            'CHAN_CD': "number",
            'CATEGORY_CD': "str",
            'SECTOR_CD': "str",
            'SEGMENT_CD': "str",
            'CONCEPT_CD': "str",
            'CAMPAIGN_CD': "number",
            'CAMPAIGN_INDEX': "number",
            'CAMPAIGN_LENGTH': "number",
            'OFFER_CODE': "str",
            'OFFER_GROUP': "str",
            'OFFER_PERC': "interval",
            'OFFER_PRICE': "interval",
            'UNITS_ACTUAL': "number",
            'UPA_ACTUAL': "number",
            'INTRO_CAMPAIGN_DISTANCE': "number",
            'NEW_SPLASH': "str",
            'SCRATCH_N_SNIFF': "str",
            'VISUAL_FOCUS': "str",
            'CONDITION_FOR_OTHER': "str",
            'LAYOUT_DENSITY': "str",
            'OFFER_DENSITY': "str",
            'OFFER_DENSITY_NUM': "interval",
            'KEY_OFFER_GROUP': "str",
            'KEY_SECTION_GROUP': "str",
            'IS_OUTLIER': "number"
        }

        self.map = mapping_json
        self.history = history
        self.history["PROD_ID"] = self.history["PROD_ID"].astype(np.int64)
        self.history["CHAN_CD"] = self.history["CHAN_CD"].astype(str)
        self.history["OFFER_PERC_M"] = self.history["OFFER_PERC_M"].astype(np.int64)
        self.history["AVG_UPA"] = self.history["AVG_UPA"].astype(float)

        self.intents = intents

        self.map_helper = MappingHelper()

        self.inverted_map = {}

        for c in self.map.keys():
            if self.cols[c] == "interval":
                d = dict((self.map_helper.try_interval(v), k) for k, v in self.map[c].items())
            else:
                d = dict((v, k) for k, v in self.map[c].items())
            self.inverted_map[c] = d

    @staticmethod
    def log(message: str, ts):
        logger.info(message + ": " + str((datetime.datetime.now() - ts).total_seconds()))


    def from_json(self, input_data) -> pd.DataFrame:
        df = pd.DataFrame.from_records(input_data)
        return df

    def to_json(self, output_data: pd.DataFrame) -> json:
        return output_data.to_json(orient='index')

    def apply_mapping(self, original_data: pd.DataFrame) -> pd.DataFrame:
        df = original_data#.copy()
        for c in self.map.keys():
            if c in df.keys():
                if c in self.inverted_map:
                    if self.cols[c] == "interval":
                        df[c+"_M"] = self.map_helper.map_interval(df[c], self.inverted_map[c])
                    else:
                        df[c+"_M"] = df[c].map(self.inverted_map[c])

                    df[c+"_M"] = df[c+"_M"].astype('float') # to allow NaN

        return df

    def remove_mapping(self, mapped_data: pd.DataFrame) -> pd.DataFrame:
        for c in self.map.keys():
            if c in mapped_data.keys():
                mapped_data[c] = mapped_data[c].replace(self.inverted_map[c])

        return mapped_data

    def merge_history(self, df: pd.DataFrame):
        df["PROD_ID"] = df["PROD_ID"].astype(np.int64)
        df["CHAN_CD"] = df["CHAN_CD"].astype(str)
        df["OFFER_PERC_M"] = df["OFFER_PERC_M"].astype(np.int64)


        if 'CHAN_CD' in self.history.columns:
            df = df.merge(self.history[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "AVG_UPA"]], how="left", on=["PROD_ID", "CHAN_CD", "OFFER_PERC_M"])
        else:
            df = df.merge(self.history[["PROD_ID", "OFFER_PERC_M", "AVG_UPA"]], how="left", on=["PROD_ID", "OFFER_PERC_M"])

        #df['AVG_UPA'] = np.where(df["AVG_UPA"].isnull(), -1, df["AVG_UPA"])
        #df['AVG_UPA'] = df['AVG_UPA_FULL']
        #df['AVG_UPA'] = np.where(df["AVG_UPA_FULL"].isnull(), -1, df["AVG_UPA_FULL"])
        df['WITH_HISTORY'] = np.where(df["AVG_UPA"].notnull(), 1, 0)

        return df

    def merge_intents(self, df: pd.DataFrame):
        return MappingService.add_intent(df, self.intents)

    def apply(self, df: pd.DataFrame, features=None):
        logging.info("Applying mapping")
        mapped = self.apply_mapping(df)
        logging.info("Basic mapping applied")
        enriched = MappingService.enrich(mapped, features)
        logging.info("Data enriched")
        with_history = self.merge_history(enriched)
        logging.info("Added history")
        with_intent = self.merge_intents(with_history)
        logging.info("Added intents")

        return with_intent

    @staticmethod
    def map(df: pd.DataFrame):
        # backup original values

        ## Convert columns to category data type and map to integers. Save the mapping into mappings dictionary.
        mappings = {}
        for col in ['CHAN_CD', 'CATEGORY_CD', 'SECTOR_CD',
                    'SEGMENT_CD', 'CONCEPT_CD', 'OFFER_CODE', 'OFFER_GROUP',
                    'SCRATCH_N_SNIFF', 'VISUAL_FOCUS', 'CONDITION_FOR_OTHER', 'LAYOUT_DENSITY', 'OFFER_DENSITY', 'KEY_OFFER_GROUP', 'KEY_SECTION_GROUP']:
            df[col+"_M"] = df[col].astype('category')
            mappings[col] = dict(zip(df[col+"_M"].cat.codes, df[col+"_M"]))
            df[col+"_M"] = df[col+"_M"].cat.codes

        df['OFFER_PERC_M'] = pd.cut(df['OFFER_PERC'], bins=MappingService.get_perc_bins())
        df['OFFER_PRICE_M'] = pd.cut(df['OFFER_PRICE'], bins=MappingService.get_price_bins())
        df['OFFER_DENSITY_NUM_M'] = pd.cut(df['OFFER_DENSITY_NUM'], bins=MappingService.get_offer_density_bins())

        for col in ['OFFER_PERC', 'OFFER_PRICE', 'OFFER_DENSITY_NUM']:
            mappings[col] = dict(zip(df[col+"_M"].cat.codes, df[col+"_M"]))
            df[col+"_M"] = df[col+"_M"].cat.codes


        # Manual order of NEW_SPLASH
        new_splash_type = pd.CategoricalDtype(categories=["N-0", "N-N2", "N-N"], ordered=True)
        df["NEW_SPLASH_M"] = df["NEW_SPLASH"].astype(new_splash_type)
        mappings["NEW_SPLASH"] = dict(zip(df["NEW_SPLASH_M"].cat.codes, df["NEW_SPLASH_M"]))
        df["NEW_SPLASH_M"] = df["NEW_SPLASH_M"].cat.codes


        return df, mappings

    @staticmethod
    def enrich(df: pd.DataFrame, features = None):
        ts = datetime.datetime.now()
        MappingService.log("Enrich started", ts)
        ts = datetime.datetime.now()

        temp = df['CAMPAIGN_CD'].astype(str)
        df['YEAR'] = temp.str[:4].astype(np.int64)
        df['MONTH'] = temp.str[4:].astype(np.int64)  # temporary placeholder, will be overwritten
        df['CAMPAIGN_DAY_END'] = (
                    (df['MONTH'] - 1) * 21 + 28)  # represents number of days since the beginning of the year
        df['CAMPAIGN_DAY_END'] = pd.to_datetime(df['YEAR'] * 1000 + df['CAMPAIGN_DAY_END'], format='%Y%j')
        df['CAMPAIGN_DAY_START'] = df['CAMPAIGN_DAY_END'] - pd.to_timedelta(df['CAMPAIGN_LENGTH'], unit='d')

        df['MONTH'] = df['CAMPAIGN_DAY_START'].dt.month.astype(np.int8)
        df['YEAR'] = df['YEAR'].astype(np.int16)
        df['WEEK'] = df['CAMPAIGN_DAY_START'].dt.week.astype(np.int8)

        df['CAMPAIGN_ID'] = df['CHAN_CD'].map(str) + df['CAMPAIGN_CD'].map(str)

        df['CAMPAIGN_IN_YEAR'] = df['CAMPAIGN_CD'].mod(df['YEAR'].astype(int) * 100)

        df["UPA_PER_CAMPAIGN"] = df["UPA_ACTUAL"].map(float) * 20 / df["CAMPAIGN_LENGTH"].map(float)
        df["OFFER_PRICE_ORIGINAL"] = np.where(df["OFFER_PERC"] > 0, df["OFFER_PRICE"] * 100 / (df["OFFER_PERC"]), df["OFFER_PRICE"])

        df['OFFER_PRICE_ORIGINAL'] = pd.cut(df['OFFER_PRICE_ORIGINAL'], bins=MappingService.get_price_bins())
        df['OFFER_DENSITY_NUM_ZERO'] = np.where(df['OFFER_DENSITY_NUM'] == 0, 0, 1).astype(np.int8)
        MappingService.log("Basic enrichment", ts)
        ts = datetime.datetime.now()

        if features is None or 'PRODUCTS_DISCOUNT_COUNT' in features:
            ## Create a new column with a count of products within the same discount group and catalogue.
            temp = df.groupby(by=['OFFER_PERC_M', 'CAMPAIGN_ID']).count()[['PROD_ID']].to_dict()
            mapping_products_discount = {}
            for k, v in temp['PROD_ID'].items():
                mapping_products_discount[k] = v
            df['PRODUCTS_DISCOUNT_COUNT'] = list(zip(df['OFFER_PERC_M'], df['CAMPAIGN_ID']))
            df['PRODUCTS_DISCOUNT_COUNT'] = df['PRODUCTS_DISCOUNT_COUNT'].map(mapping_products_discount)
            MappingService.log("PRODUCTS_DISCOUNT_COUNT", ts)
            ts = datetime.datetime.now()

        if features is None or 'PRODUCTS_PRICE_COUNT' in features:
            ## Create a new column with a count of products within the same price group and catalogue.
            temp = df.groupby(by=['OFFER_PRICE_M', 'CAMPAIGN_ID']).count()[['PROD_ID']].to_dict()
            mapping_products_price = {}
            for k, v in temp['PROD_ID'].items():
                mapping_products_price[k] = v
            df['PRODUCTS_PRICE_COUNT'] = list(zip(df['OFFER_PRICE_M'], df['CAMPAIGN_ID']))
            df['PRODUCTS_PRICE_COUNT'] = df['PRODUCTS_PRICE_COUNT'].map(mapping_products_price)
            MappingService.log("PRODUCTS_PRICE_COUNT", ts)
            ts = datetime.datetime.now()

        if features is None or any(f in features for f in ['OFFER_PERC_M_LAG_' + str(x) for x in range(0, 11)]) or any(f in features for f in ['OFFER_PRICE_M_LAG_' + str(x) for x in range(0, 11)]):
            ## Create five lags of discount, price, and number of active consultants and columns describing the gap between the current and lagged value in weeeks.
            for col in ['OFFER_PERC_M', 'OFFER_PRICE_M']:
                for i in range(1, 5):
                    if features is None or any(f in features for f in [col + '_LAG_' + str(i), col + '_LAG_' + str(i) + '_WEEKS_AGO']):
                        temp = df.groupby(by=['PROD_ID', 'CHAN_CD_M'])[col].shift(i).rename(col + '_LAG_' + str(i))
                        df = pd.concat([df, temp], axis=1)
                        temp = df.groupby(by=['PROD_ID', 'CHAN_CD_M'])['CAMPAIGN_DAY_START'].shift(i).rename(
                            col + '_LAG_' + str(i) + '_WEEKS_AGO')
                        df = pd.concat([df, temp], axis=1)
                        df[col + '_LAG_' + str(i) + '_WEEKS_AGO'] = round(
                            (df['CAMPAIGN_DAY_START'] - df[col + '_LAG_' + str(i) + '_WEEKS_AGO']).dt.days / 7)
                        df[col + '_LAG_' + str(i)] = np.where(df[col + '_LAG_' + str(i)].isnull(), 0,
                                                              df[col + '_LAG_' + str(i)])
                        df[col + '_LAG_' + str(i) + '_WEEKS_AGO'] = np.where(df[col + '_LAG_' + str(i) + '_WEEKS_AGO'].isnull(),
                                                                         0, df[col + '_LAG_' + str(i) + '_WEEKS_AGO'])
            MappingService.log("LAGS", ts)
            ts = datetime.datetime.now()

            ## Actives count increase since last campaign
            actives = df.groupby(by=['CAMPAIGN_ID'])['ACTIVE_CONSULTANTS'].mean().shift(1).rename(
                'ACTIVE_CONSULTANTS_LAG_1')
            mapping = {}
            for k, v in actives.items():
                mapping[k] = v
            df['ACTIVE_CONSULTANTS_LAG_1'] = df['CAMPAIGN_ID']
            df['ACTIVE_CONSULTANTS_LAG_1'] = df['ACTIVE_CONSULTANTS_LAG_1'].map(mapping)
            df['ACTIVE_CONSULTANTS_LAG_1'] = np.where(df['ACTIVE_CONSULTANTS_LAG_1'].isnull(), df['ACTIVE_CONSULTANTS'],
                                                      df['ACTIVE_CONSULTANTS_LAG_1'])

            df['ACTIVE_CONSULTANTS_DIFF'] = df['ACTIVE_CONSULTANTS'].map(float) / df['ACTIVE_CONSULTANTS_LAG_1'].map(float)
            MappingService.log("ACTIVE_CONSULTANTS_LAG_1", ts)
            ts = datetime.datetime.now()

        if features is None or any(f in features for f in ['COUNT_PRODUCTS_CATEGORY_M', 'COUNT_PRODUCTS_SEGMENT_M', 'COUNT_PRODUCTS_SECTOR_M']):
            ## Count of unique products per category, sector, and segment within a single issue of catalogue.
            for col in ['CATEGORY_CD_M', 'SECTOR_CD_M', 'SEGMENT_CD_M']:
                temp = df.groupby(by=[col, 'CAMPAIGN_ID']).count()[['PROD_ID']].to_dict()
                mapping = {}
                for k, v in temp['PROD_ID'].items():
                    mapping[k] = v
                df['COUNT_PRODUCTS_' + col.replace('_CD', '')] = list(zip(df[col], df['CAMPAIGN_ID']))
                df['COUNT_PRODUCTS_' + col.replace('_CD', '')] = df['COUNT_PRODUCTS_' + col.replace('_CD', '')].map(mapping)
            MappingService.log("COUNT_PRODUCTS_", ts)
            ts = datetime.datetime.now()

        if features is None or any(f in features for f in ['PRODUCTS_WITH_PERC_' + str(x) for x in range(0, 11)] or 'PRODUCTS_IN_CAMPAIGN' in features):
            ## Count total products in each campaign
            products_in_campaign = df.groupby(by=['CAMPAIGN_ID']).count()[["PROD_ID"]]
            mapping = {}
            for k, v in products_in_campaign['PROD_ID'].items():
                mapping[k] = v
            df['PRODUCTS_IN_CAMPAIGN'] = df['CAMPAIGN_ID']
            df['PRODUCTS_IN_CAMPAIGN'] = df['PRODUCTS_IN_CAMPAIGN'].map(mapping)
            MappingService.log("PRODUCTS_IN_CAMPAIGN", ts)
            ts = datetime.datetime.now()

            ## Count total products in each offer discount category
            for i in range(0, MappingService.get_perc_bins().__len__()):
                if features is None or 'PRODUCTS_WITH_PERC_' + str(i) in features:
                    items = df[df['OFFER_PERC_M'] == i]
                    bycampaign = items.groupby(by=['CAMPAIGN_ID']).count()[["PROD_ID"]]

                    mapping = {}
                    for k, v in bycampaign['PROD_ID'].items():
                        prods = np.average(df[df['CAMPAIGN_ID'] == k]['PRODUCTS_IN_CAMPAIGN'])

                        mapping[k] = 0 if prods == 0 else v / prods
                    df['PRODUCTS_WITH_PERC_' + str(i)] = df['CAMPAIGN_ID']
                    df['PRODUCTS_WITH_PERC_' + str(i)] = df['PRODUCTS_WITH_PERC_' + str(i)].map(mapping)
                    df['PRODUCTS_WITH_PERC_' + str(i)] = np.where(df['PRODUCTS_WITH_PERC_' + str(i)].isnull(), 0, df['PRODUCTS_WITH_PERC_' + str(i)])  # remove NaNs
            MappingService.log("PRODUCTS_WITH_PERC_", ts)
            ts = datetime.datetime.now()

        if features is None or 'INTRO_CAMPAIGN_DISTANCE' in features:
            # Remover 500 from Intro_capaign_distance
            s = df["INTRO_CAMPAIGN_DISTANCE"]
            max_campaign_distance = s[s < 500].max()
            df["INTRO_CAMPAIGN_DISTANCE_M"] = np.where(df["INTRO_CAMPAIGN_DISTANCE"] == 500, max_campaign_distance + 1,
                                                       df["INTRO_CAMPAIGN_DISTANCE"])
            MappingService.log("INTRO_CAMPAIGN_DISTANCE", ts)
            ts = datetime.datetime.now()


        if features is None or any(f in features for f in ['LAST_CAMPAIGN_GAP', 'PREV_INTRO_CAMPAIGN_DISTANCE']):
            ## Count gaps in campaigns
            temp = df.groupby(by=['PROD_ID', 'CHAN_CD_M'])
            col = temp['INTRO_CAMPAIGN_DISTANCE_M'].shift(1).rename('PREV_INTRO_CAMPAIGN_DISTANCE')
            df = pd.concat([df, col], axis=1)
            df['LAST_CAMPAIGN_GAP'] = df['INTRO_CAMPAIGN_DISTANCE_M'] - df['PREV_INTRO_CAMPAIGN_DISTANCE'] - 1

            df['LAST_CAMPAIGN_GAP'] = np.where(df['LAST_CAMPAIGN_GAP'].isnull(), 0, df['LAST_CAMPAIGN_GAP'])
            df['LAST_CAMPAIGN_GAP'] = np.where(df['LAST_CAMPAIGN_GAP'] < 0, 0, df['LAST_CAMPAIGN_GAP'])
            df['PREV_INTRO_CAMPAIGN_DISTANCE'] = np.where(df['PREV_INTRO_CAMPAIGN_DISTANCE'].isnull(), 0, df['PREV_INTRO_CAMPAIGN_DISTANCE'])
            MappingService.log("LAST_CAMPAIGN_GAP", ts)
            ts = datetime.datetime.now()

        if features is None or any(f in features for f in ['CONCEPTS_PER_PAGE']):
            concept_per_page = df.groupby(by=['CHAN_CD_M', 'CAMPAIGN_CD', 'PAGE_NUMBER'])["CONCEPT_CD"].nunique().rename('CONCEPTS_PER_PAGE')
            df = df.merge(concept_per_page.reset_index(), how="left", left_on=['CHAN_CD_M', 'CAMPAIGN_CD', 'PAGE_NUMBER'], right_on=['CHAN_CD_M', 'CAMPAIGN_CD', 'PAGE_NUMBER'])

        return df

    @staticmethod
    def add_full_history(df: pd.DataFrame, last_known_year: int):
        nolaunch = df[df.INTRO_CAMPAIGN_DISTANCE > 0]

        no_last_year = nolaunch[nolaunch["YEAR"] <= last_known_year]

        cumsum = no_last_year.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].cumsum()
        cumcount = no_last_year.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].cumcount()

        df['CUMSUM'] = cumsum - nolaunch['UPA_ACTUAL']
        df['CUMSUM_WITH_FIRST'] = cumsum
        df['CUMCOUNT'] = cumcount
        df['AVG_UPA'] = df['CUMSUM'] / df['CUMCOUNT']

        # Propagate last known AVG_UPA

        concept_upa = no_last_year.groupby(by=['CONCEPT_CD', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].mean().rename("UPA_CONCEPT").reset_index()
        df = df.merge(concept_upa, left_on=['CONCEPT_CD', 'CHAN_CD', 'OFFER_PERC_M'], right_on=['CONCEPT_CD', 'CHAN_CD', 'OFFER_PERC_M'], how="left")

        type_upa = no_last_year.groupby(by=['TYPE_CD', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].mean().rename("UPA_TYPE").reset_index()
        df = df.merge(type_upa, left_on=['TYPE_CD', 'CHAN_CD', 'OFFER_PERC_M'],right_on=['TYPE_CD', 'CHAN_CD', 'OFFER_PERC_M'], how="left")

        segment_upa = no_last_year.groupby(by=['SEGMENT_CD', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].mean().rename("UPA_SEGMENT").reset_index()
        df = df.merge(segment_upa, left_on=['SEGMENT_CD', 'CHAN_CD', 'OFFER_PERC_M'],right_on=['SEGMENT_CD', 'CHAN_CD', 'OFFER_PERC_M'], how="left")

        sector_upa = no_last_year.groupby(by=['SECTOR_CD', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].mean().rename("UPA_SECTOR").reset_index()
        df = df.merge(sector_upa, left_on=['SECTOR_CD', 'CHAN_CD', 'OFFER_PERC_M'],right_on=['SECTOR_CD', 'CHAN_CD', 'OFFER_PERC_M'], how="left")

        category_upa = no_last_year.groupby(by=['CATEGORY_CD', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].mean().rename("UPA_CATEGORY").reset_index()
        df = df.merge(category_upa, left_on=['CATEGORY_CD', 'CHAN_CD', 'OFFER_PERC_M'], right_on=['CATEGORY_CD', 'CHAN_CD', 'OFFER_PERC_M'], how="left")

        fallback_upa = no_last_year.groupby(by=['CAMPAIGN_CD', 'CHAN_CD'])['UPA_ACTUAL'].mean().rename("UPA_FALLBACK").reset_index()
        df = df.merge(fallback_upa, left_on=['CAMPAIGN_CD', 'CHAN_CD'], right_on=['CAMPAIGN_CD', 'CHAN_CD'], how="left")

        df = df.sort_values(by=['CAMPAIGN_CD', 'CHAN_CD', 'PROD_ID'])
        df['AVG_UPA'] = df.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['AVG_UPA'].fillna(method='ffill')

        df["UPA_BASELINE"] = np.where(df["AVG_UPA"].notnull() & (df['INTRO_CAMPAIGN_DISTANCE'] > 10), df["AVG_UPA"],
                                  np.where(df["UPA_CONCEPT"].notnull(), df["UPA_CONCEPT"],
                                           np.where(df["UPA_TYPE"].notnull(), df["UPA_TYPE"],
                                               np.where(df["UPA_SEGMENT"].notnull(), df["UPA_SEGMENT"],
                                                        np.where(df["UPA_SECTOR"].notnull(), df["UPA_SECTOR"],
                                                                 np.where(df["UPA_CATEGORY"].notnull(), df["UPA_CATEGORY"], df["UPA_FALLBACK"]))))))

        df['UPA_BASELINE'] = df.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_BASELINE'].fillna(method='ffill')

        df['WITH_HISTORY'] = np.where(df["AVG_UPA"].notnull(), 1, 0)
        df['CUMSUM'] = np.where(df["CUMSUM"].isnull(), 0, df["CUMSUM"])
        df['CUMCOUNT'] = np.where(df["CUMCOUNT"].isnull(), 0, df["CUMCOUNT"])

        df['UPA_CATEGORY'] = df['UPA_CATEGORY'].interpolate()  # without fillin limit
        df['UPA_SEGMENT'] = np.where(df['UPA_SEGMENT'].isnull(), df['UPA_CATEGORY'], df['UPA_SEGMENT'])
        df['UPA_TYPE'] = np.where(df['UPA_TYPE'].isnull(), df['UPA_SEGMENT'], df['UPA_TYPE'])
        #df['UPA_BASELINE'] = np.where((df['PREV_INTRO_CAMPAIGN_DISTANCE'] > 10) & (df['YEAR'] <= last_known_year), df['UPA_BASELINE'], df['UPA_SEGMENT'])

        return df

    @staticmethod
    def get_last_history(df: pd.DataFrame) -> pd.DataFrame:
        last = df[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "UPA_BASELINE"]].groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])
        #last = df[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "AVG_UPA"]].groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])

        last = last.last()
        last = last.reset_index()

        return last.rename(columns={'UPA_BASELINE':'AVG_UPA'})

    @staticmethod
    def get_history(df: pd.DataFrame) -> pd.DataFrame:
        # Ignore first campaign
        known = df[df.INTRO_CAMPAIGN_DISTANCE > 0]

        # Add avg_upa column per discount group
        history = known.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M',  "CHAN_CD"])['UPA_ACTUAL'].mean()
        history = history.reset_index()
        history.rename(columns={'UPA_ACTUAL':'AVG_UPA'}, inplace=True)

        #return history
        # Calculate missing AVG_UPAs
        history["SAMPLES"] = history.groupby(["PROD_ID"])["PROD_ID"].transform("count")
        products = df[["CHAN_CD", "PROD_ID"]].unique()
        product_list = list(itertools.product(products, range(0, 10)))
        product_discount_matrix = pd.DataFrame(data=product_list, columns=["PROD_ID",  "CHAN_CD", "OFFER_PERC_M"])

        with_history = product_discount_matrix.merge(history, how="left", on=["PROD_ID",  "CHAN_CD", "OFFER_PERC_M"])


#        # calculate reference UPA for each discount category
#        avg_upas = with_history.groupby( "CHAN_CD", "OFFER_PERC_M")["AVG_UPA"].mean()

        # get avg upa polynom
        #poly = CubicSpline(range(0, 10), avg_upas)

        #avg_discount_category = with_history[with_history["AVG_UPA"].notnull()].groupby("PROD_ID")["OFFER_PERC_M"].mean()
        #pivoted = with_history[["PROD_ID", "OFFER_PERC_M",  "CHAN_CD",  "AVG_UPA"]].pivot(index="PROD_ID", columns="OFFER_PERC_M", values="AVG_UPA")

        #summary = pivoted[[]]  # get just indices
        #summary["AVG_UPA"] = pivoted[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]].mean(axis=1)
        #summary = summary.join(avg_discount_category, how="left", rsuffix="_AVG")
        #summary["REF_UPA"] = [poly(x) for x in summary["OFFER_PERC_M"]]
        #summary["REF_MULTIPLIER"] = summary["AVG_UPA"] / summary["REF_UPA"]

        #with_history = with_history.join(avg_upas, how="left", on="OFFER_PERC_M", rsuffix="_REF")
        #with_history = with_history.join(summary[["REF_MULTIPLIER"]], how="left", on="PROD_ID")

        #with_history["AVG_UPA_CALC"] = with_history["AVG_UPA_REF"] * with_history["REF_MULTIPLIER"]
        #with_history["AVG_UPA_FULL"] = np.where(with_history["AVG_UPA"].notnull(), with_history["AVG_UPA"], with_history["AVG_UPA_CALC"])

        return with_history

    @staticmethod
    def get_intent(file: str, region: str) -> pd.DataFrame:
        intents = pd.read_excel(file)
        intents["INTENT"] = intents[region]
        intents["INTENT_M"] = intents[region].map(intents_dict)

        intents = intents.rename(columns={"Code": "PROD_ID"})

        return intents

    @staticmethod
    def add_intent(df: pd.DataFrame, intents: pd.DataFrame):
        df = pd.merge(df, intents[["PROD_ID", "INTENT", "INTENT_M"]], how="left", on=["PROD_ID"])
        df["INTENT_M"] = np.where(df["INTENT_M"].isnull(), 0, df["INTENT_M"])
        df["INTENT"] = np.where(df["INTENT"].isnull(), 0, df["INTENT"])

        return df

    @staticmethod
    def get_price_per_bp(file: str) -> pd.DataFrame:
        bps = pd.read_csv(file, sep=',')
        return bps

    @staticmethod
    def add_price_per_bp(df: pd.DataFrame, bps: pd.DataFrame):
        ppbp = pd.merge(df[["PROD_ID", "OFFER_PRICE", "OFFER_PERC"]], bps, how="left", on=["PROD_ID"])

        ppbp["OFFER_PRICE_ORIGINAL"] = np.where(ppbp["OFFER_PERC"] == 0, ppbp["OFFER_PRICE"],  ppbp["OFFER_PRICE"] * 100.0 / ppbp["OFFER_PERC"])
        df["PRICE_PER_BP"] = ppbp["BP"] / ppbp["OFFER_PRICE_ORIGINAL"]
        df["PRICE_PER_BV"] = ppbp["BV"] / ppbp["OFFER_PRICE_ORIGINAL"]

        return df

    @staticmethod
    def get_perc_bins():
        perc_bins = [x for x in range(0, 120, 10)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        perc_bins = [-1] + perc_bins

        return perc_bins

    @staticmethod
    def get_price_bins():
        price_bins = [x for x in range(0, 120, 20)]
        price_bins += [x for x in range(150, 550, 50)]
        price_bins += [x for x in range(600, 1800, 200)]
        price_bins += [x for x in range(2000, 3600, 400)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        price_bins = [-1] + price_bins

        return price_bins

    @staticmethod
    def get_layout_density_bins():
        layout_density_bins = [x for x in range(0, 10, 1)]
        layout_density_bins += [x for x in range(10, 40, 2)]
        layout_density_bins += [x for x in range(40, 60, 5)]
        layout_density_bins += [x for x in range(60, 220, 20)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        layout_density_bins = [-1] + layout_density_bins

        return layout_density_bins

    @staticmethod
    def get_offer_density_bins():
        offer_density_bins = [x for x in range(0, 10, 1)]
        offer_density_bins += [x for x in range(10, 20, 2)]
        offer_density_bins += [x for x in range(20, 40, 5)]
        offer_density_bins += [x for x in range(40, 100, 10)]
        offer_density_bins += [x for x in range(100, 200, 20)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        offer_density_bins = [-1] + offer_density_bins

        return offer_density_bins
