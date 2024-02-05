from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://Kolo:leceki73@skins.dpdrssl.mongodb.net/?retryWrites=true&w=majority")
db = client['CommunityDragon']
collection = db['List_of_Skins']

root_url = "http://localhost:5000"
res = "https://raw.communitydragon.org/latest/plugins"

all_data_cursor = collection.find({})
all_data_list = list(all_data_cursor)
app.config['all_data'] = all_data_list
# print(all_data_list)

@app.route('/')
def index():

    return render_template('index.html', res=res, image_sources=all_data_list, root_url=root_url)


@app.route('/skin/<champion_skin_name>')
def skin_details(champion_skin_name):
    matching_object = None
    for obj in all_data_list:
        if obj.get("name") == champion_skin_name:
            matching_object = obj
            break

    # if matching_object:
    #     print("Matching object found:")
    #     print(matching_object)
    # else:
    #     print("No matching object found.")
    return render_template('skin_details.html', skin_data=matching_object, image_sources=all_data_list, res=res, root_url=root_url)


# @app.route('/champions/list')
# def champion_list():
if __name__ == '__main__':
    app.run(debug=False)