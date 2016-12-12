"""
Upload dwca
Unzip dwca
for [taxo, distribution, vernacular, associates]:
    Read into panadas data frame
    Save data frame to db
"""

from django.conf import settings

def upload_dwca(zipfile):
    pass

def unzip_dwca(zipfile):
    pass

def append_dwca(dwca_path):
    pass
    # user = settings.DATABASES['default']['USER']
    # password = settings.DATABASES['default']['PASSWORD']
    # database_name = settings.DATABASES['default']['NAME']
    #
    # database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    #     user=user,
    #     password=password,
    #     database_name=database_name,
    # )
    #
    # engine = create_engine(database_url, echo=False)
    # df.to_sql(HistoricalPrices, con=engine)
    # return()
