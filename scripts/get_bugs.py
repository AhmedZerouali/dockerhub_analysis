########## HERE WE EXTRACT BUGS FROM UDD ###############
import psycopg2
import pandas as pd
from tqdm import tqdm

def connexion_udd():
        conn_string="host='udd-mirror.debian.net' port='5432' dbname='udd' user='udd-mirror' password='udd-mirror'"
        conn = psycopg2.connect(conn_string)
        conn.set_client_encoding('UTF8')
        cursor = conn.cursor()
        return cursor
    
def extract_bugs_from_udd(cursor,source):

    cursor.execute(
        "SELECT DISTINCT bugs.source, bugs.id, bugs.status, bugs.severity, "+
        "bugs.arrival, bugs.last_modified, bugs_found_in.version, bugs_fixed_in.version "+
        "FROM bugs_found_in, bugs LEFT JOIN bugs_fixed_in "+
        "ON bugs.id=bugs_fixed_in.id "+
        "WHERE bugs.id=bugs_found_in.id "+
        "AND bugs.source='"+source+"' ")
    normal=cursor.fetchall()

    cursor.execute(
    "SELECT DISTINCT archived_bugs.source, archived_bugs.id, archived_bugs.status, archived_bugs.severity, "+
    "archived_bugs.arrival, archived_bugs.last_modified, "+
    "archived_bugs_found_in.version, archived_bugs_fixed_in.version "+
    "FROM archived_bugs_found_in, archived_bugs LEFT JOIN archived_bugs_fixed_in "+
    "ON archived_bugs.id=archived_bugs_fixed_in.id "+
    "WHERE archived_bugs.id=archived_bugs_found_in.id "+
    "AND archived_bugs.source='"+source+"'")
    archive=cursor.fetchall()
    
    return normal, archive

def main():
    cursor=connexion_udd()

    sources = pd.read_csv('../data/for_analysis/installed_packages.csv',
        usecols=['source'])
    sources  = sources.source.drop_duplicates().values

    normal = []
    archive = []
    for source in tqdm(sources):
        n, a = extract_bugs_from_udd(cursor, source)
        normal = normal + n
        archive = archive + a

    normal = list(zip(*normal))
    archive = list(zip(*archive))

    columns=['source','debianbug','status','severity','arrival','last_modified','found_in','fixed_in']
    df_normal = pd.DataFrame(columns=columns)
    df_archive = pd.DataFrame(columns=columns)

    for index, col in enumerate(columns):
        df_normal[col] = normal[index]
        df_archive[col] = archive[index]

    df_normal['type'] = 'normal'
    df_archive['type'] = 'archive'

    data = pd.concat([df_normal, df_archive])
    data.to_csv('../data/prepared_data/bugs_extracted_20190830.csv', index=False)

if __name__ == "__main__":
    main()
