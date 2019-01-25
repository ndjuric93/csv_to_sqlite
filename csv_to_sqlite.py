import sys
import sqlite3

def read_file_lines(path):
    """ Read file lines from the specific path """
    print('Opening file ' + path)
    with open(path, 'r') as file:
        return file.read().splitlines()


def parse_path():
    """ Parses path to the csv file, exits if file is not supplied """
    if len(sys.argv) < 2:
        print('No csv file specified, exiting')
        print('Please enter path to csv file as a first argument')
        exit()
    return sys.argv[1]


def parse_data(csv):
    """ Parses CSV data """
    keys, values = csv[0], csv[1:]
    return keys, values


def create_database(file_name):
    """ Creates SQLite database and returns cursor """
    conn = sqlite3.connect(file_name + '.db')
    return conn.cursor()


def create_table(cursor, table_name, keys):
    """ Creates table with given cursor, columns with given keys in a given table name """
    print('Creating table...')
    db_keys = '(' + keys + ')'
    cursor.execute(f"CREATE TABLE {table_name} {db_keys}")
    print('Table ' + table_name + ' created')


def insert_values(cursor, table_name, values):
    """ Inserts given values into table with given cursor in a given table name """
    print('Inserting values...')
    for value in values:
        value_list = value.split(',')
        value_placeholder = '(' + ','.join('?' * (len(value_list))) + ')'
        cursor.execute(f"INSERT INTO {table_name} VALUES {value_placeholder}", value_list)
    print('Inserted ' + str(len(values)) + ' records!')

if __name__ == '__main__':
    print('---------------------------')
    print('CSV to SQLite')
    print('---------------------------')
    path = parse_path()
    csv = read_file_lines(path=path)
    keys, values = parse_data(csv=csv)
    file_name = path[0:-4]
    cursor = create_database(file_name=file_name)
    create_table(cursor=cursor, table_name=file_name, keys=keys)
    insert_values(cursor=cursor, table_name=file_name, values=values)
    print('Finished!')
