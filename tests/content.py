import sys, os
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from HDUCoursesAPI.db_sqlite import DBSqlite