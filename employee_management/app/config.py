
import os # a python module that helps with operating system task

base_dir=os.path.abspath(os.path.dirname(__file__)) 
#file_ = is the special variable that contains path of current script

# os.path.dirname(_file_) - gets the directory name component of the path

# os.path.abspath() - it converts the relative path to absolute path from the os.path.dirname()

 

#print(base_dir)

class Config:

    SECRET_KEY=os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_dir, 'employees.db')

    sQLALCHEMY_TRACK_MODIFICATIONS=False