from flask import Blueprint, request
import json

from test_data import user_list, finish_data, dbstat_data, pieinfo_data, tableinfo_data #test data


#-----API Construction-----#
mainpageApi = Blueprint('mainpageApi', __name__)


#-----Routing Definition-----#
@mainpageApi.route('userprofile', methods=['GET'])
def returnUserprofile():
    user = request.args['user']
    
    """
    連接DB, 拿到user information
    """

    for d in user_list:
        if d["user"] == user:
            print(d)
            return d


@mainpageApi.route('finishinfo', methods=['GET'])
def returnFinishinfo():

    """
    連接DB, 拿到Finish info
    """

    return finish_data

@mainpageApi.route('dbstat', methods=['GET'])
def returnDBstatistic():

    """
    連接DB, 拿到DB的統計資料
    """

    return dbstat_data


@mainpageApi.route('pieinfo', methods=['GET'])
def returnpieinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """

    return pieinfo_data


@mainpageApi.route('tableinfo', methods=['GET'])
def returntableinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """

    return json.dumps(tableinfo_data)