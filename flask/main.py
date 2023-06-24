
import uuid 
from flask import Flask, request, jsonify, abort, render_template


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = "1318d3d1-d979-47e1-a225-dab1751dbe75"
todo_list_2_id = "3062dc25-6b80-4315-bb1d-a7c86b014c65"
todo_list_3_id = "44b02e00-03bc-451d-8d01-0c67ea866fee"
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# basis for data structure
todo_lists = []
entries = []

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/")
def main_page():
    return "<p>Hallo</p>"


# endpoints for getting, deleting and changing the name of todo lists
@app.route("/todo-list/<list_id>", methods=["GET", "DELETE", "PATCH"])
def handle_list(list_id):
    # find todo list by a given ID
    list_item = None
    for l in todo_lists:
        if l["id"] == list_id:
            list_item = l
            break
    # if ID is invalid return not found
    if not list_item:
        abort(404)
    if request.method == "GET":
        # return todo entries for the todo list corresponding to the provided ID
        print("Returning todo list...")
        return jsonify([i for i in entries if i["list"] == list_id])
    elif request.method == "DELETE":
        # delete list of id
        print("Deleting todo list...")
        todo_lists.remove(list_item)
        return "", 200
    elif request.method == "PATCH":
        # change name of list
       data = request.get_json()
       if "name" in data:
            list_item["name"] = data["name"]
            return jsonify({"message": "Name der ToDo-Liste aktualisiert"}), 200
       else:
            return jsonify({"error": "Ungültige Anfrage"}), 400
        
# endpoint for creating a new list
@app.route("/todo-list", methods=["POST"])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print("Got new list to be added: {}".format(new_list))
    # create id for new list, save it and return the list with id
    new_list["id"] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# endpoint for retrieving all lists
@app.route("/todo-list", methods=["GET"])
def get_all_lists():
    if not todo_lists:
        return jsonify
    return jsonify(todo_lists)

# endpoint for adding a new entry to a list
@app.route("/todo-list/<list_id>/entry", methods=["POST"])
def add_to_list(list_id):
    new_entry = request.get_json(force=True)
    create_entry = {
        'id' : str(uuid.uuid4()),
        'name' : new_entry["name"],
        'description' : new_entry["description"],
        'list' : list_id
    }
    entries.append(create_entry)
    return create_entry

# endpoint to update an existing entry in a list
@app.route("/entry/<entry_id>", methods = ["PATCH", "DELETE"])
def handle_entry(entry_id):
        entries_item = None
        for l in entries:
            if l["id"] == entry_id:
                entries_item = l
                break
        # if ID is invalid return not found
        if not entries_item:
            abort(404)
        if request.method == "PATCH":
            data = request.get_json()
            if "name" in data and "description" in data:
                entries_item["name"] = data["name"]
                entries_item["description"] = data["description"]
                return jsonify({"message": "Eintrag aktualisiert"}), 200
            else:
                return jsonify({"error": "Ungültige Anfrage"}), 400
        elif request.method == "DELETE":
            entries.remove(entries_item)
            print(entries)
            return jsonify({"message" : "Eintrag gelöscht"}), 200


if __name__ == "__main__":
    # start Flask server
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
