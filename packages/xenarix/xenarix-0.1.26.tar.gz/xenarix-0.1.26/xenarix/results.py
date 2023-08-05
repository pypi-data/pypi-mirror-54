# coding=utf-8
import numpy as np
import pandas as pd
import os
import datetime
from .common import *
from collections import namedtuple, OrderedDict

T_Row = namedtuple('T_Row', 'INDEX DATE T DT INTERPOLATED')


def build_result_data_info2(set_name, scen_name, result_name):
    result_info_file_path = xen_result_dir() + '/' + set_name + '/' + scen_name + '/' + result_name

    return build_result_data_info(result_info_file_path)


def build_result_data_info(result_info_file_path):
    if not os.path.exists(result_info_file_path):
        raise Exception("result info load error. file not exist.")

    result_data_info = pd.read_csv(result_info_file_path + '/' + resultinfo_filename, delimiter='|')

    return result_data_info


def build_cali_result_detail_info2(cali_name, model_name, result_name):
    result_info_file_path = xen_cali_result_dir() + '/' + cali_name + '/' + model_name + '/' + result_name

    return build_cali_result_detail_info(result_info_file_path)


def build_cali_result_detail_info(result_info_file_path):
    if not os.path.exists(result_info_file_path):
        raise Exception("cali result info load error. result does not exist : {0}".format(result_info_file_path))

    filename = result_info_file_path + '/' + cali_detailinfo_filename
    if not os.path.exists(filename):
        raise Exception("cali result datail file does not exist : {0}".format(filename))

    return pd.read_csv(filename, delimiter='|')


def build_cali_result_parameters_info2(cali_name, model_name, result_name):
    result_info_file_path = xen_cali_result_dir() + '/' + cali_name + '/' + model_name + '/' + result_name

    return build_cali_result_parameters_info(result_info_file_path)


def build_cali_result_parameters_info(result_info_file_path):
    if not os.path.exists(result_info_file_path):
        raise Exception("cali result info load error. result does not exist : {0}".format(result_info_file_path))

    filename = result_info_file_path + '/' + cali_parametersinfo_filename
    if not os.path.exists(filename):
        raise Exception("cali result parameters file does not exist : {0}".format(filename))

    return pd.read_csv(filename, delimiter='|')


def build_timegrid_info2(set_name, scen_name, result_name):
    timegrid_info_file_path = os.path.join(xen_result_dir(), set_name, scen_name, result_name)

    return build_timegrid_info(timegrid_info_file_path)


def build_timegrid_info(timegrid_info_file_path):
    if not os.path.exists(timegrid_info_file_path):
        raise Exception("result info load error. file not exist.")

    result_data_info = pd.read_csv( os.path.join(timegrid_info_file_path, timegridinfo_filename),
                                    header=None,
                                    delimiter='|',
                                    usecols=[0,1,2,3],
                                    names=['INDEX','DATE', 'T','DT'])

    return result_data_info


