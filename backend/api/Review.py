from flask import Blueprint, request
import json

from test_data import review_example


#-----API Construction-----#
reviewApi = Blueprint('reviewApi', __name__)

#-----Routing Definition-----#
@reviewApi.route('postreview', methods=['POST'])
def updatedbforreview():
    
    """
    連接DB, 更新目前的status
    """
    print(request.data) #可以拿到前端POST
    return "Nothing"


@reviewApi.route('getreview', methods=['GET'])
def getreview():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    import random
    data = review_example[random.randint(0, 2)]
    return data







