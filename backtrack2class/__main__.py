import os

from . import app

INPUT_FILE_NAME = 'input.xlsx'
STATIC_INPUT_FILE_NAME = 'static_input.xlsx'

if __name__ == '__main__':
    data_dir = os.path.join(os.getcwd(), 'data')
    input_file_path = os.path.join(data_dir, INPUT_FILE_NAME)
    static_file_path = os.path.join(data_dir, STATIC_INPUT_FILE_NAME)
    app.run(input_file_path, static_file_path)
