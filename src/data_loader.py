import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import re
from io import StringIO
from logger import logger
from psycopg2 import sql


def load_data(connection_params: dict, table_name: str, file_path: str) -> pd.DataFrame:
    try:
        # Connect to the database
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Fetch data from the database
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)

        # Log information
        logger.info("Successfully fetched data from the database.")

    except Exception as e_db:
        # Log the error
        logger.error(f"Error fetching data from the database: {e_db}")

        try:
            # Try reading data from CSV file
            df = pd.read_csv(file_path)

            # Log information
            logger.info("Successfully loaded data from the CSV file.")

        except Exception as e_csv:
            # Log the error
            logger.error(f"Error reading data from CSV file: {e_csv}")
            df = pd.DataFrame()

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed.")

    return df



def load_sql_to_dataframe(file_path: str) -> pd.DataFrame:
    try:

        # Read the content of the SQL dump file
        with open(file_path, 'r') as file:
            sql_dump = file.read()

        # Find the start of the data section
        start_index = re.search(r'FROM stdin;', sql_dump).end() + 1

        # Extract the column names
        columns = re.search(r'COPY public.xdr_data (.+?) FROM stdin;', sql_dump).group(1).split(', ')

        # Extract the data part
        data_part = sql_dump[start_index:]

        # Create a StringIO object to simulate a file-like object
        data_io = StringIO(data_part)

        # Read the data into a Pandas DataFrame
        df = pd.read_csv(data_io, delimiter='\t', header=None)

        # Set column names
        df.columns = columns

        logger.info('Load sql file dumped data to pandas dataframe.')
    except Exception as e:
            logger.error(e)
    return df

def run_sql_query(connection_params: dict, query: str) -> None:
    try:
        connection = psycopg2.connect(**connection_params)

        # Create a cursor
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(query)

        # Commit the transaction
        connection.commit()

        # Log success
        logger.info(f'Successfully ran SQL query: {query}')

    except Exception as e:
        # Log the error
        logger.error(f'Error running SQL query: {e}')

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return None



def populate_dataframe_to_database(connection_params: dict, df: pd.DataFrame, table_name:str) -> None:
    try:

        # Extract connection parameters
        db_url = f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"

        

        # Create database connection
        engine = create_engine(db_url, echo=False)

        # Log information
        logger.info("Successfully connected to the database.")

        # Insert DataFrame into the database
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        # Log information
        logger.info(f"Inserted {len(df)} rows into the database table {table_name}.")

    except Exception as e:
        # Log the error
        logger.error(f"Error inserting data into the database: {e}")

    finally:
        # Close the connection
        if engine:
            engine.dispose()
            logger.info("Database connection closed.")

    return None