# file timegrid
class TimeGrid:
    def __init__(self, set_name, scen_name, result_name):
        self.set_name = set_name
        self.scen_name = scen_name
        self.result_name = result_name
        self.initialize()

    def __iter__(self):
        return self.data.itertuples(index=False)

    def __getitem__(self, item):
        return self.data.iloc[item]

    def initialize(self):
        self.data = build_timegrid_info2(self.set_name, self.scen_name, self.result_name)

    ###
    # return T_Row : left side only
    def find_closest_row_by_date(self, d):
        _d = d
        if isinstance(d, datetime.datetime):
            d = d.strftime("%Y-%m-%d")

        rows = self.data['DATE']

        pos = 0
        for r in rows:
            if _d <= r:
                break
            pos += 1

        # selecte before row
        pos -= 1

        return T_Row(pos, self.data.loc[pos]['DATE'], self.data.loc[pos]['T'], self.data.loc[pos]['DT'], False)

    # return T_Row : left side only
    def find_closest_row_by_t(self, t):
        _t = t

        rows = self.data['T']

        pos = 0
        for r in rows:
            if _t <= r:
                break
            pos += 1

        # selecte before row
        pos -= 1

        return T_Row(pos, self.data.loc[pos]['DATE'], self.data.loc[pos]['T'], self.data.loc[pos]['DT'], False)

    def has_date(self, d):
        return (self.data['DATE'] == d).any()

    def has_t(self, t, error=error_bound):
        return (self.data['T'].between(t - error, t + error)).any()

    def find_row_by_date(self, d, interpolation=False):
        def interpolate(before_t_row, d):
            before_date = before_t_row.DATE
            before_t = before_t_row.T

            before_datetime = datetime.datetime.strptime(before_date, '%Y-%m-%d')
            d_datetime = datetime.datetime.strptime(d, '%Y-%m-%d')
            days = (d_datetime - before_datetime).days
            t = before_t + float(days)/365
            dt = t - before_t

            return T_Row(before_t_row.INDEX+0.5, d, t, dt, True)

        rows = self.data[self.data['DATE'] == d]

        if rows.empty:
            if interpolation:
                last_row = self.data.iloc[-1]
                if last_row['DATE'] < d:
                    raise Exception(d + ' is out of range, Max Date : ' + last_row['DATE'])
                t_row = self.find_closest_row_by_date(d)
                return interpolate(t_row, d)
            else:
                return None
        else:
            row = rows.iloc[0]
            pos = row['INDEX']
            return T_Row(pos, row['DATE'], row['T'], row['DT'], False)

    def find_row_by_t(self, t, interpolation=False, error=error_bound):
        def interpolate(before_t_row, t):
            before_date = before_t_row.DATE
            before_t = before_t_row.T
            before_datetime = datetime.datetime.strptime(before_date, '%Y-%m-%d')

            dt = t - before_t
            date = before_datetime + datetime.timedelta(days=int(dt * 365))

            return T_Row(before_t_row.INDEX, date.strftime("%Y-%m-%d"), t, dt, True)

        rows = self.data[self.data['T'].between(t - error, t + error)]

        if rows.empty:
            if interpolation:
                t_row = self.find_closest_row_by_t(t)
                return interpolate(t_row, t)
            else:
                return None
        else:
            row = rows.iloc[0]
            pos = row['INDEX']
            return T_Row(pos, row['DATE'], row['T'], row['DT'], False)

    def pre_t_row(self, t_row):
        if not isinstance(t_row, T_Row):
            raise Exception('T_Row type is needed')

        if not t_row.INDEX == 0:
            if t_row.INTERPOLATED:
                return self.pandas_row_to_t_row(self.data.iloc[int(t_row.INDEX)])
            else:
                return self.pandas_row_to_t_row(self.data.iloc[int(t_row.INDEX) - 1])

        return None

    def next_t_row(self, t_row):
        if not isinstance(t_row, T_Row):
            raise Exception('T_Row type is needed')

        if not t_row.INDEX == len(self.data.index):
            return self.pandas_row_to_t_row(self.data.iloc[int(t_row.INDEX) + 1])

        return None

    def pandas_row_to_t_row(self, pandas_row):
        return T_Row(pandas_row['INDEX'], pandas_row['DATE'], pandas_row['T'], pandas_row['DT'], False)


