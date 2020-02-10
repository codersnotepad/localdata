def eoddataPrice(exchange=None,
                symbols=None,
                startDate=None,
                endDate=None,
                printStats=False,
                printGraph=False,
                columns=None,
                frequency=None):

    import sys, os, platform
    if platform.system() == 'Windows':
        sys.path.insert(0, os.path.abspath('W:\\common\\python'))
    elif platform.system() == 'Linux':
        sys.path.insert(0, os.path.abspath('/mnt/ns01/common/python'))
    elif platform.system() == 'Darwin':
        sys.path.insert(0, os.path.abspath('/Users/Shared/CPU/common/python'))

    import who_am_i as w

    #--- imports/variables
    import pandas as pd
    import re
    from os import listdir
    from os.path import isfile, join
    from os import path
    from datetime import date

    #--- default varaibles
    dsource = 'eoddata'
    dtype = 'price'
    #dfrequency = ['day','month','quarter']
    dfrequency = ['day']
    dcolumns = ['symbol','open','high','low','close','volume']
    dexchanges = ['AMEX','NASDAQ','NYSE','OTCB']

    #--- variable validation
    if exchange == None:

        sys.exit("ERROR: Please specify an Exchange. e.g. exchange='amex'")

    exchange = exchange.upper()

    if exchange not in dexchanges:

        sys.exit("ERROR: invalid exchange supplied '"+exchange+"' Valid excahnges"+str(dexchanges))

    if startDate != None:

        if not re.match('\d{4}-\d{2}-\d{2}$',startDate):

            sys.exit('ERROR: startDate does not match format yyyy-mm-dd.')

    else:

        startDate = '1900-09-09'

    if endDate != None:

        if not re.match('\d{4}-\d{2}-\d{2}$',endDate):

            sys.exit('ERROR: endDate does not match format yyyy-mm-dd.')

    else:

        endDate = date.today().strftime('%Y-%m-%d')

    if symbols == None:

        #--- get random symbol from exchange
        symbols = 'RYF'

    #--- get symbols
    if isinstance(symbols,str):

        symbols = [symbols.upper()]

    elif isinstance(symbols,list):
        slist = list()
        for s in symbols:

            slist.append(s.upper())

        symbols = slist

    #--- get columns
    if columns == None:

        columns = dcolumns

    if isinstance(columns,str):

        columns = [columns.lower()]

    elif isinstance(columns,list):
        clist = list()
        for c in columns:

            clist.append(c.lower())

        columns = clist

    #--- check columns
    for c in columns:

        if c not in dcolumns:

            sys.exit("ERROR: invalid column supplied '"+c+"'")

    #--- get frequency
    if frequency == None:

        frequency = 'day'

    if not isinstance(frequency, str):

        sys.exit("ERROR: invalid frequency supplied '"+str(frequency)+"'")

    frequency = frequency.lower()

    if frequency not in dfrequency:

        sys.exit("ERROR: invalid frequency supplied '"+frequency+"'")

    #--- extract summary
    print('----------------------------------------------------------------------------------------')
    print('Extract Summary')
    print('----------------------------------------------------------------------------------------')
    print('- Exchange:   ',exchange)
    print('- Symbol(s):  ',symbols)
    print('- Start Date: ',startDate)
    print('- End Date:   ',endDate)
    print('- Columns:    ',columns)
    print('- Print Stats:',printStats)
    print('- Print Graph:',printGraph)

    #--- get list of possible files
    indata_dir = w.data_dir+dsource+w.dir_delimiter+dtype+w.dir_delimiter+frequency+w.dir_delimiter
    filelist = [f for f in listdir(indata_dir) if isfile(join(indata_dir, f)) and re.match(exchange.lower()+'_\d{4}.xz$',f)]
    filelist.sort()

    #--- get years from files
    years = list()
    for file in filelist:

        year = file.replace(exchange.lower()+'_','')
        year = year.replace('.xz','')
        year = int(year)
        years.append(year)

    startYear = int(startDate[:4])
    endYear = int(endDate[:4])
    years = [i for i in years if i >= startYear and i <= endYear]

    #--- create table list
    infiles = list()
    for year in years:

        file = indata_dir+exchange.lower()+'_'+str(year).strip()+'.xz'
        infiles.append(file)

    #--- extract data
    df = pd.DataFrame()
    pd_SD = pd.to_datetime(startDate).date()
    pd_ED = pd.to_datetime(endDate).date()

    for file in infiles:

        _df = pd.read_pickle(file)
        _df = _df.loc[(_df['date'] >= pd_SD) & (_df['date'] <= pd_ED) & (_df['symbol'].str.strip().isin(symbols))]

        if df.empty:

            df = _df

        else:

            df = df.append(_df)

    df.sort_values(by='date', inplace=True)
    df.set_index('date', inplace=True)
    df = df[columns]

    if printGraph == True:

        df.plot()

    if printStats == True:

        print('NOTE: printStats in development.')

    return df
