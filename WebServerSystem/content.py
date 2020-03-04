from flask_restful import Resource, Api, reqparse, abort
from flask import jsonify
import json
import time
from WebServerSystem.models import db, app, Item

"""
    api返回格式为{"status":XXX,
                  "message":XXX,
                  "data":{...}}
    添加item时，addtime和deadline的日期格式为:XXXX.XX.XX
    否则添加失败
"""

# 实例化api对象
api = Api(app)

# 实例化Paresr对象
parse = reqparse.RequestParser()

parse.add_argument('content', type=str)
parse.add_argument('status', type=int)
parse.add_argument('addtime', type=str)
parse.add_argument('deadline', type=str)


class TabrResource(Resource):
    def options(self):
        return {'Allow': '*'}, 200, {'Access-Control-Allow-Origin': '*',
                                     'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                                     'Access-Control-Allow-Headers': 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild',
                                     }


# 判断日期格式是否合法
def time_valid_or_not(date):
    try:
        time.strptime(date, "%Y.%m.%d")
        return True
    except:
        return False


# 添加时间是否在截止日期之前
def addtime_before_deadline(addtime, deadline):
    time.strptime(addtime, "%Y.%m.%d")
    time.strptime(deadline, "%Y.%m.%d")
    if deadline > addtime:
        return True
    else:
        return False


# 添加待办事项,只接受post请求
class AddItem(TabrResource):
    def post(self):
        # 获取post传来的数据
        args = parse.parse_args()
        content = args["content"]
        status = args["status"]
        addtime = args["addtime"]
        deadline = args["deadline"]
        # 判断日期是否合法
        if time_valid_or_not(addtime) == False or time_valid_or_not(deadline) == False:
            return json.dumps({"status": 1,
                               "message": "invalid addtime or deadline.",
                               "data": None}, ensure_ascii=False)
        # 判断截止日期是否在添加日期之后
        if addtime_before_deadline(addtime, deadline) == False:
            return json.dumps({"status": 1,
                               "message": "deadline before addtime !",
                               "data": None}, ensure_ascii=False)
        try:
            id_list = [item.id for item in Item.query.all()]
            # 没有事项则id从1开始
            new_id = 1
            if len(id_list) == 0:
                new_item = Item(id=new_id, content=content, status=status, addtime=addtime, deadline=deadline)
            else:
                new_id = max(id_list) + 1
                new_item = Item(id=new_id, content=content, status=status, addtime=addtime, deadline=deadline)
            db.session.add(new_item)
            db.session.commit()
            return json.dumps({"status": 0,
                               "message": "add successfully ! item_id = %d" % new_id,
                               "data": None}, ensure_ascii=False)
        except Exception as e:
            print(e)
            return json.dumps({"status": 1,
                               "message": "add failed",
                               "data": None})

    def get(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.post method only.",
            "data": None,
        })

    def put(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.post method only.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.post method only.",
            "data": None,
        })


# 将待办事项设置为已完成
class Set_to_finished(TabrResource):
    def put(self, id):  # id=0 时即将所有事待办事项设置为已完成

        if id == 0:
            item_list = Item.query.filter_by(status=0).all()
            for item in item_list:
                item.status = 1
            db.session.commit()
            return json.dumps({"status": 0,
                               "message": "set all to finished successfully !",
                               "data": None})
        else:  # id不为0时将相应id的事项设置为已完成
            item = Item.query.filter_by(id=id).first()
            if item == None:
                abort(404, message="Item not found!")
            item.status = 1
            db.session.commit()
            return json.dumps({"status": 0,
                               "message": "set item (id = %d) to finished success !" % id,
                               "data": None})

    def get(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.put method only.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.put method only.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.put method only.",
            "data": None,
        })


class Get_item(TabrResource):
    def get(self, instruction):
        data = []
        if instruction == "all":
            item_list = Item.query.all()
            for item in (item_list):
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "待办" if item.status == 0 else "已完成",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        elif instruction == "finished":
            item_list = Item.query.filter_by(status=1).all()
            for item in item_list:
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "已完成",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        elif instruction == "todo":
            item_list = Item.query.filter_by(status=0).all()
            for item in item_list:
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "待办",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        else:
            abort(404, message="invalid instruction,your instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        return jsonify({'status': 0,
                        'message': 'get ' + instruction + ' data' if data != [] else "No items found !",
                        'data': data})

    def post(self, instruction):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })

    def delete(self, instruction):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })

    def put(self, instruction):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })


# 获取事项数量
class Get_count(TabrResource):
    def get(self, instruction):
        if instruction == "all":
            num = len(Item.query.all())
        elif instruction == "finished":
            num = len(Item.query.filter_by(status=1).all())
        elif instruction == "todo":
            num = len(Item.query.filter_by(status=0).all())
        else:
            abort(404, message="invalid instruction,our instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        return json.dumps({
            "status": 0,
            "message": "get '" + instruction + "' item count.",
            "data": num,
        }, ensure_ascii=False)

    def post(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })

    def put(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.get method only.",
            "data": None,
        })


# 删除某id事项
class Delete_item_by_id(TabrResource):
    def delete(self, id):
        item = Item.query.filter_by(id=id).first()
        if item == None:
            abort(404, message="Item not found!")
        db.session.delete(item)
        db.session.commit()
        return json.dumps({
            "static": 0,
            "message": "delete item (id = %d) successfully !" % id,
            "data": None
        })

    def put(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })

    def get(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })


# 删除多项事项
class Delete_item_by_instruction(TabrResource):
    def delete(self, instruction):
        if instruction == "all":
            items = Item.query.all()
        elif instruction == "finished":
            items = Item.query.filter_by(status=1).all()
        elif instruction == "todo":
            items = Item.query.filter_by(status=0).all()
        else:
            abort(404, message="invalid instruction,our instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        count = 0
        for item in items:
            count += 1
            db.session.delete(item)
            db.session.commit()
        return json.dumps({
            "status": 0,
            "message": "delete '" + instruction + "' item successfully!",
            "data": {"delete_count": count},
        }, ensure_ascii=False)

    def put(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })

    def get(self):
        return json.dumps({
            "status": 405,
            "message": "invalid method.delete method only.",
            "data": None,
        })


api.add_resource(AddItem, '/add_item')
api.add_resource(Set_to_finished, '/set_to_finished/<int:id>')
api.add_resource(Get_item, '/get_item/<string:instruction>')
api.add_resource(Get_count, "/get_count/<string:instruction>")
api.add_resource(Delete_item_by_id, '/del_item_by_id/<int:id>')
api.add_resource(Delete_item_by_instruction, '/del_item_by_instruction/<string:instruction>')
