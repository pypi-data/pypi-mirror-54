from .simple import get_time, read_config

if __name__=='__main__':
    import os
    print('The code is getting executed at this location: ' + os.getcwd())
    get_time()
    print(read_config('config/cities.yaml')['cities'])
