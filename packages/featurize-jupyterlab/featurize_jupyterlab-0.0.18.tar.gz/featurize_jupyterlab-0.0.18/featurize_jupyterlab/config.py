from sqlalchemy import create_engine
import os


class Config:
    if os.environ.get('FENV', None) == 'test':
        engine = create_engine('postgresql+psycopg2://featurize:featurizepw@localhost:5432/featurize_test')
    else:
        engine = create_engine('postgresql+psycopg2://featurize:featurizepw@localhost:5432/featurize')

    server_addr = '127.0.0.1'
    rpc_port = '6725'
