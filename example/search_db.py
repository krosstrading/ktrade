from pymongo import MongoClient

def get_data_from_db(code, from_date, until_date, db_suffix = '_D'):
    from_date = from_date if from_date.__class__.__name__ == 'date' else from_date.date()
    until_date = until_date if until_date.__class__.__name__ == 'date' else until_date.date()

    url = 'mongodb://nnnlife:gkdtkd6^tkfwk@192.168.0.22:27017'
    stock_db = MongoClient(url)['stock']
    db_data = list(stock_db[code + db_suffix].find({'0': {'$gte':time_converter.datetime_to_intdate(from_date), '$lte': time_converter.datetime_to_intdate(until_date)}}))
    print(code + db_suffix, time_converter.datetime_to_intdate(from_date), time_converter.datetime_to_intdate(until_date))
    db_data = sort_db_data(db_data, db_suffix)
    days = [time_converter.intdate_to_datetime(d['0']).date() for d in db_data]
    days = list(dict.fromkeys(days))
    working_days = get_working_days(from_date, until_date)
    vacancy_data = list(stock_db[code + '_V'].find({'0': {'$gte':time_converter.datetime_to_intdate(from_date), '$lte': time_converter.datetime_to_intdate(until_date)}}))
    vacancy_days = [time_converter.intdate_to_datetime(d['0']).date() for d in vacancy_data]
    empties = _check_empty_date(days, vacancy_days, working_days)
    #print('DB DATA', len(db_data), 'EMPTIES', empties)
    return db_data, empties

