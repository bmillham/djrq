djrq Installation instructions.

Installation is easy, only python is required, and virtualenv is strongly recommended. These instructions assume you will be using virtualenv.

You will need to decide where to install DJRQ. A good idea would be: ~/www/djrq

Here are the simple steps to getting DJRQ running in development mode.

brian@cyberman ~ $ mkdir -p ~/www
brian@cyberman ~ $ cd ~/www
brian@cyberman ~/www $ git clone https://github.com/bmillham/djrq.git

DJRQ will now be in ~/www/djrq

Now setup the virtualenv

brian@cyberman ~/www $ cd djrq
brian@cyberman ~/www/djrq $ virtualenv --distribute --no-site-packages .

This installs virtualenv to ~/www/djrq. Now activate the vitrualenv

brian@cyberman ~/www/djrq $ . bin/activate

Now install WebCore and all dependencies

(djrq)brian@cyberman ~/www/djrq $ cd DJRQ
(djrq)brian@cyberman ~/www/djrq/DJRQ $ python setup.py install

Step 2 may take a little while to run, as it's installing dependencies. If installing oursql fails, you will need to install libmysqlclient-dev

DJRQ, WebCore and all dependencies are now installed.
Now, copy development.example.ini to development.ini  (~/www/djrq/DJRQ/development.example.ini)
Edit development.ini, and change the db.djname.url lines (there are 2 of them) to match your database credentials.

At this time, only 1 DJ database is supported, but the example does show more than one. This will work in the near future.

Now it's time to test things out!

Make sure you still have your virtualenv active.

(djrq)brian@cyberman ~/www/djrq/DJRQ $ paster serve --reload development.ini

Now point your web browser to localhost:8080 to view your site!

Setting up to run under nginX in production mode:
COMING SOON!

nginx sample config file is in nginx.example.conf
