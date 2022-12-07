from flask import Flask, request
from flask_cors import CORS
from optimization import search, scatter_plot, guassian_plot, compare


app = Flask(__name__)
CORS(app)


@app.route('/execute', methods=['POST'])
def execute_optimiser():
    data = request.get_json()
    fields = ['LTX', 'LRX', 'PTX', 'PRX', 'GRX', 'GTX', 'RSX', 'Frequency']
    response = {}
    flag = False
    my_type = True
    missed_field = []

    # Missing field validation
    for field in fields:
        if field not in data:
            flag = True
            missed_field.append(field)
        response = {"error": f'Opps! seems you missed {missed_field} field(s)'}

    # Field data type validation
    for key, value in data.items():
        if type(value) != int:
            if type(value) != float:
                my_type = False
                response = {
                    "error": f'The field {key}, has a value type of String instead of a Number'}
    if not flag:
        if my_type:
            ltx = data['LTX']
            lrx = data['LRX']
            ptx = data['PTX']
            prx = data['PRX']
            grx = data['GRX']
            gtx = data['GTX']
            rsx = data['RSX']
            freq = data['Frequency']
            response = search(ltx, lrx, ptx, prx, grx, gtx, rsx, freq)
    return response


@app.route('/graph', methods=["POST"])
def generate_graph():
    params = request.get_json()
    response = {}
    distance = params['distance']
    margin = params['margin']
    FM = params['FM']
    Av = params['Av']
    FM_con = params['FM_con']
    Av_con = params['Av_con']

    scatter = scatter_plot(distance, margin, FM, Av)
    gaussian = guassian_plot(distance)
    comparison = compare(distance, margin, FM_con, Av_con)
    response = {"scatter": scatter,
                "gaussian": gaussian, "comparison": comparison}
    return response


@app.route('/report', methods=['GET'])
def generate_report():
    return {"status": True}



if __name__ == '__main__':
    app.run(debug=True)