from django.conf import settings
from configparser import ConfigParser
from os import path
from os import listdir
from dwca.read import DwCAReader
from dwca.darwincore.utils import qualname as qn
import pandas as pd
from sqlalchemy import create_engine
from taxonomy.models import DwcaTaxon

def get_connection_string():
    cnf_file_name = settings.DATABASES['default']['OPTIONS']['read_default_file']
    cnf_file_name = my_dir = path.expanduser(cnf_file_name)
    parser = ConfigParser()
    parser.read(cnf_file_name)
    host = parser.get('client', 'host')
    database = parser.get('client', 'database')
    user = parser.get('client', 'user')
    password = parser.get('client', 'password')

    connection_string = 'mysql://{}:{}@{}/{}'.format(user, password, host, database)
    return(connection_string)

def dwca_to_db():
    dwca_files = listdir('dwca')
    if len(dwca_files) == 1:

        # For now, we will only deal with one Darwin Core Archive.
        # If we delete all records from DwcaTaxon, all associated records in the other 3 DwCA
        # tables should disappear because the "on_delete=models.CASCADE" is set.
        DwcaTaxon.objects.all().delete()

        dwca_filename = 'dwca/{}'.format(dwca_files[0])

        # dwca = DwCAReader(dwca_filename) unzips the archive into a tempoary directory
        # named "t/dwca/"
        # dwca.close() removes the temporary directory
        dwca = DwCAReader(dwca_filename)

        df_taxon = pd.read_csv('t/dwca/dwcaTaxon.csv')

        # Add the "bibliographicCitation" constant field to each record
        df_taxon['bibliographicCitation'] = dwca.rows[0].data['http://purl.org/dc/terms/bibliographicCitation']
        engine = create_engine(get_connection_string())
        df_taxon.to_sql('taxonomy_dwcataxon', con=engine, index=False, if_exists='append')

        df_distribution = pd.read_csv('t/dwca/dwcaDistribution.csv')
        df_distribution.to_sql('taxonomy_dwcadistribution', con=engine, index=False, if_exists='append')

        df_vernacular = pd.read_csv('t/dwca/dwcaVernacular.csv')
        df_vernacular.to_sql('taxonomy_dwcavernacular', con=engine, index=False, if_exists='append')

        df_associates = pd.read_csv('t/dwca/dwcaResourceRelationship.csv')
        df_associates.to_sql('taxonomy_dwcaresourcerelationship', con=engine, index=False, if_exists='append')

        # dwca_files.close()
    else:
        print('ERROR Number of files in the dwca directory is not equal to one.')
    return()
