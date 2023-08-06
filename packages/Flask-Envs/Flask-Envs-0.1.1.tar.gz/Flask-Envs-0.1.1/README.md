# Flask-Envs

<div class="module">

flask\_envs

</div>

Flask-Envs provides environment tools and configuration for Flask applications.

This package is built on top of its original "Flask Environments" package
which is not maintained any longer.

Flask-Envs was built to make it easy for developers to use Flask Environments
in Python 3


# Installation

> $ pip install flask-envs

# Getting Started

The following code illustrates how to setup environment based
configuration. The first thing to do is create a configuration file.
These can be created using Python or Yaml.

Python:

    class Config(object):
        DEBUG = False
        TESTING = False

    class Development(Config):
        DEBUG = True
        DATABASE = 'development_db'

    class Production(Config):
        DATABASE = 'production_db'

Yaml:

    COMMON: &common
      DEBUG: False
      TESTING: False

    DEVELOPMENT: &development
      <<: *common
      DEBUG: True
      DATABASE: 'development_db'

    PRODUCTION: &production
      <<: *common
      DATABASE: 'production_db'

Next, create your application and initialize the Environments
extensions:

    from flask import Flask
    from flask_envs import Environments

    app = Flask(__name__)
    env = Environments(self.app)

Then simply use the <span class="title-ref">from\_object</span> method
or the <span class="title-ref">from\_yaml</span> method to load the
configuration:

    env.from_object('myapp.config')
    env.from_yaml(os.path.join(os.getcwd(), 'myapp', 'config.yml'))

Only the values for the specified environment will be applied.

Flask-Envs assumes an operating system environment variable
named <span class="title-ref">FLASK\_ENV</span> will be set to one of
your possible environments. If it is not set, it will default to
<span class="title-ref">DEVELOPMENT</span>.

To change the default environment or the environment varibale name pass
the <span class="title-ref">var\_name</span> or
<span class="title-ref">default\_env</span> parameters to the
Environments constructor like so:

    from flask import Flask
    from flask_envs import Environments

    app = Flask(__name__)
    env = Environments(self.app, var_name='CUSTOM_VAR_NAME', default_env='CUSTOM_ENV')