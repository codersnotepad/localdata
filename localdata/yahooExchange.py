def yahooExchange(exchange=None,
                columns=None):

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
    dsource = 'yahoo'
    dtype = 'exchange'
    dcolumns = ['symbol','name','industry','max_date','min_date','records']
    dexchanges = ['AMEX','NASDAQ','NYSE','OTCB']

    #--- variable validation
    if exchange == None:

        sys.exit("ERROR: Please specify an Exchange. e.g. exchange='amex'")

    exchange = exchange.upper()

    if exchange not in dexchanges:

        sys.exit("ERROR: invalid exchange supplied '"+exchange+"' Valid excahnges"+str(dexchanges))

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

    #--- extract summary
    print('----------------------------------------------------------------------------------------')
    print('Extract Summary')
    print('----------------------------------------------------------------------------------------')
    print('- Exchange:   ',exchange)
    print('- Columns:    ',columns)


    #--- extract data
    df = pd.read_pickle(w.data_dir+dsource+w.dir_delimiter+dtype+w.dir_delimiter+exchange.lower()+'.xz')

    return df