# file load numpy wrapping
class ResultModel:
    def __init__(self, result_data_info_row, timegrid):
        # REF_DT
        # RESULT_ID
        # RESULT_NM
        # SCENARIO_ID
        # SHOCK_NAME
        # SHOCK_SEQ
        # REF_INDEX_CD
        # MODEL_TYPE
        # CALCULATION
        # ORIGIN_CURRENCY
        # TARGET_CURRENCY
        # OUTPUT
        # CALC_TYPE
        # SCENARIO_NUM
        # T_COUNT
        # STEP_PER_YEAR
        # GEN_START_TIME
        # GEN_END_TIME
        # GEN_TYPE
        # STATUS_MESSAGE
        # STATUS
        # DESCRIPTION
        # FILEPATH
        self.name = result_model_key(result_data_info_row)

        self.index_name = result_data_info_row['REF_INDEX_CD']
        self.shock_name = result_data_info_row['SHOCK_NAME']
        self.filepath = result_data_info_row['FILEPATH']
        self.scenario_num = result_data_info_row['SCENARIO_NUM']
        self.t_count = result_data_info_row['T_COUNT']
        self.calc_name = result_data_info_row['CALCULATION']
        self.calc_type = result_data_info_row['CALC_TYPE']
        self.timegrid = timegrid
        self.info = result_data_info_row

        if self.calc_type == 'DEBUGPRINT':
            self.scenario_num = 1
        self.data = np.memmap(self.filepath, np.double, mode='r', shape=(self.scenario_num, self.t_count))

    def x0(self):
        return self.data[0][0]

    def average(self):
        return np.average(self.data, axis=0)

    def analytic(self):
        ue_filepath = self.filepath.replace('_value', '_UNCONDITIONALEXPECTATION')
        v = np.memmap(ue_filepath, np.double, mode='r', shape=(1, self.t_count))
        return v

    # def load(self, start_pos=None, end_pos=None):
    #     if start_pos is None:
    #         start_pos = 1
    #
    #     self.scenario_num = self.result_data_info['SCENARIO_NUM'][0]
    #
    #     if end_pos is None:
    #         end_pos = self.scenario_num
    #
    #     if self.calc_type == 'DEBUGPRINT':
    #         self.scenario_num = 1
    #
    #     self.t_count = self.result_data_info['T_COUNT'][0]
    #     self.arr = np.memmap(self.file_full_path, np.double, mode='r', shape=(self.scenario_num, self.t_count))[start_pos-1:end_pos].tolist()
    #     return self.arr
    #
    # def average(self, start_pos=None, end_pos=None):
    #     if self.arr is None:
    #         self.load(start_pos, end_pos)
    #
    #     return np.average(self.arr, axis=0)

    # return value selected scenario_count
    def interpolated_value(self, t_row, scenario_count = 0):
        return np.interp(t_row.T, self.timegrid.data['T'], self.data[scenario_count,:])

    def interpolated_values(self, t_row):
        if not isinstance(t_row, T_Row):
            return None

        if self.timegrid.has_date(t_row.DATE):
            return self.data[:, t_row.INDEX]

        pre_t_row = self.timegrid.pre_t_row(t_row)
        next_t_row = self.timegrid.next_t_row(t_row)

        y0 = self.data[:, pre_t_row.INDEX]
        y1 = self.data[:, next_t_row.INDEX]
        t0 = pre_t_row.T
        t1 = next_t_row.T
        t = t_row.T

        y = y0 + (t-t0) * (y1-y0) / (t1-t0)

        #print str(t0) + ' : ' + str(t1) + ',' + str(t)
        #print str(y0) + ' : ' + str(y1) + ',' + str(y)

        return y

    # def interpolated_value2(self, scenario_count, t_row):
    #     if isinstance(t_row, T_Row):
    #         pre_t_row = self.timegrid.pre_t_row(t_row)
    #         next_t_row = self.timegrid.next_t_row(t_row)
    #
    #         y0 = self.data[scenario_count][pre_t_row.INDEX]
    #         y1 = self.data[scenario_count][next_t_row.INDEX]
    #         t0 = pre_t_row.T
    #         t1 = next_t_row.T
    #         t = t_row.T
    #
    #         y = y0 + (t-t0)* (y1-y0) / (t1-t0)
    #
    #         #print str(t0) + ' : ' + str(t1) + ',' + str(t)
    #         #print str(y0) + ' : ' + str(y1) + ',' + str(y)
    #
    #         return y

    # return shape : (scenario_num, t_count)
    # def interpolated_values(self, t_row):
    #     if isinstance(t_row, T_Row):
    #         pre_t_row = self.timegrid.pre_t_row(t_row)
    #         next_t_row = self.timegrid.next_t_row(t_row)
    #
    #         y0 = self.data[scenario_count][pre_t_row.INDEX]
    #         y1 = self.data[scenario_count][next_t_row.INDEX]
    #         print str(y0) + ' : ' + str(y1)
    #
    #         # y = y0 + (t-t0)* (y1-y0) / (t1-t0)
    #         y = y0 + (t_row.DT) * (y1 - y0) / (next_t_row.DT)
    #
    #         return y


    def export_csv(self, filename):
        np.savetxt(filename, self.data, delimiter=",")


