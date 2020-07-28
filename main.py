from ighelper import IgHelper
from settings import USE_MONGO

if __name__ == '__main__':
    ighelper = IgHelper()
    print("Your unfollowers are: ")
    for unfollower in ighelper.unfollowers:
        print(unfollower)

    if USE_MONGO:
        ighelper.dump_to_mongo()
