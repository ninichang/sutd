''' 
 The __init__.py serves double duty: it will contain the application factory, 
 and it tells Python that the flaskr directory should be treated as a package.

 Usage:
 - change the issue variable to the chosen policy / social issue
'''

import os
from flask import Flask, render_template, url_for, redirect, request, session, flash, jsonify
from flask_pymongo import PyMongo



### VARIABLES
issue = '(whatever policy chosen)'

reasonings = {
    'reasoning1' : 'some reasoning',
    'reasoning2' : 'some reasoning',
    'reasoning3' : 'some reasoning',
    'reasoning4' : 'some reasoning',
    'reasoning5' : 'some reasoning'
}

# reasonings_3 : the reasonings users need to give fairness scores for in stage3
# ideally reasonings_3 should be dictionary, each reasoning corresponds to a fairness score

reasonings_3 = {
    'reasoning1': 3,
    'reasoning2': 1, 
    'reasoning3': 5, 
    'reasoning4': 4, 
    'reasoning5': 3, 
    'reasoning6': 1
}

dimensions = {
    'dim1' : 'some dimension', 
    'dim2' : 'some dimension', 
    'dim3' : 'some dimension'
}


fair_dims = {
    'fair_dim1': 'some fairness dimension',
    'fair_dim2': 'some fairness dimension',
    'fair_dim3': 'some fairness dimension'
}



### ROUTES
def create_app(test_config=None):
    # create and configure the app
    app = Flask('research', instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='1234566666',
    )

    app.config["MONGO_URI"] = "mongodb://localhost:27017/sutd"
    mongo = PyMongo(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/stage1')
    def stage1():
        return render_template('1-1.html', issue=issue)

    @app.route('/1-2', methods=['POST', 'GET'])
    def func_for_1_2():
        return render_template('1-2.html', issue=issue)
 

    # only after you submit a form can you access this page
    @app.route('/1-3', methods=['POST'])
    def func_for_1_3():
        username = request.form.get('userName')
        email = request.form.get('userEmail')
        original_stance = request.form.get('original_stance')
        reasoning_for_original_stance = request.form.get('reasoning')

        # only save the user information into the database if the username does not already exist
        if username and email and original_stance and reasoning_for_original_stance and not mongo.db.users.find_one({"username":username}):

            for max_id_user in mongo.db.users.find().sort("id", -1).limit(1):
                next_id = max_id_user["id"] + 1

            # save the form input values in 1-2 into the database
            mongo.db.users.insert({
                "id": next_id,
                "username": username,
                "email": email,
                "original stance": original_stance,
                "reasoning for original stance" : reasoning_for_original_stance
                }) 


        original_stance_value = int(original_stance)
        oppo_stance = ''
        if original_stance_value == 3:
            oppo_stance = 'agree or disagree'
            return render_template('1-3-2.html', oppo_stance=oppo_stance)
        elif original_stance_value > 3:
            oppo_stance = 'disagree'
        else:
            oppo_stance = 'agree'
        session['oppo_stance'] = oppo_stance
        return render_template('1-3.html') 


        # # store the reasoning for opposite stance into the database
        # if request.form.get('oppo_reasoning'):
        #     mongo
        #     # be careful with the mongo.db.users.update. You need all the key value pairs inside
        #     # retrieve the user in python and then append the new information to it
        #     # use session for the username



    @app.route('/stage2')
    def stage2():
        return render_template('2-1.html')

    @app.route('/2-2', methods=['GET', 'POST'])
    def func_for_2_2():
        if request.method == 'POST':
            session['user_stage_2'] = str(request.form.get('inputUserName'))
            if mongo.db.users.find_one({"username":session['user_stage_2']}):
                return render_template('2-2.html', 
                    reasonings=reasonings, 
                    dimensions=dimensions, 
                    user=session['user_stage_2'])
            else:
                return render_template('notRegistered.html', user=session['user_stage_2'])


    @app.route('/stage3')
    def stage3():
        return render_template('3-1.html')

    @app.route('/3-2', methods=['GET', 'POST'])
    def func_for_3_2():
        if request.method == 'POST':
            if request.form.get('inputUserName'):
                user = str(request.form.get('inputUserName'))
                if mongo.db.users.find_one({"username":user}):
                    return render_template('3-2.html', 
                        reasonings_3=reasonings_3, 
                        fair_dims=fair_dims,
                        user=user)
                else:
                    return render_template('notRegistered.html', user=user)
        elif request.method == 'GET':
            return 'hello'



    # for debugging : can enter all the stage html templates directly in the url
    @app.route('/<string:stageID>')
    def goTo(stageID):
        url = stageID + '.html'
        return render_template(url, issue=issue)


    # database testing
    @app.route('/testing-<string:userName>')
    def testing(userName):
        if userName == ' ':
            return jsonify({"exists":'no'})
        elif mongo.db.users.find_one({"username":userName}):
            return jsonify({"exists":'yes'})
        else:
            return jsonify({"exists":'no'})
    

    # @app.route('/thank_you', methods=['POST'])
    # def thank_you():
    #     if request.form.get('form-1-3-2'):



    #         return render_template('thank_you.html')


    @app.route('/end', methods=['POST'])
    def end():
        return render_template('/end.html')

    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))
    return app