class TimeSeriesResultModel:
    def __init__(self, timeseries, timegrid):
        self.timegrid = timegrid
        self.timeseries = timeseries

        # return value selected scenario_count
    def interpolated_value(self, t_row, scenario_count = 0):
        return np.interp(t_row.T, self.timegrid.data['T'], self.data[scenario_count,:])



class ResultObj:
    def __init__(self, set_name, scen_name, result_name):
        self.set_name = set_name
        self.scen_name = scen_name
        self.result_name = result_name
        # self.process_names = None
        self.scenario_num = 0
        self.t_count = 0
        self.res_models = OrderedDict()
        self.timegrid = None
        self.result_data_info = None
        self.initialize()

    # def summary(self):
    #     return ''

    def initialize(self):
        self.result_data_info = build_result_data_info2(self.set_name, self.scen_name, self.result_name)

        # timegrid
        # self.timegrid = build_timegrid_info2(self.set_name, self.scen_name, self.result_name)
        self.timegrid = TimeGrid(self.set_name, self.scen_name, self.result_name)

        # models
        # self.names = []
        for index, row in self.result_data_info.iterrows():
            # if debug 가 아니면 넣기...?
            rm = ResultModel(row, self.timegrid)

            self.res_models[rm.name] = rm
            #self.models[str.upper(key)] = rm

            # self.names.append(rm.name)

    # scen_count = 0 to scen_num - 1
    def get_multipath(self, scen_count, type='namedtuple'):
        if type == 'namedtuple':
            data = {}
            for m in self.res_models.values():
                data[m.name] = m.data[scen_count]
            return pd.DataFrame.from_dict(data)
        else:
            res = []

            for m in self.res_models.values():
                res.append(m.data[scen_count])

            return np.array(res)

    # model_count = 0 to model_num - 1
    def get_modelpath(self, model_count=0):
        return list(self.res_models.values())[model_count].data

    # model name
    def get_modelpath_by_name(self, model_name):
        return self.res_models[model_name].data

    # find ResultModel using key
    def get_resultModel(self, model, calc=None, shock='BASE'):
        if isinstance(model, ProcessModel):
            model_name = model.model_name
        else:
            model_name = model

        if isinstance(calc, Calculation):
            calc_name = calc.calc_name
        elif isinstance(calc, str):
            calc_name = calc
        else:
            calc_name = 'nan'

        key = result_model_key2(shock, model_name, calc_name)
        return self.res_models[key]

    def get_resultModel_by_index(self, index):
        return list(self.res_models.values())[index]

    def get_resultModel_list(self):
        return list(self.res_models.values())

    def export_npz(self, filename):
        npy_dict = dict()

        res_data_source = self.result_data_info.to_numpy()
        res_data_arr = []

        for res_row in res_data_source:
            res_data_arr.append(tuple(res_row))

        npy_dict['result_info'] = np.array(res_data_arr, dtype=[
                                ('REF_DT', 'S10'),
                                ('RESULT_ID', 'S255'),
                                ('RESULT_NM', 'S25'),
                                ('SCENARIO_ID', 'S255'),
                                ('SHOCK_NAME', 'S255'),
                                ('SHOCK_SEQ', 'i4'),
                                ('REF_INDEX_CD', 'S255'),
                                ('MODEL_TYPE', 'S25'),
                                ('CALCULATION', 'S25'),
                                ('ORIGIN_CURRENCY', 'S10'),
                                ('TARGET_CURRENCY', 'S10'),
                                ('OUTPUT', 'S10'),
                                ('CALC_TYPE', 'S10'),
                                ('SCENARIO_NUM', 'i4'),
                                ('T_COUNT', 'i4'),
                                ('STEP_PER_YEAR', 'i4'),
                                ('GEN_START_TIME', 'S12'),
                                ('GEN_END_TIME', 'S12'),
                                ('GEN_TYPE', 'i4'),
                                ('STATUS_MESSAGE', 'S255'),
                                ('STATUS', 'i4'),
                                ('DESCRIPTION', 'S255'),
                                ('FILEPATH', 'S255')])

        timegrid_arr = []
        for t_row in self.timegrid:
            timegrid_arr.append((t_row.INDEX, t_row.DATE, t_row.T, t_row.DT))

        npy_dict['timegrid']= np.array(timegrid_arr,
                                       dtype = [('INDEX', 'i4'), ('DATE', 'S10'), ('T', 'f4'), ('DT', 'f4')])

        for model in self.res_models.values():
            npy_dict[model.name] = model.data

        np.savez(filename, **npy_dict)


