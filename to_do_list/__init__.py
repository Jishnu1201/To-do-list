import os
import random

from flask import Flask, render_template

from . import db

def create_app(test_config=None):
    app = Flask("to_do_list")
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'todolist.sqlite')
    )

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import tasks
    app.register_blueprint(tasks.bp)

    from . import db 
    db.init_app(app) 


    return app

if __name__ == "__main__":
    create_app().run
    
