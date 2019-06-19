''' 
 The __init__.py serves double duty: it will contain the application factory, 
 and it tells Python that the flaskr directory should be treated as a package.

 Usage:
 - change the issue variable to the chosen policy / social issue
'''

import os
from flask import Flask, render_template, url_for, redirect, request

### VARIABLES

reasonings = [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut a urna sit amet urna rhoncus egestas vel eget metus. Duis euismod magna ut erat aliquet, eget aliquet nulla scelerisque. Donec at elit sed lorem blandit facilisis. Morbi tempus metus sit amet orci semper lacinia. In aliquam pellentesque egestas. Maecenas scelerisque suscipit leo. Curabitur ut diam placerat, commodo mi sodales, consectetur sem. Mauris vestibulum dictum arcu in consequat. Cras in odio et est cursus iaculis tempus a massa. Cras nunc mi, convallis eget ipsum et, vehicula tristique enim. Nunc vulputate condimentum pellentesque. Donec molestie sem sed massa mattis, et ultricies ante iaculis. Sed semper odio nunc, ac posuere purus commodo at.', 

            'In quis ex vitae diam laoreet sollicitudin. Vestibulum blandit cursus turpis, a viverra nisl iaculis nec. Nam magna elit, ultrices vitae sodales nec, cursus at odio. Vivamus mollis facilisis consectetur. Pellentesque viverra dictum nisl vitae laoreet. Proin vel hendrerit risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vivamus cursus ante eget lacus pharetra, a varius ligula condimentum. Ut molestie laoreet lobortis.',

            'Nam ac dui rhoncus, malesuada lectus a, facilisis turpis. Pellentesque malesuada leo non mollis tristique. Cras laoreet dolor in risus aliquam vehicula. Etiam nec orci vel lectus aliquet malesuada. Cras vitae vulputate nibh. Mauris est ex, malesuada a sapien et, facilisis tristique quam. Pellentesque tincidunt nunc sed est fermentum ullamcorper. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi eros magna, accumsan in leo sed, laoreet accumsan eros. Morbi lectus metus, cursus vel tincidunt vitae, varius placerat nunc.',

            'Phasellus faucibus feugiat mauris. Aenean aliquet, lorem vel rutrum mollis, enim ex commodo neque, ut congue sem nunc quis turpis. Suspendisse non eros quis neque facilisis congue ut nec velit. Suspendisse at tellus elit. Donec at lacinia erat. Suspendisse tristique metus nec metus congue sodales. Nullam sagittis eu diam venenatis consequat. Nunc dapibus odio ex, non maximus dui laoreet in. Cras sed cursus massa.',

            'Vestibulum eu feugiat neque. Integer hendrerit fringilla justo a dictum. Cras luctus laoreet odio. Quisque aliquet vehicula scelerisque. Sed at egestas urna. Fusce at nisi in erat luctus malesuada in ac lectus. Maecenas commodo placerat nibh id dictum. Ut finibus rutrum magna quis ornare. Donec nunc metus, dignissim sit amet eleifend et, aliquam eget ante. Duis cursus dapibus accumsan.'        
        ]

# reasonings_3 : the reasonings users need to give fairness scores for in stage3
# ideally reasonings_3 should be dictionary, each reasoning corresponds to a fairness score

reasonings_3 = {
    'random reasoning': 3,
    'random reasoning': 1, 
    'random reasoning': 5, 
    'random reasoning': 4, 
    'random reasoning': 3, 
    'random reasoning': 1
}

dimensions = [
    'dimension 1', 'dimension 2', 'dimension 3'
]


fair_dims = [
    'fairness dimension 1', 'fairness dimension 2', 'fairness dimension 3'
]



### ROUTES
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    @app.route('/stage1', methods=['GET', 'POST'])
    def stage1():
        issue = '(whatever policy chosen)'
        return render_template('1-1.html', issue=issue)

    @app.route('/stage2', methods=['GET', 'POST'])
    def stage2():
        return render_template('2-2.html', reasonings=reasonings, 
        dimensions=dimensions)

    @app.route('/stage3', methods=['GET', 'POST'])
    def stage3():
        return render_template('3-2.html', reasonings_3=reasonings_3, fair_dims=fair_dims)

    # for debugging : can enter all the stage html template numbers directly in the url
    @app.route('/<string:stageID>')
    def goTo(stageID):
        url = stageID + '.html'
        issue = '(whatever policy chosen)'
        return render_template(url, issue=issue)

    return app