def xeResultLoad(result_obj, start_pos, end_pos):
    result_obj.load(start_pos, end_pos)
    return result_obj.arr


def resultModel_list(set_name, scen_name, result_name):
    result_dir = xen_result_dir() + '/' + set_name + '/' + scen_name + '/' + result_name

    result_data_info = build_result_data_info(result_dir + '/' + resultinfo_filename)
    result_arr = dict()
    # for model_name, shock_nm, calculation, filepath, calc_type in zip(result_data_info['REF_INDEX_CD'], result_data_info['SHOCK_NAME'], result_data_info['CALCULATION'], result_data_info['FILEPATH'], result_data_info['CALC_TYPE']):
    #     result_arr[str(model_name) + '_' + str(shock_nm) + '_' + str(calculation)] = ResultObj(filepath, calc_type)
    for index, row in result_data_info.iterrows():
        result_arr[result_model_key(row)] = ResultModel(row)
        #result_arr[str(row['REF_INDEX_CD']) + '_' + str(row['SHOCK_NAME']) + '_' + str(row['CALCULATION'])] = ResultModel(row)

    return result_arr


def resultObj_list():
    res = []
    scen_set_items = os.listdir(xen_result_dir())

    for scen_set in scen_set_items:
        scen_id_items = os.listdir(xen_result_dir() + dir_sep + scen_set)
        for scen_id in scen_id_items:
            result_id_items = os.listdir(xen_result_dir() + dir_sep + scen_set + dir_sep + scen_id)
            for result_id in result_id_items:
                #res.append([scen_set, scen_id, result_id, ResultObj(scen_set, scen_id, result_id)])
                res.append(ResultObj(scen_set, scen_id, result_id))

    return res


# def xeResultFile(file_full_path):
#     result_obj = ResultObj(file_full_path)
#     return result_obj


def xeResultAggregate(result_obj_list, scen_num):
    arr = []

    for obj in result_obj_list:
        obj.load(scen_num,scen_num)
        arr.append(obj.arr[0])

    return np.array(arr)


class CaliResultObj:
    def __init__(self, cali_name, model_name, result_name):
        self.cali_name = cali_name
        self.model_name = model_name
        self.result_name = result_name

        self.detail_info = None
        self.parameters_info = None

        self.initialize()

    def initialize(self):
        self.detail_info = build_cali_result_detail_info2(self.cali_name, self.model_name, self.result_name)
        self.parameters_info = build_cali_result_parameters_info2(self.cali_name, self.model_name, self.result_name)




